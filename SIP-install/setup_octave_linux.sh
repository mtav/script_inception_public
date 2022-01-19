#!/bin/bash
set -eu

safe_link_dir()
{
  if [[ ! $1 ]];then exit 2; fi
  if [[ ! $2 ]];then exit 2; fi

  TARGET="$1"
  DEST="$2"
  FILE="$DEST/$(basename $TARGET)"

  if [ ! -e $TARGET ]
  then
    echo "ERROR: Target $TARGET not found."
    exit 1
  fi

  # check if target already exists and remove eventually
  if [ -L "$FILE" ] # FILE exists and is a symbolic link (same as -h)
  then
      echo "WARNING: Removing symbolic link $FILE"
      ls -l "$FILE"
      rm -v "$FILE"
  else
    if [ -e $FILE ]
    then
      echo "WARNING: $FILE already exists and is not a symbolic link."
      ls -l "$FILE"
      cp -iv "$FILE" "$FILE.$(date +%Y%m%d_%H%M%S)"
      rm -iv "$FILE"
    fi
  fi

  # link if the file does not exist
  if [ ! -e $FILE ]
  then
    echo "Linking $TARGET"
    ln --symbolic "$TARGET" "$FILE"
  fi
}

OCTAVERC=$(readlink -f $(dirname ${0})/../config/.octaverc)
echo "OCTAVERC : ${OCTAVERC}"

echo "Creating symlink to .octaverc in: ${HOME}"
# ln --symbolic --target-directory="${HOME}" "${OCTAVERC}"
safe_link_dir "${OCTAVERC}" "${HOME}"

SNAPDIR="${HOME}/snap/octave/current"
echo "Creating symlink to .octaverc in: ${SNAPDIR}"
if test -d "${SNAPDIR}"
then
  # ln --symbolic --target-directory="${SNAPDIR}" "${OCTAVERC}"
  safe_link_dir "${OCTAVERC}" "${SNAPDIR}"
  read -p "Enable removable media access in snap for Octave? (y/n): " ans
  if test "${ans}" = "y"
  then
    sudo snap connect octave:removable-media  :removable-media
    sudo snap connections octave
  fi
fi
