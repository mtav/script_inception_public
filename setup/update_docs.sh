#!/bin/bash

# TODO: use https://readthedocs.org/ ?

echo "===> Updating documentation"
# disabling latexpdf because of recursive ref issue
#cd $HOME/Development/script_inception_public/docs && make BUILDDIR=$HOME/isys_git/documentation clean html latexpdf

REPODIR=$(readlink -f "$(dirname "${0}")"/..)
echo ${REPODIR}

cd ${REPODIR}/src/docs && make BUILDDIR=${REPODIR}/docs clean html-without-todo

cd ${REPODIR}/docs
touch .nojekyll

# ln --symbolic html/index.html index.html

cat << EOF > index.html
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Refresh" content="0; url=./html/index.html" />
  </head>
</html>
EOF

# # DOXYGENDOCDIR="$HOME/isys_git/documentation/generated_by_doxygen"
# DOXYGENDOCDIR="$HOME/isys_git/documentation/"
# 
# mkdir -p ${DOXYGENDOCDIR}
# # cd ${DOXYGENDOCDIR} && doxygen ~/Development/script_inception_public/docs/script_inception_public.doxyfile
# cd ${DOXYGENDOCDIR} && doxygen ~/Development/script_inception_public/docs/script_inception_public-absolute-paths.doxyfile
# 
# set +eux
