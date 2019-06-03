IMPORTANT NOTE:
Due to some concerns about what to release and what not to release publically, this repository is no longer always updated. :(
The most up to date version is now on the shared internal "K: drive".

I will try to "cherry-pick" some commits to push if possible (or once enough has been published or the PhD is done, just push everything (provided the big boss is happy with it as well)).
In the meanwhile, if you are interested, just contact me directly.
We now have some more Blender import/export/add mesh scripts for the Nanoscribe GWL language among other things.

script_inception_public documentation
=====================================
:backend: html5
:theme: flask
:toc2:
:icons:
:data-uri:
:pygments:
:toclevels: 4

What this is
------------
Useful scripts for MEEP and Bristol FDTD and maybe other stuff. :)

The idea is to centralize scripts used by almost everyone to reduce code duplication and therefore errors and time wasting, as well as improve the overall quality of code over time.

License
-------
Unless otherwise specified inside a file or folder, everything is under GPLv3 (cf COPYING.txt).

The following (written by Ian Buss) are under the LGPL:

* Bris2Meep

* Postprocessor

* Geo2Str

Links
-----
For more info: https://wikis.bris.ac.uk/display/Photonics/Public+scripts+repository

Other useful links/tools
~~~~~~~~~~~~~~~~~~~~~~~~
- Blender documentation: http://wiki.blender.org/
- Python 3 documentation: http://docs.python.org/py3k/
- Git documentation: http://git-scm.com/documentation
- Pyscripter: https://code.google.com/p/pyscripter/
- Notepad++: http://www.notepad-plus-plus.org/
- Tortoise git: https://code.google.com/p/tortoisegit/

Directories for the installation
--------------------------------
Directories that will be used:

- *SCRIPT_DIR*: This will be where you placed the scripts from this repository. +
ex: H:\script_inception_public

- *BLENDER_DIR*: Here you can choose your Blender installation directory (for system-wide availability) or the user-specific Blender directory (created after first running Blender): +
 * For a system-wide install:
 ** Windows XP: 'C:\Program Files\Blender Foundation\Blender\2.63'
 ** Windows Vista/7: 'C:\Program Files\Blender Foundation\Blender\2.63'
 * For a user-specific install:
 ** Windows XP:
 *** For Blender 2.6x: 'C:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\2.63'
 *** For Blender 2.49: 'C:\Documents and Settings\USERNAME\Application Data\Blender Foundation\Blender\.blender'
 ** Windows Vista/7: 'C:\Users\USERNAME\AppData\Roaming\Blender Foundation\Blender\2.63'

- *PYTHONDIR*: Where your python 3 installation is located. +
ex: 'C:\Python32'

Notes
~~~~~
- The paths might be slightly different on your system, so adapt as necessary.

- If you do not have admin rights, don't worry. You can get installers or .zip packages for all the necessary software, except numpy. For numpy, you can install it somewhere else where you have admin rights and then just copy the numpy folder from there. :)

- The "Application Data" folder may be hidden. To unhide it: http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/win_fcab_show_file_extensions.mspx?mfr=true_ +

- The .py extensions may be hidden. You can unhide them in a way similar to showing hidden folders. Uncheck the "Mask known file extensions" somewhere.

Blender scripts
---------------

Installation HOWTO
~~~~~~~~~~~~~~~~~~

I still need to make it a bit more user-friendly, but to install it, here's what you have to do (tested on Windows XP and Vista/Windows 7):

Windows install with Blender 2.6+
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*Because there isn't any numpy 64-bit installer at the moment, it is best to install 32-bit versions of everything.*

. Install Blender 2.6+ (32bit) +
http://www.blender.org/download/get-blender/

. Install python 3 (32bit) +
http://www.python.org/download/releases/3.2.3/

. Install numpy 1.6.2 (32bit) for python 3.2 +
http://sourceforge.net/projects/numpy/files/NumPy/1.6.2/

. Copy *PYTHONDIR\Lib\site-packages\numpy* into *BLENDER_DIR\scripts\modules*

. Create a file named 'custompath.py' in *BLENDER_DIR\scripts\startup* with the following in it (create directories as necessary):
+

----
#!/usr/bin/env python3
import sys +
#Note: make sure that all "\" characters in SCRIPT_DIR are doubled, i.e. of the form "\\" +
#ex: sys.path.append('C:\\somewhere\\randomdir\\script_inception_public')
sys.path.append('SCRIPT_DIR')
----
+
. Download and extract the latest version of the repository to *SCRIPT_DIR*: https://github.com/mtav/script_inception_public/archives/master +
_Note: You can also checkout/clone the repository using git, which is a much better option, and will allow you to easily update it. Try https://code.google.com/p/tortoisegit/[TortoiseGit] for an easy way to do this for example. It will also allow you to push changes back to the repository, should you wish to contribute code. ;)_

. Create the directory *BLENDER_DIR\scripts\addons* if it does not exist.

. Copy *SCRIPT_DIR\blender_scripts\io_import_scene_bfdtd.py* into *BLENDER_DIR\scripts\addons*

. Copy *SCRIPT_DIR\blender_scripts\io_import_scene_gwl.py* into *BLENDER_DIR\scripts\addons*

. Start Blender, go to File->User preferences->Addons and enable the addons.

You can use 'Help->Toggle system console' for debugging in case of problems.

Windows install with Blender 2.49
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The import scripts have all been updated for Blender 2.6x and will not work with older versions.
But you may still find the following instructions useful if you want to use the Blender caliper and layer manager scripts (which have not been ported yet) with Blender 2.49:

. Install python 2.6 (normally, there is a bundled package with blender+python, but apparently they only keep it for the latest stable release): +
http://www.python.org/download/releases/2.6.6/

. Install numpy from: +
http://sourceforge.net/projects/numpy/files/NumPy/1.6.1/numpy-1.6.1-win32-superpack-python2.6.exe/download

. Install blender 2.49b (so, not the latest version, but I'll try to fix that later. The problem is that the latest blender version uses python 3 instead of python 2.6) +
http://download.blender.org/release/Blender2.49b/blender-2.49b-windows.exe

. Download and extract the latest version of the repository to *SCRIPT_DIR*: https://github.com/mtav/script_inception_public/archives/master

. Copy all the .py files from *SCRIPT_DIR\blender_scripts* into *BLENDER_DIR\scripts* +
_Note: The .py extensions may be hidden, but just copy all the contents of the folder. The other files shouldn't cause problems._

. Copy the file *SCRIPT_DIR\blender_scripts\.B.blend* into *BLENDER_DIR* +
_Note: This is just to set up a nicer default workspace, so it is optional. You can save your workspace as the default at any time in Blender with *File->Save default settings*._

. Define the following environment variables (cf http://support.microsoft.com/kb/310519 for how to do this) :

* *DATADIR = H:\* (or whatever else you want to use as the default import directory. It does not matter much, since the import script will store the last directory you imported from. I am going to change it so this variable is not mandatory anymore)
* *PYTHONPATH = SCRIPT_DIR* (Use the folder you chose in step 4)

Ok, you are now ready to import BFDTD files with blender.

Example filestructure after installation
++++++++++++++++++++++++++++++++++++++++
*SCRIPT_DIR*\addpath_recurse +
*SCRIPT_DIR*\README.html +
... +
*BLENDER_DIR*\.B.blend +
*BLENDER_DIR*\scripts\FDTDGeometryObjects.py +
...

Usage instructions
^^^^^^^^^^^^^^^^^^

. Start blender

. *File->Import->BristolFDTD (.geo,.inp,.in)* or *File->Import->GWL (.gwl)*

. Search for .geo,.inp,.in or .gwl files and import them (Tip: In Blender 2.49, middle-click on a file opens it)

Other blender scripts
~~~~~~~~~~~~~~~~~~~~~

1) Layer manager (not yet ported to python3/blender 2.6x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It makes it easier to show/hide the diverse components of the BFDTD files. +
To use it, in the "scripts window" (On the right if you copied .B.blend from the repository as your default workspace), click on *Scripts->System->Layer manager*.

2) Blender caliper (not yet ported to python3/blender 2.6x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To show dimensions, etc, you can use the blender caliper script. +
To use it, in the "scripts window" (On the right if you copied .B.blend from the repository as your default workspace), click on *Scripts->Wizards->Blender caliper*.

Notes on the python 3 port (Work in progress)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
On Ubuntu 10.04 and maybe other old distributions, it may be necessary to install python, numpy and blender from source.
Some scripts still need to be ported, but BFDTD and GWL import in Blender works.

Useful links
^^^^^^^^^^^^

* http://blenderartists.org/forum/showthread.php?233753-adding-3rd-party-modules
* http://www.blender.org/download/source-code/
* http://wiki.blender.org/index.php/Dev:2.5/Doc/Building_Blender/Linux/Ubuntu/CMake

Quick guide
^^^^^^^^^^^

. Install python 3.2 from source with $HOME/opt as prefix for example (*./configure --prefix=$PREFIX*)
. Configure the environment with:
+
----
export PYTHONPATH=$PYTHONPATH:$HOME/opt/lib/python3.2/site-packages/
export PYTHONPATH=$PYTHONPATH:$HOME/Development/script_inception_public
export LD_LIBRARY_PATH=$HOME/opt/lib:$LD_LIBRARY_PATH
----
+
. Install blender from source: configure the PYTHON variables in cmake correctly so they point to your python installation
. Install numpy from source with the same prefix as before: *python setup.py install --prefix=$PREFIX*
. Run setup_linux.sh
. Start Blender and go to *File->User preferences->Addons*, search for the BFDTD import script and enable it.
. Now you should be able to import BFDTD files through *File->Import->Import BFDTD*

Matlab/Octave scripts
---------------------
To effectively use the Matlab/Octave scripts from this repository, you should add the paths to your Matlab/Octave path. +

. First of all, edit *startup.m* by setting *PUBLIC_REPO_DIR* to the directory where you placed the repository, i.e. *SCRIPT_DIR*:
+
----
    % Adapt those settings according to your setup and where you placed the repository
    PUBLIC_REPO_DIR = SCRIPT_DIR;
----
+
. Then:

If you use Matlab
~~~~~~~~~~~~~~~~~
For Matlab, there are several ways to do this. Choose one of the following options:

* Copy *startup.m* from the repository into your Matlab startup folder (you can find out what it is by running *userpath()* in Matlab). Restart Matlab and it should run the startup.m script and recursively add the necessary folders.
* Add the repository recursively in Matlab: *File->Set path...->Add with subfolders...*, select the repository, then *Save*.
* If you don't use any startup script already, you can also simply add just the repository folder *File->Set path...->Add folder...*, select the repository, then *Save*. Matlab will then use the startup script from the repository.
* Edit your own *startup.m* appropriately.

To test if it works, you can run *get_c0()* for example or *postprocessor()*.

_Note: You can also set up the environment variable *MATLABPATH* to define the Matlab search path._

If you use Octave
~~~~~~~~~~~~~~~~~
Under GNU/Linux:
----
ln -s $PATH_TO_REPO/.octaverc ~/.octaverc 
----

Private repository:
-------------------
git@git.assembla.com:script_inception_private.git

Notes:
------

For density of states plotting, check out:

* examples/MPB-examples/dos.scm
* third_party/MPB_utilities/
