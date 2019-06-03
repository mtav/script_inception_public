# system setup:
# install the latest miniconda:
https://conda.io/miniconda.html
https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

# choose a prefix:
CONDA_PREFIX=${HOME}/miniconda/

# install miniconda
bash miniconda.sh -b -p ${CONDA_PREFIX}
bash Miniconda3-latest-Linux-x86_64.sh -b -p ${CONDA_PREFIX}

# add the path to PATH
export PATH=${CONDA_PREFIX}/bin:$PATH

# create a python environment with pymeep
conda create -n mp -c chogan -c conda-forge pymeep

# running scripts:
export PATH=$HOME/miniconda/bin:$PATH
source activate mp
