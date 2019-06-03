(define n_RCD 1)
(define n_backfill 3)

(define rx 0.2)
(define ry 0.2)

(set! geometry-lattice (make lattice (size 3 3 3)))

(define (tetra x y z R mat)
  (list
    (make cylinder
      (material mat)
      (center (vector3 (- x (/ 1 8)) (- y (/ 1 8)) (- z (/ 1 8))))
      (radius R)
      (height (/ (sqrt 3) 4))
      (axis (vector3 -1 -1 -1))
    )
    (make cylinder
      (material mat)
      (center (vector3 (- x (/ 1 8)) (+ y (/ 1 8)) (+ z (/ 1 8))))
      (radius R)
      (height (/ (sqrt 3) 4))
      (axis (vector3 -1  1  1))
    )
    (make cylinder
      (material mat)
      (center (vector3 (+ x (/ 1 8)) (- y (/ 1 8)) (+ z (/ 1 8))))
      (radius R)
      (height (/ (sqrt 3) 4))
      (axis (vector3  1 -1  1))
    )
    (make cylinder
      (material mat)
      (center (vector3 (+ x (/ 1 8)) (+ y (/ 1 8)) (- z (/ 1 8))))
      (radius R)
      (height (/ (sqrt 3) 4))
      (axis (vector3  1  1 -1))
    )
  )
)

(define unitcell
  (append
    (tetra -0.25 -0.25 -0.25 rx (make medium (index n_RCD)))
    (tetra -0.25  0.25  0.25 rx (make medium (index n_RCD)))
    (tetra  0.25 -0.25  0.25 rx (make medium (index n_RCD)))
    (tetra  0.25  0.25 -0.25 rx (make medium (index n_RCD)))
  )
)

(set! geometry
  (append
    (list
      (make block
        (material (make medium (index n_backfill)) )
        (center (vector3 0 0 0) )
        (size (vector3 1 1 1) )
        (e1 (vector3 1 0 0))
        (e2 (vector3 0 1 0))
        (e3 (vector3 0 0 1))
      )
    )
    (geometric-objects-lattice-duplicates unitcell
      1
      1
      1
    )
  )
)

(set! resolution 50)
(set! eps-averaging? false)

(init-fields) ; for MEEP
(output-epsilon)

(system* "h5tovtk" "meep-RCD-normal-rods-eps-000000.00.h5")
(system* "paraview" "meep-RCD-normal-rods-eps-000000.00.vtk")

(exit)
