#!/bin/bash
# run an MPB simulation and plot the results to test if everything is setup correctly.
#
# Note: Xming is required for X11 graphical applications on WSL. However, it requires configuring the Windows firewall if you are using WSL2.
# More infos here:
#   https://github.com/microsoft/WSL/issues/4139
#   https://github.com/cascadium/wsl-windows-toolbar-launcher/blob/master/README.md#troubleshooting
#
# Due to this, this script will only test image generation instead of opening plotting windows.
#
# Extra info for running matplotlib without an Xserver:
#   https://www.delftstack.com/howto/matplotlib/how-to-save-plots-as-an-image-file-without-displaying-in-matplotlib/
#   https://stackoverflow.com/questions/4931376/generating-matplotlib-graphs-without-a-running-x-server
#   https://stackoverflow.com/questions/2801882/generating-a-png-with-matplotlib-when-display-is-undefined
#   https://matplotlib.org/faq/howto_faq.html#matplotlib-in-a-web-application-server

set -eu

# test path setup
bash ${HOME}/Development/script_inception_public/src/testing/test_guile_load_path.sh

# test MPB plotting setup
TESTDIR=$(mktemp -d)
cd ${TESTDIR}

OUTFILE="test.out"

mpb_wrapper.py --workdir='.' --outfile=${OUTFILE} k-interp=5 resolution=10 num-bands=3 ${HOME}/Development/script_inception_public/src/examples/MPB-examples/RCD/RCD.ctl
MPB_parser.py --saveas "test" ${OUTFILE} plot --y-range-auto --x-range-auto --no-show

echo "====="
echo "Output can be found in ${TESTDIR}"
# https://superuser.com/questions/1113385/convert-windows-path-for-windows-ubuntu-bash
echo "On Windows, go to $(wslpath -w ${TESTDIR})"
echo "====="
echo "SUCCESS"
