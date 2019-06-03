mpb resolution=100 mesh-size=1 w=0.48 h=0.48 inside-index=1 outside-index=2.4 filename-prefix=\"test-\" ellipctical_RCD.ctl | tee test.out

mpb filename-prefix=\"round-\" round_RCD.debug.ctl | tee round_RCD.debug.out
h5tovtk round-epsilon.h5

mpb filename-prefix=\"ellip-\" ellipctical_RCD.debug.ctl | tee ellipctical_RCD.debug.out
h5tovtk ellip-epsilon.h5


mpb filename-prefix=\"ellip-\" ellipctical_RCD.debug.ctl && h5tovtk ellip-epsilon.h5 && paraview ellip-epsilon.vtk

 (set! geometry-lattice (make lattice
                          (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
                          (basis1 0 1 1)
                          (basis2 1 0 1)
                          (basis3 1 1 0)))

mpb ellipctical_RCD.debug.ctl | tee ellipctical_RCD.debug.out

mpb round_RCD.debug.ctl | tee round_RCD.debug.out
