#!/bin/bash
# setup .bashrc for use with SIP on WSL in Windows 10

set -eu

# update & install main packages
sudo apt update
sudo apt install mpb h5utils python3-numpy python3-matplotlib x11-apps python3-pandas dos2unix tofrodos ack

# setup symlinks
mkdir --parents ~/Development
ln -s /mnt/c/Development/script_inception_public ~/Development/script_inception_public

# setup .bashrc
cp --interactive --verbose ${HOME}/.bashrc{,$(date +%Y%m%d_%H%M%S)}

cat <<EOF >> ${HOME}/.bashrc

##### SIP config #####
source /mnt/c/Development/script_inception_public/config/.bash_local.BC3.sh
######################
EOF

echo "SUCCESS"
