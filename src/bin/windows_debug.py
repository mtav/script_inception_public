#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import platform
import shutil
import argparse
import tempfile
import subprocess

#cmd = 'magick identify -format %w Desktop\phcno5\phc_2750.jpg'
#subprocess.run(cmd.split())

#from tkinter import filedialog
#from tkinter import *

import tkinter
import tkinter.filedialog
 
root = tkinter.Tk()
#root.filename =  tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
#print (root.filename)

root.filename =  tkinter.filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
print (root.filename)

#import tkinter
#import tkFileDialog

#root = Tkinter.Tk()
#filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
#print(root.tk.splitlist(filez))
