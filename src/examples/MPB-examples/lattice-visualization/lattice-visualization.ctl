(set! resolution 50)

(set! geometry (list
  (make cylinder
    (axis 1 0 0)
    (center 0 -0.5 -0.5)
    (height 1)
    (radius 0.25)
    (material (make dielectric (epsilon 2)) )
  )
  (make cylinder
    (axis 0 1 0)
    (center -0.5 0 -0.5)
    (height 1)
    (radius 0.25)
    (material (make dielectric (epsilon 3)) )
  )
  (make cylinder
    (axis 0 0 1)
    (center -0.5 -0.5 0)
    (height 1)
    (radius 0.25)
    (material (make dielectric (epsilon 4)) )
  )
))

(set! filename-prefix "lattice-cartesian-")
(run)

(define a1 (vector3 0 2 3))
(define a2 (vector3 1 0 3))
(define a3 (vector3 1 2 0))

(define L1 (/ (vector3-norm a1) 2))
(define L2 (/ (vector3-norm a2) 2))
(define L3 (/ (vector3-norm a3) 2))

(set! geometry-lattice
  (make lattice
    (basis1 a1)
    (basis2 a2)
    (basis3 a3)
    (basis-size L1 L2 L3)
  )
)

(set! geometry (list
  (make cylinder
    (axis 1 0 0)
    (center 0 -0.5 -0.5)
    (height L1)
    (radius 0.25)
    (material (make dielectric (epsilon 2)) )
  )
  (make cylinder
    (axis 0 1 0)
    (center -0.5 0 -0.5)
    (height L2)
    (radius 0.25)
    (material (make dielectric (epsilon 3)) )
  )
  (make cylinder
    (axis 0 0 1)
    (center -0.5 -0.5 0)
    (height L3)
    (radius 0.25)
    (material (make dielectric (epsilon 4)) )
  )
))

(set! filename-prefix "lattice-non-cartesian-")
(run)
