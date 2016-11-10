#!/usr/bin/env python

# setup.py
import sys
from distutils.core import setup
import py2exe

sys.argv.append("py2exe")

setup(
    #options = {'py2exe': {'optimize': 2}},
    windows = [{'script': "smartd-pyngui.py",
				'icon_resources': [(1, smartd-pyngui.ico")]}],
				
    zipfile = "shared.lib",
    #console=["smartd-pyngui.py"],
    data_files=[("", ["smartd-pyngui.ui"])],
    options= {
        "py2exe": { 
            "includes" : ["sys",
						  "pygubu.builder.tkstdwidgets",
                          "pygubu.builder.ttkstdwidgets",
                          "pygubu.builder.widgets.dialog",
                          "pygubu.builder.widgets.editabletreeview",
                          "pygubu.builder.widgets.scrollbarhelper",
                          "pygubu.builder.widgets.scrolledframe",
                          "pygubu.builder.widgets.tkscrollbarhelper",
                          "pygubu.builder.widgets.tkscrolledframe",
                          "pygubu.builder.widgets.pathchooserinput",],
            "excludes" : ["_ssl",
                          "pyreadline",
                          "difflib",
                          "doctest",
                          "locale",
                          "optparse",
                          "calendar",],
            "compressed" : True,
                          
                    }},
        )