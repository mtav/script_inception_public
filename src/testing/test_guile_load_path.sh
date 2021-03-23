#!/bin/bash
set -eu

if [ -z ${GUILE_LOAD_PATH+x} ]
then
  echo "GUILE_LOAD_PATH is unset."
  exit -1
else
  echo "GUILE_LOAD_PATH is set to '${GUILE_LOAD_PATH}'"
fi

TMPDIR=$(mktemp -d )
echo "TMPDIR = ${TMPDIR}"

cd ${TMPDIR}

cat <<EOF >test_guile_load_path.ctl
(load-from-path "MPB_woodpile_FCT.ctl")
(load-from-path "all_FCC_BZ_labels.ctl")
(exit)
EOF

mpb test_guile_load_path.ctl

echo "GUILE_LOAD_PATH configured correctly."

cd -
