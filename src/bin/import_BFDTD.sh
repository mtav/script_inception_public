#!/bin/bash

#PYTHONPATH=:$HOME/opt/lib/python3.3/site-packages/:$HOME/Development/script_inception_public:$HOME/Development/script_inception_private

blender --python $(dirname $0)/../blender_scripts/modules/bfdtd_import.py -- "$@"
#blender --python $BLENDER_USER_SCRIPTS/bfdtd_import.py -- "$@"
