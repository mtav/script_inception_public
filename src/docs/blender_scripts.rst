Blender scripts
===============

The various available Blender addons are located in **script_inception_public/blender_scripts/addons/**.
They require Blender version > v2.7.

Once you have the python path of your Blender Python installation correctly set up, you can install them from within Blender via:
**File->User preferences...->Addons->Install from File...**

Scripts which are not yet meant for use, will show a warning sign on the right.

Setting up the Blender Python path:
-----------------------------------
Create a file named 'custompath.py' in *BLENDER_DIR\\scripts\\startup* with the following in it (create directories as necessary)::

    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-

    import sys

    def register():
    
      # Note: make sure that all "\" characters in SCRIPT_DIR are doubled, i.e. of the form "\\"
      # example: sys.path.append('C:\\somewhere\\randomdir\\script_inception_public')
      
      # A simpler alternative is to use the python raw string notation, by simply placing an "r" in front of the string as in the following example:
      # example: sys.path.append(r'C:\somewhere\randomdir\script_inception_public')

      print('Adding script_inception_public path')
      sys.path.append('SCRIPT_DIR')
      
      # more specific examples:
      #   to support the argparseui module
      #     sys.path.append(r'C:\Users\USERNAME\Development\argparseui')
      #   to add the path to your non-blender python installation
      #     sys.path.append(r'C:\Users\USERNAME\Development\bin\python34\lib\site-packages')

    if __name__ == "__main__":
        register()

Usage instructions
-------------------

#. Start blender

#. *File->Import->BristolFDTD (.geo,.inp,.in)* or *File->Import->GWL (.gwl)*

#. Search for .geo,.inp,.in or .gwl files and import them (Tip: In Blender 2.49, middle-click on a file opens it)

Notes on the python 3 port
--------------------------
On Ubuntu 10.04 and maybe other old distributions, it may be necessary to install python, numpy and blender from source.
Some old useful scripts like the layer manager and Blender caliper still need to be ported.

Not yet ported Blender scripts
```````````````````````````````

1) Layer manager (not yet ported to python3/blender 2.6x)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

It makes it easier to show/hide the diverse components of the BFDTD files. +
To use it, in the "scripts window" (On the right if you copied .B.blend from the repository as your default workspace), click on *Scripts->System->Layer manager*.

2) Blender caliper (not yet ported to python3/blender 2.6x)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

To show dimensions, etc, you can use the blender caliper script. +
To use it, in the "scripts window" (On the right if you copied .B.blend from the repository as your default workspace), click on *Scripts->Wizards->Blender caliper*.

Old installation HOWTO
----------------------

I still need to make it a bit more user-friendly, but to install it, here's what you have to do (tested on Windows XP and Vista/Windows 7):

Windows install with Blender 2.6+
``````````````````````````````````
*Because there isn't any numpy 64-bit installer at the moment, it is best to install 32-bit versions of everything.*

#. Install Blender 2.6+ (32bit):
   http://www.blender.org/download/get-blender/

#. Install python 3 (32bit):
   http://www.python.org/download/releases/3.2.3/

#. Install numpy 1.6.2 (32bit) for python 3.2:
   http://sourceforge.net/projects/numpy/files/NumPy/1.6.2/

#. Copy *PYTHONDIR\\Lib\\site-packages\\numpy* into *BLENDER_DIR\\scripts\\modules*

#. Create a file named 'custompath.py' in *BLENDER_DIR\\scripts\\startup* with the following in it (create directories as necessary)::

    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-

    import sys

    def register():
    
      # Note: make sure that all "\" characters in SCRIPT_DIR are doubled, i.e. of the form "\\"
      # example: sys.path.append('C:\\somewhere\\randomdir\\script_inception_public')
      
      # A simpler alternative is to use the python raw string notation, by simply placing an "r" in front of the string as in the following example:
      # example: sys.path.append(r'C:\somewhere\randomdir\script_inception_public')

      print('Adding script_inception_public path')
      sys.path.append('SCRIPT_DIR')
      
      # more specific examples:
      #   to support the argparseui module
      #     sys.path.append(r'C:\Users\USERNAME\Development\argparseui')
      #   to add the path to your non-blender python installation
      #     sys.path.append(r'C:\Users\USERNAME\Development\bin\python34\lib\site-packages')

    if __name__ == "__main__":
        register()




#. Download and extract the latest version of the repository to *SCRIPT_DIR*: https://github.com/mtav/script_inception_public/archives/master

   .. note::
     You can also checkout/clone the repository using git, which is a much better option, and will allow you to easily update it. Try https://code.google.com/p/tortoisegit/[TortoiseGit] for an easy way to do this for example. It will also allow you to push changes back to the repository, should you wish to contribute code. ;)

#. Create the directory *BLENDER_DIR\\scripts\\addons* if it does not exist.

#. Copy *SCRIPT_DIR\\blender_scripts\\io_import_scene_bfdtd.py* into *BLENDER_DIR\\scripts\\addons*

#. Copy *SCRIPT_DIR\\blender_scripts\\io_import_scene_gwl.py* into *BLENDER_DIR\\scripts\\addons*

#. Start Blender, go to File->User preferences->Addons and enable the addons.

You can use 'Help->Toggle system console' for debugging in case of problems.

Windows install with Blender 2.49
``````````````````````````````````

The import scripts have all been updated for Blender 2.6x and will not work with older versions.
But you may still find the following instructions useful if you want to use the Blender caliper and layer manager scripts (which have not been ported yet) with Blender 2.49:

#. Install python 2.6 (normally, there is a bundled package with blender+python, but apparently they only keep it for the latest stable release):
   http://www.python.org/download/releases/2.6.6/

#. Install numpy from:
   http://sourceforge.net/projects/numpy/files/NumPy/1.6.1/numpy-1.6.1-win32-superpack-python2.6.exe/download

#. Install blender 2.49b (so, not the latest version, but I'll try to fix that later. The problem is that the latest blender version uses python 3 instead of python 2.6):
   http://download.blender.org/release/Blender2.49b/blender-2.49b-windows.exe

#. Download and extract the latest version of the repository to *SCRIPT_DIR*:
   https://github.com/mtav/script_inception_public/archives/master

#. Copy all the .py files from *SCRIPT_DIR\\blender_scripts* into *BLENDER_DIR\\scripts*

   .. note::
     The .py extensions may be hidden, but just copy all the contents of the folder. The other files shouldn't cause problems.

#. Copy the file *SCRIPT_DIR\\blender_scripts\\.B.blend* into *BLENDER_DIR*

   .. note::
     This is just to set up a nicer default workspace, so it is optional. You can save your workspace as the default at any time in Blender with *File->Save default settings*.

#. Define the following environment variables (cf http://support.microsoft.com/kb/310519 for how to do this) :

* *DATADIR = H:\\* (or whatever else you want to use as the default import directory. It does not matter much, since the import script will store the last directory you imported from. I am going to change it so this variable is not mandatory anymore)
* *PYTHONPATH = SCRIPT_DIR* (Use the folder you chose in step 4)

Ok, you are now ready to import BFDTD files with blender.

Example filestructure after installation
'''''''''''''''''''''''''''''''''''''''''

* *SCRIPT_DIR*\\addpath_recurse
* *SCRIPT_DIR*\\README.html
* ...
* *BLENDER_DIR*\\.B.blend
* *BLENDER_DIR*\\scripts\\FDTDGeometryObjects.py
* ...

Quick guide
````````````

#. Install python 3.2 from source with $HOME/opt as prefix for example (*./configure --prefix=$PREFIX*)
#. Configure the environment with::

    export PYTHONPATH=$PYTHONPATH:$HOME/opt/lib/python3.2/site-packages/
    export PYTHONPATH=$PYTHONPATH:$HOME/Development/script_inception_public
    export LD_LIBRARY_PATH=$HOME/opt/lib:$LD_LIBRARY_PATH

#. Install blender from source: configure the PYTHON variables in cmake correctly so they point to your python installation
#. Install numpy from source with the same prefix as before: *python setup.py install --prefix=$PREFIX*
#. Run setup_linux.sh
#. Start Blender and go to *File->User preferences->Addons*, search for the BFDTD import script and enable it.
#. Now you should be able to import BFDTD files through *File->Import->Import BFDTD*

Useful links
------------

* http://blenderartists.org/forum/showthread.php?233753-adding-3rd-party-modules
* http://www.blender.org/download/source-code/
* http://wiki.blender.org/index.php/Dev:2.5/Doc/Building_Blender/Linux/Ubuntu/CMake
