This is an example showing how to visualize 3D data.

The CTL file runs a source in vacuum and saves the Ez field values in two different ways:
1) To one HDF5 file per time slice. Data format: XYZ
2) To a single HDF5 file for all time slices. Data format: XYZT

Three different ways of visualizing the data are presented:
1) Converting each time slice HDF5 file to VTK and then opening them as a group in Paraview after renaming them.
2) Doing the same, but using the single XYZT HDF5 file.
3) Creating images and a GIF from the single XYZT HDF5 file using a slice through the central Z layer.

To run it, you can use the run.sh script and then the postprocess-single-h5.sh script to postprocess the single HDF5 file.

On Windows, you can use the PowerRename tool to rename all files so they can be opened as a group in Paraview:
https://docs.microsoft.com/en-us/windows/powertoys/
