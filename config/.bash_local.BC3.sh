#!/bin/bash

##########################################################
##### Environment setup

##################
# PATH
##################

export PATH=$PATH:$HOME/bin

export PATH=$HOME/opt/bin:$PATH
# export PATH=$PATH:$HOME/opt/bin

export PATH=$HOME/opt/usr/bin:$PATH
# export PATH=$PATH:$HOME/opt/usr/bin

# where python packages and others install their binaries:
export PATH=${PATH}:${HOME}/.local/bin

export PATH=$PATH:$HOME/bin/public_bin
export PATH=$PATH:$HOME/bin/community_bin

export PATH=$PATH:$HOME/Development/script_inception_public/src/bin
export PATH=$PATH:$HOME/Development/script_inception_public/src/bin/hacks
export PATH=$PATH:$HOME/Development/script_inception_public/src/geometries
export PATH=$PATH:$HOME/Development/script_inception_public/src/h5_vtk_stl_converters

##################
# PYTHON
##################
export PYTHONSTARTUP=$HOME/.pystartup
#export PYTHONPATH=$PYTHONPATH:$HOME/opt/lib/python3.3/site-packages/
#export PYTHONPATH=$PYTHONPATH:${MODULE_PREFIX}/opt/lib/python3.3/site-packages/
export PYTHONPATH=$PYTHONPATH:$HOME/Development/script_inception_public/src

# export PYTHONPATH=$PYTHONPATH:$HOME/opt/lib/python3.4/site-packages/

##################
# GUILE
##################
export GUILE_LOAD_PATH=$HOME/Development/script_inception_public/src/MPB/library:.
export GUILE_WARN_DEPRECATED=no
### for guile experts
# export GUILE_WARN_DEPRECATED=detailed

##################
# MISC
##################
export PROMPTSTYLE=3
# export MATLABPATH=$HOME/MATLAB
export SIP_PATH=${HOME}/Development/script_inception_public/src/
export MATLABPATH=${SIP_PATH}
#export MODULEPATH=$MODULEPATH:$HOME/modulefiles

export CPATH=/cm/shared/libraries/gnu_builds/hdf5-1.8.12/include/

##########################################################
##### Modules for working on bluecrystal

##### Important notes:

### "module" does not return error on failure unfortunately making success checks problematic

### apps/meep-1.2.1-mpi
# libraries/gnu_builds/h5utils-1.12.1 must be loaded after apps/meep-1.2.1-mpi, else
# /usr/mpi/gcc/mvapich2-1.7-qlc/bin/mpirun
# will be used instead of
# /usr/mpi/gcc/mvapich-1.2.0-qlc/bin/mpirun
#
# /usr/mpi/gcc/mvapich2-1.7-qlc/bin/mpirun leads to this error:
# PMGR_COLLECTIVE ERROR: unitialized MPI task: Missing required environment variable: MPIRUN_RANK

### apps/python-meep-1.3
# requires libraries/gnu_builds/gsl-1.16
# works with: /cm/shared/apps/openmpi/gcc/64/1.6.5/bin/mpirun

### apps/matlab-r2015a
# This module will break git HTTPS pull/push because it changes libcurl from:
# /usr/lib64/libcurl.so.4
# to:
# /cm/shared/apps/Matlab-R2015a/bin/glnxa64/libcurl.so.4

loadgit() {
  ### git
  LATEST_GIT=$(module avail 2>&1 | grep git | sort | tail -1)
  module load ${LATEST_GIT}
  # module unload apps/matlab-r2015a
  # module load tools/git-1.8.4.2
  # module load tools/git-1.7.9
  # module load tools/git-2.18.0
  # module load tools/git-2.22.0
}

loadmatlab() {
  LATEST_MATLAB=$(module avail 2>&1 | grep matlab | sort | tail -1)
  module load ${LATEST_MATLAB}
  # module load apps/matlab-r2015a
  # module load apps/matlab-r2013a
  # module load apps/matlab-r2013b
  # module load matlab-R2014a-x86_64
  # module load apps/matlab-R2009a
}

unloadmatlab() {
  if module list 2>&1 | grep matlab >/dev/null
  then
    MATLAB_MODULE=$(module list 2>&1 | grep matlab | awk '{print $2}')
    module unload ${MATLAB_MODULE}
  fi
}

loadModules() {
  # TODO: As suggested by admin McCallum: should load modules in job scripts instead, to reduce loaded things and conflicts... + maybe add load utilities for CLI convenience

  # mpb
  module load apps/mpb-1.5-mpi

  ### for qsub, qstat, etc
  # module load shared default-environment
  module load torque/4.2.4.1 moab/7.2.9 # same as previous, but does not load dot (which adds . to PATH)

  ### required for python-meep
  module load libraries/gnu_builds/gsl-1.16
  # module load gnu_builds/gsl-1.13
  # module load gnu_builds/gsl

  ### for meep
  module load apps/python-meep-1.3 # loads different mpirun!!!
  # module load apps/meep-1.2.1-mpi
  # module load apps/meep-1.2-mpi
  # module load meep-mpi
  # module load apps/meep-mpi

  ### h5utils
  module load libraries/gnu_builds/hdf5-1.8.12
  module load libraries/gnu_builds/h5utils-1.12.1
  # module load gnu_builds/h5utils

  ### python
  module load languages/python-3.7.7
  # module load languages/python-3.3.2
  # module load languages/python-2.7.10
  # module load languages/python-2.7.6-sklearn
  # module load languages/python-2.7.6
  # module load languages/python-2.7.5
  # module load languages/python-2.7.2
  # module load languages/python-2.7
  # module load languages/python-2.6.8

  ### paraview
  module load apps/paraview-4.3.1
  # module load apps/paraview-4.0.1
  # module load apps/paraview-3.8

  ### misc
  # module load apps/phylobayes-4.1-serial-gsl
  # module load apps/phylobayes-3.3f-serial-gsl

  # module load languages/fpc-2.4.0

  # module load gnu_builds/hdf5.mpi

  # module load mpiexec/0.84_432
  # module load tools/mpiexec-0.84
  # module load mvapich/gcc/64/1.2.0-qlc

  # module load shared torque moab
  # module load libraries/gnu_builds/atlas-3.10.1
  
  ### load most recent matlab
  # loading matlab changes the curl library to one not supporting https, which prevents the use of git
  loadmatlab

  ### load most recent git
  loadgit

  ### custom modules
  module load bfdtd
  module load photonics-shared-binaries
}

loadBC3config()
{
#   echo "Loading BC3 config"
  alias git='git.sh'
}

if declare -f module >/dev/null
then
  loadModules &> /dev/null
fi

case $(hostname) in
  newblue*) loadBC3config;;
#   bigblue*) export PPN=8;;
#   bluecrystal*) export PPN=4;;
#   babyblue*) export PPN=4;;
#   *) export PPN=1;;
esac

##########################################################
##### reference info

#case $(hostname) in
# bigblue*) export PPN=8;;
# bluecrystal*) export PPN=4;;
# babyblue*) export PPN=4;;
# *) export PPN=1;;
#esac

#BC1:
#92 nodes each with two dual-core Opteron processors, memory 8 GB RAM per node (2 GB per core)
#ppn=4
#2GB/core
#8GB/node

#BC2:
#416 nodes each with 2 x 2.8 GHz 4 core Intel Harpertown E5462 processors, memory 8 GB RAM per node (1GB per core), 193GB scratch space on /local
#ppn=8
#1GB/core
#8GB/node

#BC3:
#223 base blades which have 16 x 2.6Hz SandyBridge cores, 4GB/core and a 1TB SATA disk.
#ppn=16
#4GB/core
#64GB/node

# 360 hours
# export TORQUE_QUEUE=long

# 120 hours
# export TORQUE_QUEUE=short

# export PPN=1
# export PPN=2
# export PPN=16

### queues:
# testq              --      --    01:00:00   --    1   3 --   E R
# veryshort          --      --    12:00:00   --  223 1703 --   E R
# short              --      --    120:00:0   --  108 1051 --   E R
# medium             --      --    240:00:0   --   58  18 --   E R
# long               --      --    360:00:0   --   88 123 --   E R

# Windows 10 WSL specific configuration
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null ; then
    #echo "Windows 10 Bash"
	export DISPLAY=:0.0
#else
#    echo "Anything else"
fi
