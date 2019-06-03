#!/bin/bash
blender -P $(dirname $0)/../blender_scripts/io_import_scene_str.py -- "$@"
