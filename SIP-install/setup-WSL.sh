#!/bin/bash
# setup .bashrc for use with SIP on WSL in Windows 10

set -eu

# update & install main packages
sudo apt update
sudo apt install mpb h5utils python3-numpy python3-matplotlib x11-apps python3-pandas dos2unix tofrodos ack

# setup symlinks
mkdir --parents ~/Development
ln --symbolic /mnt/c/Development/script_inception_public ~/Development/script_inception_public

bashrc_setup_automatic() {
  # back up current .bashrc
  cp --interactive --verbose ${HOME}/.bashrc{,$(date +%Y%m%d_%H%M%S)}

  # append code to current .bashrc
  cat <<EOF >> ${HOME}/.bashrc
##### SIP config #####
source /mnt/c/Development/script_inception_public/config/.bash_local.BC3.sh
######################
EOF
}

bashrc_setup_instructions() {
  echo "Please add the following lines to your ~/.bashrc:"
  echo "##### SIP config #####"
  echo "source /mnt/c/Development/script_inception_public/config/.bash_local.BC3.sh"
  echo "######################"
}

# setup .bashrc
echo "Setup .bashrc automatically? (y/n)"
read ans
case $ans in
  y|Y|yes) bashrc_setup_automatic;;
  *) bashrc_setup_instructions;;
esac

echo "SUCCESS"
