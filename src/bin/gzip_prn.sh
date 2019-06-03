#!/bin/bash
# gzip .prn files in given directories (current directory by default)
# It could be defined as an alias, but this way, it does not pollute the bash config.
find "$@" -type f -name "*.prn" -exec gzip {} \;
