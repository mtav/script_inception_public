Setup on GNU/Linux:
-------------------
Run setup_linux.sh

Setup on Windows:
-----------------
Run this python script from the repository:

```
script_inception_public\src\blender_scripts\setup_win.py
```

It will ask you to select your Blender APPDATA directory. Simply select the Blender version for which you want to set up the addons.

It does the setup by:
* creating junctions in the appropriate subdirectory, i.e.: `%APPDATA%\Blender Foundation\Blender\%VERSION%\scripts`,
* and creating a **custompath.py** startup script in `%APPDATA%\Blender Foundation\Blender\%VERSION%\scripts\startup`

Old deprecated Blender 2.49 setup information:
----------------------------------------------

To use these scripts in Blender:

* On Windows: Place them into the following directory:

  * C:\Documents and Settings\$USER\Application Data\Blender Foundation\Blender\.blender\scripts
 
* Or on newer Windows versions (Windows 10 and later):

  * C:\Users\$USER\AppData\Roaming\Blender Foundation\Blender\2.93\scripts

```
$ cygpath "C:\Users\$USERNAME\AppData\Roaming\Blender Foundation\Blender\2.93\scripts"
/c/Users/${USERNAME}/AppData/Roaming/Blender Foundation/Blender/2.93/scripts
```

* On GNU/Linux: Place them into the following directory:
  * ~/.blender/scripts/
  * I recommend creating a symlink to the scripts in the checked out repository instead. That way you can update it easily with "git pull". :)


Considerations for possible Blender-BFDTD system redesign:
----------------------------------------------------------
How the import currently works:
* open and parse file to create BFDTDobject
* loop through those objects and depending on their type call the appropriate blender-dependent function to add them (they are all methods of the FDTDGeometryObjects class)

What we should probably do:
* get rid of all those type-specific geolists in BFDTDobject (or write corresponding getter functions)
* get number of different materials used in the BFDTDobject
* add the usual materials (probes, snapshots, etc)
* add the geo object materials
* functions to add new FDTD objects in blender should become operators like bpy.ops.mesh.primitive_cube_add()
* they will define custom  ID-Properties for the object
* a permanent FDTD panel will be added to blender via addon, which will alow seeing and editing the properties of the object, updating the object in the 3D view as well.
* editing the object in the 3D view will update the ID-properties as well
