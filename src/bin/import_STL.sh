#!/bin/bash
blender --python $(dirname $0)/../blender_scripts/addons/io_mesh_stl/stl_utils.py -- "$@"
