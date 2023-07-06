#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##### Draft/notes for a setup script for windows. Python? Bash? Windows .bat? Powershell? or NSIS? Or just .zip files that can be installed in Blender? (best option, system independent, standard way, just requires releases instead of only a git repo)
##### Script might still be useful for dev environment setup.

raise
#########################
TODO: create setup script for windows, with Tk GUI to select directory...

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

%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.6\scripts

mkdir "%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.6\scripts"
mklink /D Link %USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.6\scripts
mklink "%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.6\scripts" "%USERPROFILE%\Development\script_inception_public\src\blender_scripts\addons"

##### Current working solution
# (Works in cmd.exe, but not powershell. Does not require admin rights.)
mklink /J "%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.6\scripts\addons" "%USERPROFILE%\Development\script_inception_public\src\blender_scripts\addons"
mklink /J "%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.6\scripts\modules" "%USERPROFILE%\Development\script_inception_public\src\blender_scripts\modules"
mklink /J "%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.6\scripts\presets" "%USERPROFILE%\Development\script_inception_public\src\blender_scripts\presets"
mklink /J "%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.6\scripts\STL-files" "%USERPROFILE%\Development\script_inception_public\src\blender_scripts\STL-files"

#########################
Basic procedure:
copy all folders from:
  script_inception_public\src\blender_scripts
to:
  %APPDATA%\Blender Foundation\Blender\3.2\scripts
#########################
set -eu

BLENDERSCRIPTDIR="$HOME/Application Data/Blender Foundation/Blender/.blender/scripts"
SCRIPTS="\
bfdtd_parser.py \
bfdtd_import.py \
bfdtd_export.py \
meep_parser.py \
meep_import.py \
meep_export.py \
bfdtd_meep_export.py"

function BlenderScriptDir_to_repo()
{
    echo "BlenderScriptDir->repo"
    for f in $SCRIPTS
    do
        echo "-> $f"
        if diff "$BLENDERSCRIPTDIR/$f" "./$f";
        then
            echo "No differences. Skipping.";
        else
            echo "Differences found.";
            cp -iv "$BLENDERSCRIPTDIR/$f" ".";
        fi
    done
}

function repo_to_BlenderScriptDir()
{
    echo "repo->BlenderScriptDir";
    for f in $SCRIPTS
    do
        echo "-> $f"
        if diff "$f" "$BLENDERSCRIPTDIR/$f";
        then
            echo "No differences. Skipping.";
        else
            echo "Differences found.";
            cp -iv "$f" "$BLENDERSCRIPTDIR";            
        fi
    done
}

function diff_files()
{
    echo "diffing files";
    for f in $SCRIPTS
    do
        echo "-> $f"
        diff "$f" "$BLENDERSCRIPTDIR/$f";
    done
}

echo "0=BlenderScriptDir->repo / 1=repo->BlenderScriptDir / 2=diff repo BlenderScriptDir"
read ans
case $ans in
  0) BlenderScriptDir_to_repo;;
  1) repo_to_BlenderScriptDir;;
  2) diff_files;;
  *) echo "Unknown option";;
esac
