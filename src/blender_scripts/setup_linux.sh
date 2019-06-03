#!/bin/bash
# TODO: python+GUI version?
# TODO: script should recursively symlink the whole directory tree (maybe just create a directory symlink? but then repo might become a mess, and backups of existing files as well)

set -u

if [ $# -ne 1 ]
then
        echo "usage :"
        echo "  `basename $0` BLENDERPATH"
        echo "Usual paths:"
        echo "  GNU/Linux: ~/.config/blender/ + VERSION"
        exit -1
fi

##########
### PATH_RESOLVER:
# PATH_RESOLVER=${PATH_RESOLVER:-readlink -f}
if [ -z ${PATH_RESOLVER+x} ]
then
  echo "PATH_RESOLVER is unset"
  if which readlink &>/dev/null
  then
    PATH_RESOLVER="readlink -f"
  elif which realpath &>/dev/null
  then
    PATH_RESOLVER="realpath"
  else
    echo "Error: No path resolver found. Need readlink, realpath or equivalent." >&2
    exit -1
  fi
fi

echo "PATH_RESOLVER = ${PATH_RESOLVER}"
if ! ${PATH_RESOLVER} $0 &> /dev/null
then
  echo "Error: path resolution failed. Check PATH_RESOLVER." >&2
  exit -1
fi

### set up variables:
BLENDERPATH=$1
BLENDERSCRIPTDIR=$(dirname "$(${PATH_RESOLVER} "$0")")
PYPATH_TO_ADD=$(dirname ${BLENDERSCRIPTDIR})
CUSTOMPATH=${BLENDERPATH}/scripts/startup/custompath.py
##########
### create symlinks to the various addons
# TODO: enable addons directly

# BLENDERPATH=$HOME/bin/blender-2.56a-beta-linux-glibc27-x86_64/2.56
#BLENDERPATH=$HOME/bin/blender-2.58a-linux-glibc27-x86_64/2.58
#BLENDERPATH=$HOME/bin/blender-2.62-linux-glibc27-i686/2.62
#BLENDERPATH=$HOME/.blender/2.58
#BLENDERPATH=$HOME/.blender/2.63

#SCRIPTSDIR=$HOME/.blender/scripts/
SCRIPTSDIR=${BLENDERPATH}/scripts/addons/
mkdir -p "${SCRIPTSDIR}"

safe_link_dir()
{
  # Usage:
  #   safe_link_dir TARGET DEST
  #
  # Creates a symlink to TARGET (file or directory) in directory DEST.
  # if a file or directory named basename(TARGET) already exists in directory DEST:
  #   -if it is a symlink it will be removed
  #   -else, it will be backed up
  # All removal and moving operations are interactive, unless it is a symlink removal.
  
  if [[ ! $1 ]];then exit 2; fi
  if [[ ! $2 ]];then exit 2; fi

  TARGET="$1"
  DEST="$2"
  
  LINKPATH="$DEST/$(basename $TARGET)"

  if [ ! -d $DEST ]
  then
    echo "ERROR: $DEST does not exist or is not a directory."
    exit 1
  fi

  if [ ! -e $TARGET ]
  then
    echo "ERROR: Target $TARGET not found."
    exit 1
  fi

  BKPSUFFIX=$(date +%Y%m%d_%H%M%S)
  
  # check if target already exists and remove eventually
  if [ -L "$LINKPATH" ] # LINKPATH exists and is a symbolic link (same as -h)
  then
      echo "WARNING: Removing symbolic link $LINKPATH"
      ls -l "$LINKPATH"
      rm -v "$LINKPATH"
  elif [ -f $LINKPATH ]
  then
    echo "WARNING: $LINKPATH already exists and is not a symbolic link, but a regular file."
    ls -l "$LINKPATH"
    cp -iv "$LINKPATH" "$LINKPATH.${BKPSUFFIX}"
    rm -iv "$LINKPATH"
  elif [ -d $LINKPATH ]
  then
    echo "WARNING: $LINKPATH already exists and is not a symbolic link, but a regular directory."
    ls -l "$LINKPATH"
    echo "mv -iv "$LINKPATH" "$LINKPATH.${BKPSUFFIX}" ? (y/n)"
    read ans
    if [ "$ans" = "y" ]
    then
      mv -iv "$LINKPATH" "$LINKPATH.${BKPSUFFIX}"
    fi
  fi

  # link if the file does not exist
  if [ ! -e $LINKPATH ]
  then
    echo "Linking $TARGET" to "$LINKPATH"
    ln -s "$TARGET" "$LINKPATH"
  fi
}

# presets
safe_link_dir "${BLENDERSCRIPTDIR}/presets" "${BLENDERPATH}/scripts/"

# addons
for f in "${BLENDERSCRIPTDIR}/addons/"*.py
do
  echo "Processing $f file...";
  if [ -d $SCRIPTSDIR ]
  then
    safe_link_dir $(${PATH_RESOLVER} "$f") $SCRIPTSDIR
  else
    echo "ERROR: $SCRIPTSDIR does not exist."
  fi
done

##########
### create the custompath.py file to set up the PYTHONPATH for blender

setup_custom_path()
{
PYPATH_TO_ADD="$1"
CUSTOMPATH="$2"

if [ -f ${CUSTOMPATH} ]
then
  echo "WARNING: ${CUSTOMPATH} already exists. Proceed(y/n)?"
  read ans
  case $ans in
  y) echo "Proceeding...";;
  *) exit 1;;
  esac  
fi

mkdir -p $(dirname ${CUSTOMPATH})

cat >${CUSTOMPATH} << EOF
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def register():

  # Note: make sure that all "\" characters in SCRIPT_DIR are doubled, i.e. of the form "\\"
  # example: sys.path.append('C:\\somewhere\\randomdir\\script_inception_public')

  # A simpler alternative is to use the python raw string notation, by simply placing an "r" in front of the string as in the following example:
  # example: sys.path.append(r'C:\somewhere\randomdir\script_inception_public')

  print('Adding script_inception_public path')
  sys.path.append('${PYPATH_TO_ADD}')

  # more specific examples:
  #   to support the argparseui module
  #     sys.path.append(r'C:\Users\USERNAME\Development\argparseui')
  #   to add the path to your non-blender python installation
  #     sys.path.append(r'C:\Users\USERNAME\Development\bin\python34\lib\site-packages')

  # to fix the crash on some systems when trying to auto-complete
  #   bug: https://developer.blender.org/T43491#291613
  #   patch: https://developer.blender.org/D1143
  # alternative: apply patch above to "scripts/modules/console_python.py" in the blender directory
  sys.modules["readline"] = None
  import rlcompleter
  del sys.modules["readline"]

if __name__ == "__main__":
    register()
EOF

chmod +x ${CUSTOMPATH}
}

echo "PYPATH_TO_ADD=${PYPATH_TO_ADD}"
echo "CUSTOMPATH=${CUSTOMPATH}"

echo "Is this correct? (y/n/q)"
read ans
case $ans in
  y) setup_custom_path ${PYPATH_TO_ADD} ${CUSTOMPATH};;
  *) exit 1;;
esac
