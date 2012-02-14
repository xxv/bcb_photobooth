#!/usr/bin/python
# -*- coding: utf-8 -*-

import libxslt, libxml2
import tempfile, subprocess
import urllib
import os
import unicodedata

#####################################################################

class MakePdf:
    def __init__(self, xslt_file, svg_file):
        self.xslt_file = xslt_file
        self.svg_file = svg_file

    def strip_accents(self, s):
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

    def make_pdf(self, params, pdfname):
        style = libxslt.parseStylesheetDoc(libxml2.parseFile(self.xslt_file))
        doc = libxml2.parseFile(self.svg_file)
        result = style.applyStylesheet(doc, self.quotify(params))
        (fd, tmp) = tempfile.mkstemp(suffix=".svg")
        style.saveResultToFd(fd, result)
        print tmp
        subprocess.call(["inkscape", "-A", pdfname, tmp])
        os.unlink(tmp)

    def quotify(self, params):
        params_quoted = dict(params)
        for k,v in params_quoted.iteritems():
            v = ('%s' % v).replace('\"', '&quot;')
            v = ('%s' % v).replace("\'", '&apos;')
            params_quoted[k] = str(self.strip_accents(u"'%s'" % v))
        print params_quoted
        return params_quoted
