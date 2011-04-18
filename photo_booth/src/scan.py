#!/usr/bin/python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

import pexpect, re
from threading import Thread

import urllib

import subprocess
from Queue import Queue

scans = Queue()
upload_queue = Queue()

class UploadThread(Thread):
    request_stop = False

    def stop(self):
        self.request_stop = True

    def run(self):
        while not self.request_stop:
            (filename, ebid) = upload_queue.get(block=True)
            subprocess.call(["curl", "-s", "-o", "/dev/null", "-F", "photo=@%s" % filename, "http://faces.barcampboston.org/attendee/ebid:%s/photo" % ebid])


class DecodeThread(Thread):
    request_stop = False

    def stop(self):
        self.request_stop = True

    def run(self):
        subprocess.call(["adb", "logcat", "-c"])
        child = pexpect.spawn('adb logcat -s DecodeHandler:D', timeout=10000)
        find_code = re.compile(r'D/DecodeHandler\([^)]+\): (.*)')
        print "running decode thread"
        while not self.request_stop and not child.eof():
            child.expect(find_code)
            scan = child.match.group(1)
            if scan.startswith('Found barcode'):
                continue
            scans.put(scan)
        print "exiting decode thread"


class GTK_Main:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Photobooth")
        window.set_default_size(480, 640)
        window.connect("destroy", gtk.main_quit, "WM destroy")
        vbox = gtk.VBox()
        window.add(vbox)
        self.movie_window = gtk.DrawingArea()
        vbox.add(self.movie_window)
        #window.connect("clicked", self.start_stop)
        hbox = gtk.HBox()
        vbox.pack_start(hbox, False)
        hbox.set_border_width(10)
        hbox.pack_start(gtk.Label())
        self.button = gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        hbox.pack_start(self.button, False)
        self.button2 = gtk.Button("Quit")
        self.button2.connect("clicked", self.exit)
        hbox.pack_start(self.button2, False)
        self.button3 = gtk.Button("Still")
        self.button3.connect("clicked", self.btn_take_still)
        hbox.pack_start(self.button3, False)
        hbox.add(gtk.Label())
        window.show_all()

        # Set up the gstreamer pipeline
        self.player = gst.parse_launch ("v4l2src ! ffmpegcolorspace ! videoflip method=counterclockwise ! xvimagesink")
        
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            self.button.set_label("Stop")
            self.player.set_state(gst.STATE_PLAYING)
        else:
            self.player.set_state(gst.STATE_NULL)
            self.button.set_label("Start")


    ebidre = re.compile(r'EBID:(\d+);')
    def check_for_code(self):

        if scans.empty():
            return True
        scan = scans.get(block=False)

        if scan:
            m = self.ebidre.search(scan)
            if m:
                ebid = m.group(1)
                if not self.countdown_in_progress:
                    self.countdown_take_still("ebid%s.jpg" % ebid, ebid)
        return True


    def exit(self, widget, data=None):
        gtk.main_quit()

    def btn_take_still(self, widget, data=None):
        take_still(self, "pic.jpg")

    countdown_in_progress = False
    def countdown_take_still(self, filename, ebid=None, countdown=10):

        if countdown == 0:
            subprocess.call(["toilet", "--gay", "smile!"])
            subprocess.call(['aplay', '-q', '/home/steve/WTK2.5.2/wtklib/media/shutter.wav'])
            self.take_still(filename, ebid)
            self.countdown_in_progress = False
        else:
            self.countdown_in_progress = True
            subprocess.call(["toilet", "--gay", "%d" % countdown])
            gobject.timeout_add_seconds(1, self.countdown_take_still, filename, ebid, countdown - 1)

        return False

    def take_still(self, filename, ebid=None):
        self.player.set_state(gst.STATE_PAUSED)
        img = self.movie_window.get_window()
        (w,h) = img.get_size()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, w, h)
        pixbuf.get_from_drawable(img, img.get_colormap(), 0,0,0,0,w,h)
        pixbuf.save(filename, "jpeg", {"quality": "85"})
        gobject.timeout_add_seconds(5, self.clear)
        upload_queue.put((filename, ebid))
        subprocess.call(["toilet", "--gay", "Retake? Rescan!"])

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.button.set_label("Start")
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)
            self.button.set_label("Start")

    def resume_view(self):
        subprocess.call(["toilet", "--gay", "Scan QR code with phone -->"])
        self.player.set_state(gst.STATE_PLAYING)
        return False

    def clear(self):
        print "\n" * 60
        self.player.set_state(gst.STATE_NULL)
        gobject.timeout_add_seconds(5, self.resume_view)


    def on_sync_message(self, bus, message):
        print "on_sync_message"
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            # Assign the viewport
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            import time
            time.sleep(1)
            imagesink.set_xwindow_id(self.movie_window.window.xid)
            print "viewport assigned"

if __name__ == '__main__':
    dt = DecodeThread()
    dt.start()

    ut = UploadThread()
    ut.start()

    main = GTK_Main()
    gtk.gdk.threads_init()
    gobject.timeout_add(100, main.check_for_code)
    gtk.main()
    dt.stop()
    ut.stop()
