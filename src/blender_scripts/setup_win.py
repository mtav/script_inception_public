#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Setup script for windows.

Possible future alternative options:
  -Bash
  -Windows .bat
  -Powershell
  -NSIS installer (zip2exe based?)
  -.zip files that can be installed in Blender (best option, system independent, standard way, just requires releases instead of only a git repo)

This script might still be useful for a dev environment setup.

Notes:
https://www.howtogeek.com/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/
https://superuser.com/questions/343074/directory-junction-vs-directory-symbolic-link
https://stackoverflow.com/questions/58038683/allow-mklink-for-a-non-admin-user

##### file links
# soft/symbolic
mklink Link Target
# hard
mklink /H Link Target

##### directory links
# soft/symbolic
mklink /D Link Target
# hard
mklink /D /H Link Target

If no admin rights: mklink /j
'''

import os
import argparse
import subprocess
import shlex

def setupAddonsOnWindows(basedir):
    '''
    Sets up the addons for use in Blender on Windows by creating symlinks (junctions) from:
      %USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.6\scripts
    to:
      script_inception_public\src\blender_scripts

    They still need to be manually activated in Blender via the preferences menu. (for now)

    This function also works if the user has no admin rights.
    '''
    basedir = os.path.normpath(basedir)
    print('basedir:', basedir)
    target_script_dir = os.path.realpath(os.path.expanduser(os.path.dirname(__file__)))
    link_script_dir = os.path.join(basedir,'scripts')

    print('target_script_dir:', target_script_dir)
    print('link_script_dir:', link_script_dir)

    for subdir in ['addons', 'modules', 'presets', 'STL-files']:
        target = os.path.join(target_script_dir, subdir)
        link_name = os.path.join(link_script_dir, subdir)
        if not os.path.exists(link_name):
            cmd = ['cmd', '/c', 'mklink', '/J', link_name, target]
            print(shlex.join(cmd))
            subprocess.run(cmd, check=True)
        else:
            print(f'WARNING: {link_name} already exists. Skipping link creation.')
    return

def main():
    '''
    Windows setup script. Main function.
    '''
    parser = argparse.ArgumentParser(description='Script to set up Blender addons on Windows.')
    parser.add_argument('dir', nargs='?', help='Blender configuration directory. Usually of the form: %%APPDATA%%\Blender Foundation\Blender\<VERSION NUMBER>')
    args = parser.parse_args()

    print(args)

    if args.dir is None:
        import tkinter as tk
        import tkinter.filedialog as fd

        root = tk.Tk()
        root.withdraw()
        args.dir = fd.askdirectory(parent=root, initialdir = os.path.join(os.getenv('APPDATA'),'Blender Foundation','Blender'))
        root.destroy()

    print(args.dir)

    if not args.dir:
        parser.print_help()
        return

    setupAddonsOnWindows(args.dir)

if __name__ == '__main__':
    main()
