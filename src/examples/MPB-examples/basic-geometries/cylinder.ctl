(set! geometry-lattice (make lattice
                        (basis1 0 1 1)
                        (basis2 1 0 1)
                        (basis3 1 1 0)
                        (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
                        (size 1 1 1)
))

(set-param! resolution 100)

(set! geometry (list
  (make cylinder
    (material (make dielectric (index 2)))
    (center 0 0 0)
    (radius 0.1)
    ;; This part is problematic because the norm can only be calculated correctly in an orthonormal basis, but the input points might be defined in any basis.
    ;; (height (vector3-norm (vector3- B A)) )
    (height 0.5)
    (axis (cartesian->lattice (vector3 0 0 1)))
  )
))

(run)
