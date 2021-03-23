This directory contains and example to plot the energy distribution within a DBR stack with cavities of varying refractive index values (3, 3.5 and 4).

Usage:
  # Optional cleanup removing data files
  rm -fv *.h5 *.vtk *.out *.dat
  
  # Simply run this to generate all .vtk files
  ./main_wrapper.sh
  
Then open paraview and load the MPB-1D-pillar-defect.pvsm state, choosing "Search files under specified directory" and setting the data directory to the directory containing this file (or more specifically the VTK files).
