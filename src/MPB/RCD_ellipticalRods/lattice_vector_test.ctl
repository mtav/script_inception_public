; generate some test files for the h5/VTK python scripts

(define u (vector3 -1 2 3))
(define v (vector3 4 -5 6))
(define w (vector3 7 8 -9))
(set! geometry-lattice (make lattice (basis-size (vector3-norm u) (vector3-norm v) (vector3-norm w)) (basis1 u) (basis2 v) (basis3 w)))
(run)
