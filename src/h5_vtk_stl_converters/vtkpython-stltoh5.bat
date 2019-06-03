REM Adapt this file for the various structures you want to convert from stl to h5.

REM usage: stltoh5.py [-h] [-v] [-b BASEPATH]
                  REM [--epsilon_inside EPSILON_INSIDE | --n_inside N_INSIDE]
                  REM [--epsilon_outside EPSILON_OUTSIDE | --n_outside N_OUTSIDE]
                  REM [--basis1 X Y Z] [--basis2 X Y Z] [--basis3 X Y Z]
                  REM [--basis_size BASIS_SIZE BASIS_SIZE BASIS_SIZE]
                  REM [--size SIZE SIZE SIZE] [--Ncells Nx Ny Nz]
                  REM stlfile

REM to print help
REM cmd /k vtkpython.exe stltoh5.py

REM convert .stl file with default arguments
REM cmd /k vtkpython.exe stltoh5.py test.stl

REM cmd /k vtkpython.exe stltoh5.py --size 50 40 30 --Ncells 50 40 30 test.stl

REM cmd /k vtkpython.exe stltoh5.py --size 10 20 30 --basis_size 2 3 4 test.stl

cmd /k vtkpython.exe stltoh5.py --size 5 7 9 --Ncells 250 350 450 --n_inside 2.4 --n_outside 3.5 TT-3-5-7-centered.stl

REM Read in TT-3-5-7-centered.stl, but create mySuperStructure-n2.34-n24.5.h5, etc
REM cmd /k vtkpython.exe stltoh5.py --size 5 7 9 --Ncells 250 350 450 --n_inside 2.4 --n_outside 3.5 -b mySuperStructure-n2.34-n24.5 TT-3-5-7-centered.stl
