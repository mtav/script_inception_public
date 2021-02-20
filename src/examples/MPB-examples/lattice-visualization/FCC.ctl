(set! resolution 50)

(define a1 (vector3 0   0.5 0.5))
(define a2 (vector3 0.5 0   0.5))
(define a3 (vector3 0.5 0.5 0  ))

(define L1 (/ (vector3-norm a1) ))
(define L2 (/ (vector3-norm a2) ))
(define L3 (/ (vector3-norm a3) ))

(set! geometry-lattice
  (make lattice
    (basis1 a1)
    (basis2 a2)
    (basis3 a3)
    (basis-size L1 L2 L3)
  )
)

(set! geometry (list
  (make sphere
    (center 0 0 0)
    (radius 0.25)
    (material (make dielectric (epsilon 2)) )
  )
))

(set! filename-prefix "FCC-spheres-")
(run)
