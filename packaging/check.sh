#!/bin/bash
#WD=$(dirname ${0})

set -eu

ORIGDIR=$(readlink -f "$(dirname ${0})/..")
echo "ORIGDIR: ${ORIGDIR}"

cd ${ORIGDIR}
echo "==> pwd: $(pwd)"

NAME=$(python3 setup.py --name)
CURRENT_VERSION=$(python3 setup.py --version)

VENVDIR=/tmp/testdir/testenv

python3 setup.py sdist bdist_wheel
# source testenv/bin/activate
source ${VENVDIR}/bin/activate
unset PYTHONPATH PYTHONSTARTUP
pip uninstall ${NAME}
pip install --force-reinstall --upgrade ${ORIGDIR}/dist/${NAME}-${CURRENT_VERSION}-py3-none-any.whl
# find ${VENVDIR}/lib/python3.8/site-packages/
cat ${VENVDIR}/lib/python3.8/site-packages/${NAME}-${CURRENT_VERSION}.dist-info/RECORD
