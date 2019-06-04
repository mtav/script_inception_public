.. script_inception_public documentation master file, created by
   sphinx-quickstart on Thu Jun 12 12:56:07 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to script_inception_public's documentation!
===================================================

Contents:

.. toctree::
   :maxdepth: 4

   README
   blender_scripts
   blender_help
   FDTD_module
   DLW_module
   FIB_module
   script_inception_public

Matlab tools
============
.. toctree::
   :maxdepth: 4
   
   calculateModeVolume

Writing documentation
=====================

.. toctree::
   :maxdepth: 4

   doc_syntax
   doc_syntax_sphinx_domains
   
.. todolist::

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. comment out the following
  TESTS
  =====   

  These are just some tests. Please disregard.

  .. graph:: foo

     "bar" -- "baz";
     
  .. digraph:: foo

     "bar" -> "baz" -> "quux";

  .. digraph:: foo

     edge [style=dashed,color=red, dir=back];
     "Mesh3D" -> "Multimesh1D" -> "Mesh1D";
     edge [style=solid,color=black, dir=back];
     "Mesh1D" -> {"HomogeneousMesh1D","HeterogeneousMesh1D"};

  .. graphviz::

     digraph foo {
        "bar" -> "baz";
     }

  .. graphviz::

     digraph test123 {
             a -> b -> c;
             a -> {x y};
             b [shape=box];
             c [label="hello\nworld",color=blue,fontsize=24,
                  fontname="Palatino-Italic",fontcolor=red,style=filled];
             a -> z [label="hi", weight=100];
             x -> z [label="multi-line\nlabel"];
             edge [style=dashed,color=red];
             b -> x;
             {rank=same; b x}
     }

  .. graphviz::

     graph test123 {
             a -- b -- c;
             a -- {x y};
             x -- c [w=10.0];
             x -- y [w=5.0,len=3];
     }
