#!/bin/bash
# fix filenames and convert links to text files so that rsync to RDS (Windows NTFS drives?) works

DIR=${1:-.}
echo "Processing ${DIR}"

find . -name "*:*" -exec rename 's|:|_colon_|g' {} \;
find . -name "*>*" -exec rename 's|>|_greater-than_|g' {} \;
find . -name "*<*" -exec rename 's|<|_less-than_|g' {} \;
find . -name "*\?*" -exec rename 's|\?|_questionmark_|g' {} \;
find . -name '*`*' -exec rename 's|`|_backquote_|g' {} \;
find . -name '*\\*' -exec rename 's|\\|_backslash_|g' {} \;
find . -name "*£*"  -exec rename 's|£|_unicode_|g' {} \;

# convmv -r -f windows-1252 -t UTF-8 .
# convmv --notest -r -f windows-1252 -t UTF-8 .
# https://serverfault.com/questions/348482/how-to-remove-invalid-characters-from-filenames
