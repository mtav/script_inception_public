#!/bin/bash

### To use this file, add the following to your ~/.bashrc:
# if [ -f ${HOME}/Development/script_inception_public/config/.bash_local.generic.sh ]; then
#   source ${HOME}/Development/script_inception_public/config/.bash_local.generic.sh
# fi

##########################################################
##### Environment setup
export SIP_PATH=${HOME}/Development/script_inception_public/src/

##################
# PATH
##################

export PATH=$PATH:$HOME/bin

export PATH=$HOME/opt/bin:$PATH
# export PATH=$PATH:$HOME/opt/bin

export PATH=$HOME/opt/usr/bin:$PATH

# where python packages and others install their binaries:
export PATH=${PATH}:${HOME}/.local/bin

export PATH=$PATH:$HOME/bin/public_bin
export PATH=$PATH:$HOME/bin/community_bin

export PATH=$PATH:${SIP_PATH}/bin
export PATH=$PATH:${SIP_PATH}/bin/hacks
export PATH=$PATH:${SIP_PATH}/geometries
export PATH=$PATH:${SIP_PATH}/h5_vtk_stl_converters

##################
# PYTHON
##################
export PYTHONSTARTUP=$HOME/.pystartup
export PYTHONPATH=$PYTHONPATH:${SIP_PATH}

##################
# GUILE
##################
export GUILE_LOAD_PATH=${SIP_PATH}/MPB/library:.
export GUILE_WARN_DEPRECATED=no
### for guile experts
# export GUILE_WARN_DEPRECATED=detailed

##################
# MISC
##################
export PROMPTSTYLE=3
export MATLABPATH=${SIP_PATH}

##########################################################

# Windows 10 WSL specific configuration
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null ; then
    #echo "Windows 10 Bash"
	export DISPLAY=:0.0
#else
#    echo "Anything else"
fi
