#!/bin/bash
# setup .bashrc for use with SIP on WSL in Windows 10

set -eu

echo "===================================="
echo "==> Updating and installing packages"
# echo "------------------------------------"
# update & install main packages
sudo apt update
sudo apt upgrade
sudo apt install mpb h5utils python3-numpy python3-matplotlib x11-apps python3-pandas dos2unix tofrodos ack

echo "===================================="
echo "==> Setting up symlink"
# echo "------------------------------------"
# setup symlinks
mkdir --parents ${HOME}/Development

SIP_LINK=${HOME}/Development/script_inception_public

if ( test -e ${SIP_LINK} ) && ( ( ! test -d ${SIP_LINK} ) || ( ! test -L ${SIP_LINK} ) )
then
  echo "--> backing up"
  mv -iv ${SIP_LINK} ${SIP_LINK}.$(date +%Y%m%d_%H%M%S)
fi

if ( ! test -e ${SIP_LINK} )
then
  echo "--> creating symlink"
  ln --symbolic --no-target-directory /mnt/c/Development/script_inception_public ${SIP_LINK}
fi

if ( test -e ${SIP_LINK} ) && ( test -d ${SIP_LINK} ) && ( test -L ${SIP_LINK} )
then
  echo "${SIP_LINK} is now a symlink to the directory: $(readlink -f ${SIP_LINK})"
fi

echo "===================================="
echo "==> Setting up .bashrc"
# echo "------------------------------------"
bashrc_setup_automatic() {
  # back up current .bashrc
  cp --interactive --verbose ${HOME}/.bashrc{,$(date +%Y%m%d_%H%M%S)}

  # append code to current .bashrc
  cat <<EOF >> ${HOME}/.bashrc
##### SIP config #####
if [ -f ${HOME}/Development/script_inception_public/config/.bash_local.generic.sh ]; then
  source ${HOME}/Development/script_inception_public/config/.bash_local.generic.sh
fi
######################
EOF
}

bashrc_setup_instructions() {
  echo "Manual setup instructions:"
  echo "--------------------------"
  echo "Please add the following lines to your ~/.bashrc:"
  echo
  echo "##### SIP config #####"
  echo "if [ -f ${HOME}/Development/script_inception_public/config/.bash_local.generic.sh ]; then"
  echo "  source ${HOME}/Development/script_inception_public/config/.bash_local.generic.sh"
  echo "fi"
  echo "######################"
  echo
  echo "Press enter to continue."
  read ans
}

# setup .bashrc
echo
echo "Setup .bashrc automatically? (y/n)"
read ans
case $ans in
  y|Y|yes) bashrc_setup_automatic;;
  *) bashrc_setup_instructions;;
esac

# echo "==========================="
# echo "==> Reload .bashrc:"
# echo "---------------------------"
# set +eu
# source ${HOME}/.bashrc
# set -eu

# echo "==========================="
# echo "==> Test setup:"
# echo "---------------------------"
# $( dirname "${BASH_SOURCE[0]}" )/test-WSL-setup.sh

# echo
# echo "You can run the following to re-run the test manually:"
# echo "$( dirname "${BASH_SOURCE[0]}" )/test-WSL-setup.sh"
# echo
echo "SUCCESS"
