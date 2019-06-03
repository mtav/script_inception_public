(set! geometry-lattice (make lattice (size 16 16 no-size)))

(set! geometry (list
                (make block (center -2 -3.5) (size 12 1 infinity)
                      (material (make dielectric (epsilon 12))))
                (make block (center 3.5 2) (size 1 12 infinity)
                      (material (make dielectric (epsilon 12))))))

(set! pml-layers (list (make pml (thickness 1.0))))
(set! resolution 10)
(run-until 1
           (at-beginning output-epsilon)
           )
