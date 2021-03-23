#!/bin/bash
set -eu

# cd into project directory
cd $(dirname ${0})/..
echo "==> pwd: $(pwd)"

# build and upload to test pypi
#CURRENT_VERSION=$(grep version setup.py | awk -F'"' '{print $2}')
CURRENT_VERSION=$(python3 setup.py --version)
NAME=$(python3 setup.py --name)
echo "==> CURRENT_VERSION=${CURRENT_VERSION}"
# bumpversion --current-version ${CURRENT_VERSION} patch setup.py
python3 setup.py clean --all
# rm -iv dist/*
python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository testpypi dist/*

# check requirements
pkginfo -f requires_dist dist/${NAME}-*.whl

# test package
bash ./packaging/package_test.sh dist/${NAME}-*.whl
