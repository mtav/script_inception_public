README
======

What this is
------------
Useful scripts for MEEP, MPB, Bristol FDTD, Nanoscribe, FIB and other stuff.

The idea is to centralize scripts used by almost everyone to reduce code duplication and therefore errors and time wasting, as well as improve the overall quality of code over time.

License
-------
Unless otherwise specified inside a file or folder, everything is under GPLv3 (cf COPYING.txt).

The following (written by Ian Buss) are under the LGPL:

* Bris2Meep

* Postprocessor

* Geo2Str

Windows setup:
--------------

#. Find out if you have Windows 32bit or 64bit: Settings -> System -> About -> System type

   .. note::
     You can also just press the "Windows" key and type in "about" to access it faster.
  
#. Recommended: View "File name extensions" and "Hidden items":
   Open "File explorer" -> View tab -> Check "File name extensions" and "Hidden items"

#. Install Git for Windows (distributed version control system):

   http://git-scm.com/downloads

   .. note::
     It is available in the Windows 10 Software centre.

#. Install pathman, included in the "Windows Server 2003 Resource Kit Tools":

   https://www.microsoft.com/en-us/download/details.aspx?id=17657 (NOT available in the Windows 10 Software centre)

#. Download and run the following script: `SIP-install/SIP-install.bat <https://github.com/mtav/script_inception_public/raw/master/SIP-install/SIP-install.bat>`_.

#. Optional:

  #. Install notepad++: https://notepad-plus-plus.org/ (available in Windows 10 Software centre)
    
  #. Install FreeCAD: https://www.freecadweb.org/ (NOT available in Windows 10 Software centre)
  
  #. Install python 3: https://www.python.org/ (NOT available in Windows 10 Software centre)
  
  #. Install imagemagick: https://imagemagick.org/script/download.php#windows (available in Windows 10 Software centre)
  
  #. Install Octave: https://www.gnu.org/software/octave (NOT available in Windows 10 Software centre)
  
  #. Install Matlab: Matlab: https://www.mathworks.com/products/matlab.html (available in Windows 10 Software centre)

  #. Install Tortoise git (for integration of git in windows explorer): https://code.google.com/p/tortoisegit/wiki/Download

Blender setup:
--------------
#. Install Blender: https://www.blender.org/ (NOT available in Windows 10 Software centre)

#. See the instructions here for the latest up to date installation instructions: `Blender setup instructions <../../src/blender_scripts/README.md>`_

Deprecated information:
~~~~~~~~~~~~~~~~~~~~~~~
#. In Blender:

  * File -> User preferences -> Addons ->Install from file...
  * Navigate to ``C:\Development\script_inception_public\src\blender_scripts\addons``
  * Select the script to install
  * Check box next to script
  * Save user settings

Links
-----
For more info: https://wikis.bris.ac.uk/display/Photonics/Public+scripts+repository

Other useful links/tools
~~~~~~~~~~~~~~~~~~~~~~~~
* Blender documentation: http://wiki.blender.org/
* Python 3 documentation: http://docs.python.org/py3k/
* Git documentation: http://git-scm.com/documentation
* Pyscripter: https://code.google.com/p/pyscripter/
* Notepad++: http://www.notepad-plus-plus.org/
* Tortoise git: https://code.google.com/p/tortoisegit/

Directories for the installation
--------------------------------
Directories that will be used:

* *SCRIPT_DIR*: This will be where you placed the scripts from this repository.
  ex: ``H:\script_inception_public``

* *BLENDER_DIR*: Here you can choose your Blender installation directory (for system-wide availability) or the user-specific Blender directory (created after first running Blender):

  * For a system-wide install:

    * Windows XP: ``C:\Program Files\Blender Foundation\Blender\2.63``
    * Windows Vista/7: ``C:\Program Files\Blender Foundation\Blender\2.63``

  * For a user-specific install:

    * Windows XP:

      * For Blender 2.6x: ``C:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\2.63``
      * For Blender 2.49: ``C:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\.blender``

    * Windows Vista/7: ``C:\Users\USERNAME\AppData\Roaming\Blender Foundation\Blender\2.63``

* *PYTHONDIR*: Where your python 3 installation is located.
  ex: ``C:\Python32``

Notes
~~~~~
* The paths might be slightly different on your system, so adapt as necessary.

* If you do not have admin rights, don't worry. You can get installers or .zip packages for all the necessary software, except numpy. For numpy, you can install it somewhere else where you have admin rights and then just copy the numpy folder from there. :)

* The "Application Data" folder may be hidden. To unhide it: http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/win_fcab_show_file_extensions.mspx?mfr=true_ +

* The .py extensions may be hidden. You can unhide them in a way similar to showing hidden folders. Uncheck the "Mask known file extensions" somewhere.

Matlab/Octave scripts
---------------------
To effectively use the Matlab/Octave scripts from this repository, you should add the paths to your Matlab/Octave path.

#. First of all, edit *startup.m* by setting *PUBLIC_REPO_DIR* to the directory where you placed the repository, i.e. *SCRIPT_DIR*::

    % Adapt those settings according to your setup and where you placed the repository
    PUBLIC_REPO_DIR = SCRIPT_DIR;

#. Then follow one of the following two sections depending on whether you use Matlab or Octave:

If you use Matlab
~~~~~~~~~~~~~~~~~
For Matlab, there are several ways to do this. Choose one of the following options:

* Copy *startup.m* from the repository into your Matlab startup folder (you can find out what it is by running *userpath()* in Matlab). Restart Matlab and it should run the startup.m script and recursively add the necessary folders.
* Add the repository recursively in Matlab: *File->Set path...->Add with subfolders...*, select the repository, then *Save*.
* If you don't use any startup script already, you can also simply add just the repository folder *File->Set path...->Add folder...*, select the repository, then *Save*. Matlab will then use the startup script from the repository.
* Edit your own *startup.m* appropriately.

To test if it works, you can run *get_c0()* for example or *postprocessor()*.

.. note::
  You can also set up the environment variable *MATLABPATH* to define the Matlab search path.

If you use Octave
~~~~~~~~~~~~~~~~~
Under GNU/Linux::

  ln -s $PATH_TO_REPO/.octaverc ~/.octaverc 

Documentation
-------------

This HTML documentation was automatically generated using *Sphinx*.

Git repository location
-----------------------

Public repository:

  * https://github.com/mtav/script_inception_public

Private repository:

  * git@git.assembla.com:script_inception_private.git (currently not up to date)

Windows directories
-------------------

* Blender user-specific startup script directory: ``C:\Users\USERNAME\AppData\Roaming\Blender Foundation\Blender\2.72\scripts\startup``

Requirements
------------
* For Blender import/export scripts:

  * python > v3
  * blender > v2.6 (> v2.71 at least required for multi-STL export)

* For python scripts offering GUIs:

  * PyQt5
  * argparseui for PyQt5

* For python scripts using VTK:

  * python > v2.7
  * vtk > v6.1.0

* For generating documentation:

  * Sphinx (for python3, simultaneous documentation generation of both python 2 and 3 scripts is a bit problematic at the moment)

* Other required python modules for both python 2 and 3:

  * numpy
  * h5py

Example python paths
--------------------
You can check your python path with the following commands in an interactive python session::

  >>> import sys
  >>> sys.path

For an easier to read/use version::

  >>> import sys
  >>> for i in sys.path: print(i)

* Example Python3 path on a GNU/Linux system::

    ~/.config/blender/2.71/scripts/addons
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/scripts/addons
    ~/.config/blender/2.71/scripts/startup
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/scripts/startup
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/scripts/modules
    ~/opt/lib/python3.4/site-packages/h5py-2.3.1-py3.4-linux-x86_64.egg
    ~/opt/lib/python3.4/site-packages/Sphinx-1.2.3-py3.4.egg
    ~/opt/lib/python3.4/site-packages/Jinja2-2.7.3-py3.4.egg
    ~/opt/lib/python3.4/site-packages/docutils-0.12-py3.4.egg
    ~/opt/lib/python3.4/site-packages/Pygments-1.6-py3.4.egg
    ~/opt/lib/python3.4/site-packages/MarkupSafe-0.23-py3.4-linux-x86_64.egg
    ~/opt/lib/python3.4/site-packages/youtube_dl-2014.10.13-py3.4.egg
    ~/WORK/Desktop
    ~/opt/lib/python3.4/site-packages
    ~/Development/script_inception_public
    ~/Development/script_inception_private
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/python/lib/python34.zip
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/python/lib/python3.4
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/python/lib/python3.4/plat-linux
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/python/lib/python3.4/lib-dynload
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/python/lib/python3.4/site-packages
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/scripts/freestyle/modules
    ~/bin/blender-2.71-linux-glibc211-x86_64/2.71/scripts/addons/modules
    ~/.config/blender/2.71/scripts/addons/modules
    ~/opt/lib/python3.4/site-packages
    ~/Development/script_inception_public

Creating VTK files from BFDTD .prn files for 3D visualization
-------------------------------------------------------------
This is still a work in progress, but for the impatient:

#. In matlab: run *prnToh5_allSnapshots* in the data directory.
#. In cygwin 32 bit::

    h5tovtk -d log_energy  -o log_energy.vtk energy.h5 && h5tovtk -d epsilon  -o epsilon.vtk energy.h5 && h5tovtk -d energy  -o energy.vtk energy.h5

#. in paraview: load the created .vtk files

Conversion between the HDF, VTK and PRN formats
-----------------------------------------------

The scripts related to h5/vtk/prn conversion are in:

* *script_inception_public/h5_vtk_stl_converters*

They are:

* **h5tovts.py** -> convert from HDF5 to a VTK structured grid
* **stltoh5.py** -> create an h5 file from an STL file for use with the **epsilon-input-file** function in MEEP/MPB
* **prntovts.py** -> convert BFDTD output to the h5 and VTK formats (unfinished, work in progress)

**h5tovts.py** and **stltoh5.py** print out some help if used without args.

I haven't had time to document everything yet, but hopefully it's
understandable enough at the moment.

Density of states plotting
---------------------------

For density of states plotting, check out:

* examples/MPB-examples/dos.scm
* third_party/MPB_utilities/

