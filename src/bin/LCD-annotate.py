#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import platform
import shutil
import argparse
import tempfile
import subprocess

def main():
  parser = argparse.ArgumentParser(description='Annotate LCD measurements and optionally create animations. Example usage: ./LCD-annotate.py -d output --avi --gif no8*.jpg')
  parser.add_argument('infile_list', metavar='INFILE', nargs='*')
  parser.add_argument('--not-sorted', action="store_true", help='Do not sort the input files before creating an animation. (default is to sort by decreasing temperature)')
  parser.add_argument('--not-reverse', action="store_true", help='Sort by increasing temperature, rather than the default by decreasing temperature.')
  parser.add_argument('--gif-filename', help='GIF output filename')
  parser.add_argument('--avi-filename', help='AVI output filename')
  parser.add_argument('--gif', action="store_true", help='Create GIF output')
  parser.add_argument('--avi', action="store_true", help='Create AVI output')
  parser.add_argument('--delay', type=int, default=100, help='GIF output: Set the time delay (in 1/100th of a second) for the GIF output')
  parser.add_argument('--loop', type=int, default=0, help='GIF output: Number of times the GIF animation is to cycle though the image sequence before stopping. Usually this is set by default to zero (infinite loop).')
  # parser.add_argument('--resize-images', type=int, default=20, help='GIF output: Resize the pictures before creating an animation in order to reduce size of the file and the time it takes to generate it. Value in percent. Default=20%%.')
  # parser.add_argument('--resize-gif', type=int, default=20, help='GIF output: Resize the pictures before creating an animation in order to reduce size of the file and the time it takes to generate it. Value in percent. Default=20%%.')
  parser.add_argument('--resize', type=int, default=20, help='GIF output: Resize the pictures before creating an animation in order to reduce size of the file and the time it takes to generate it. Value in percent. Default=20%%.')
  parser.add_argument('-d', '--dstdir', default=tempfile.mkdtemp(), nargs='?')
  parser.add_argument('--tmpdir', default=tempfile.mkdtemp(), nargs='?', help='temp directory for intermediate files used to generate animations')
  parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  args = parser.parse_args()
  
  if args.verbosity > 1:
    print(args)
    
  # image_size = 3264x1836
  image_size = 3264

  # determine platform
  #>>> os.name
  #'nt'
  #>>> import platform
  #>>> platform.system()
  #'Windows'
  #>>> import sys
  #>>> sys.platform
  #'win32'
  if platform.system() == 'Windows':
    convert_exe = ['magick', 'convert']
    identify_exe = ['magick', 'identify']
    infile_list = []
    for i in args.infile_list:
      infile_list += glob.glob(i)
  else:
    convert_exe = ['convert']
    identify_exe = ['identify']
    infile_list = args.infile_list

  if len(infile_list) <= 0:
    # ask for things interactively
    import tkinter
    import tkinter.filedialog
    root = tkinter.Tk()
    infile_list =  tkinter.filedialog.askopenfilenames(initialdir = os.getcwd(), title = "Select files", filetypes = (("jpeg files","*.jpg"), ("all files","*.*")))
    if infile_list is None or len(infile_list) <= 0:
      raise
    else:
      print('infile_list = {}'.format(infile_list))
    
    dstdir = tkinter.filedialog.askdirectory(title = "Select destination directory for pictures")
    if dstdir is None or len(dstdir) <= 0:
      raise
    else:
      print('dstdir = {}'.format(dstdir))
    
#    f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    gif_filename = tkinter.filedialog.asksaveasfilename(defaultextension=".gif")
    if gif_filename is None:
      raise
    else:
      print('gif_filename = {}'.format(gif_filename))
    
    avi_filename = tkinter.filedialog.asksaveasfilename(defaultextension=".avi")
    if avi_filename is None:
      raisev
    else:
      print('avi_filename = {}'.format(avi_filename))
        
    args.gif_filename = gif_filename
    args.avi_filename = avi_filename
    args.gif = True
    args.avi = True
    args.dstdir = dstdir

  print('------------------')
  print('convert_exe = {}'.format(convert_exe))
  print('identify_exe = {}'.format(identify_exe))
  print('------------------')
  for i in infile_list:
    print(i)
  print('------------------')
  
  if not os.path.isdir(args.dstdir):
    os.mkdir(args.dstdir)
  
  pat = re.compile('(.*)(\d\d)(\d\d)(\.jpg)')
  # pat = re.compile('(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)(\.jpg)') # SUNFLOWER HACK
  
  outfile_list = []
  resized_outfile_list = []
  for infile in infile_list:
    s = os.path.basename(infile)
    m = pat.match(s)
  
    if not m:
      print('ERROR: Failed to match pattern.')
      print('s = {}'.format(s))
      print('pat = {}'.format(pat))
      print('m = {}'.format(m))
      raise
    
    base, temperature_integer, temperature_fractional, extension = m.groups()
    # YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, extension = m.groups() # SUNFLOWER HACK
    outfile = os.path.join(args.dstdir, '{}{}{}.annotated{}'.format(base, temperature_integer, temperature_fractional, extension))
    # outfile = os.path.join(args.dstdir, '{}-{}-{}_{}-{}-{}.annotated{}'.format(YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, extension)) # SUNFLOWER HACK
    outfile_list.append(outfile)
    
    caption = '{}.{}°C'.format(temperature_integer, temperature_fractional)
    # caption = '{}-{}-{} {}:{}:{}'.format(YEAR, MONTH, DAY, HOUR, MINUTE, SECOND) # SUNFLOWER HACK

    cmd = identify_exe + ['-format', '%w', os.path.join(os.getcwd(), infile)]
    try:
      ret = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
    except:
      print('The following command failed:')
      print('-----------------------------')
      print(' '.join(cmd))
      print('-----------------------------')
      raise
	
    width = int(ret.stdout)
    
    convert_args = ['-background', '#0008', '-fill', 'white', '-gravity', 'center', '-size' ,'{}x100'.format(width), 'caption:{}'.format(caption), infile, '+swap', '-gravity', 'south', '-composite']
    # convert_args = ['-background', '#0008', '-fill', 'white', '-gravity', 'center', '-size' ,'100x100'.format(width), 'caption:{}'.format(caption), infile, '+swap', '-gravity', 'south', '-composite']
    cmd = convert_exe + convert_args + [outfile]
    
    print('{} -> {}, {}, {}'.format(infile, outfile, caption, width))
    print(' '.join(cmd))
    try:
      ret = subprocess.run(cmd, check=True)
    except:
      print('The following command failed:')
      print('-----------------------------')
      print(' '.join(cmd))
      print('-----------------------------')
      raise
    
    if args.gif:
      if not os.path.isdir(args.tmpdir):
        os.mkdir(args.tmpdir)
      resized_outfile = os.path.join(args.tmpdir, '{}{}{}.annotated{}'.format(base, temperature_integer, temperature_fractional, extension))
      # resized_outfile = os.path.join(args.tmpdir, '{}{}{}.annotated{}'.format(YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, extension)) # SUNFLOWER HACK
      
      resized_outfile_list.append(resized_outfile)
      cmd = convert_exe + ['-resize', '{}%'.format(args.resize)] + convert_args + [resized_outfile]
      
      print('{} -> {}, {}, {}'.format(infile, resized_outfile, caption, width))
      print(' '.join(cmd))
      try:
        ret = subprocess.run(cmd, check=True)
      except:
        print('The following command failed:')
        print('-----------------------------')
        print(' '.join(cmd))
        print('-----------------------------')
        raise
    
  if not(args.not_sorted):
    outfile_list = sorted(outfile_list, reverse=not(args.not_reverse))
    resized_outfile_list = sorted(resized_outfile_list, reverse=not(args.not_reverse))
  
  if args.gif:
    base = 'sunflowers'
    if args.gif_filename:
      gif_filename = args.gif_filename
    else:
      gif_filename = '{}.gif'.format(base)
      # gif_filename = '{}-{}-{}_{}-{}-{}.gif'.format(YEAR, MONTH, DAY, HOUR, MINUTE, SECOND)
    
    print('=====> Creating {}. This might take some time'.format(gif_filename))
    
    # cmd = convert_exe + ['-resize', '{}%'.format(args.resize),'-delay', str(args.delay), '-loop', str(args.loop)] + outfile_list + [gif_filename]
    cmd = convert_exe + ['-delay', str(args.delay), '-loop', str(args.loop)] + resized_outfile_list + [gif_filename]
    if args.verbosity > 1:
      print(' '.join(cmd))
    try:
      ret = subprocess.run(cmd, check=True)
    except:
      print('The following command failed:')
      print('-----------------------------')
      print(' '.join(cmd))
      print('-----------------------------')
      raise
    
    print('=====> Created {}'.format(gif_filename))
  
  if args.avi:
    
    if args.avi_filename:
      avi_filename = args.avi_filename
    else:
      avi_filename = '{}.avi'.format(base)
    
    print('=====> Creating {}. This might take some time'.format(avi_filename))
    
    if not os.path.isdir(args.tmpdir):
      os.mkdir(args.tmpdir)
    for idx, src in enumerate(outfile_list):
      shutil.copyfile(src, os.path.join(args.tmpdir, '{:04d}{}'.format(idx, extension)))
      
    print('args.tmpdir = {}'.format(args.tmpdir))
    
    cmd = ['ffmpeg', '-r', '1', '-i', os.path.join(args.tmpdir, '%04d{}'.format(extension)), '-pix_fmt', 'yuv420p', '-r', '10', avi_filename]
    if args.verbosity > 1:
      print(' '.join(cmd))
    try:
      ret = subprocess.run(cmd, check=True)
    except:
      print('The following command failed:')
      print('-----------------------------')
      print(' '.join(cmd))
      print('-----------------------------')
      raise
    
    print('=====> Created {}'.format(avi_filename))
  
  return 0

if __name__ == '__main__':
  main()
