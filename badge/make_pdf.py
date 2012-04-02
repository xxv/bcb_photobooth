#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader
import subprocess
from tempfile import NamedTemporaryFile
import unicodedata

#####################################################################

class MakePdf:
    def __init__(self, package, svg_file):
        self.svg_file = svg_file
        self.env = Environment(loader=PackageLoader(package))
        self.template = self.env.get_template(svg_file)

    def strip_accents(self, s):
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

    def make_pdf(self, params, pdfname):
        temp = NamedTemporaryFile(mode="w", suffix=".svg")
        temp.write(self.template.render(params).encode('utf-8'))
        temp.flush()

        subprocess.call(["inkscape", "--export-dpi", "300", "-A", pdfname, temp.name])
        temp.close()
