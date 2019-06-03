#!/bin/bash

#PYTHONPATH=:/space/ANONYMIZED/home_rama/opt/lib/python3.3/site-packages/:/space/ANONYMIZED/home_rama/Development/script_inception_public:/space/ANONYMIZED/home_rama/Development/script_inception_private

blender -P $(dirname $0)/../blender_scripts/modules/GWL_import.py -- "$@"
#blender -P $BLENDER_USER_SCRIPTS/GWL_import.py -- "$@"
