#!/bin/bash
set -eu

ORIGDIR=$(readlink -f "$(dirname ${0})/..")
echo "ORIGDIR: ${ORIGDIR}"

WHL=$(readlink -f ${1})
echo "Testing ${WHL}"

# test package
# TESTDIR=$(mktemp -d )
TESTDIR=/tmp/testdir
mkdir -p ${TESTDIR}
echo ${TESTDIR} > ${ORIGDIR}/packaging/package_test.log
cd ${TESTDIR}
echo "==> pwd: $(pwd)"
# virtualenv testenv
source testenv/bin/activate
unset PYTHONPATH PYTHONSTARTUP
# pip install -U -i https://test.pypi.org/simple/ photonics
# directly install the wheel
echo "WHL: ${WHL}"
pip install -U ${WHL}
# python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps photonics
# python3 -c "import photonics"
# python3 -c "import code; import readline; import rlcompleter; import bfdtd; code.interact(local=locals())"
python3 ${ORIGDIR}/packaging/package_test.py
