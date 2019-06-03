#!/bin/bash

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
