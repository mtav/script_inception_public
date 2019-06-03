#!/bin/bash
# converts filenames to lowercase
# same as: rename 'y/A-Z/a-z/' *
# But rename does not work correctly on bluecrystal...
# Not sure why "expr" was used before. "echo" is simpler and seems to work as well.
for f in *; do
  #g=`expr "$f" : '\(.*\)' | tr '[A-Z]' '[a-z]'`
  g=`echo "$f" | tr '[A-Z]' '[a-z]'`
  mv -v "$f" "$g"
done
