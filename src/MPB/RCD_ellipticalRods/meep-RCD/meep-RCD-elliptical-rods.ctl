(load-from-path "all_FCC_BZ_labels.ctl")

(define n_RCD 1)
(define n_backfill 3)

(define-param w 0.1)
(define-param h 0.2)
(define-param inside-index 4)
(define-param outside-index 2)
(define L (/ (sqrt 3) 4))

(define cylinder_radius (/ w 2))

;; (set! geometry-lattice (make lattice (size 3 3 3)))
(set! geometry-lattice (make lattice (size 1 1 1)))

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
    (tetra -0.25 -0.25 -0.25 cylinder_radius (make medium (index n_RCD)))
    (tetra -0.25  0.25  0.25 cylinder_radius (make medium (index n_RCD)))
    (tetra  0.25 -0.25  0.25 cylinder_radius (make medium (index n_RCD)))
    (tetra  0.25  0.25 -0.25 cylinder_radius (make medium (index n_RCD)))
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

(define rod (car unitcell))

(print rod "\n")
(print (object-property-value rod 'axis) "\n")

(define rod3 (make elliptical-cylinder-RCD
  (center (c->l (/ -1 8) (/ -1 8) (/ -3 8)))
  (axis (c->l -1 -1 -1))
  (size-horizontal w)
  (size-vertical h)
  (height L )
))

(define rod-list (list
  (get_components rod3)
))

(define (RCD-func point-lattice)
  (define inside false)
  (map
    (lambda (rod)
      (if
        (and
          (point-in-periodic-object? point-lattice (list-ref rod 0))
          (point-in-periodic-object? point-lattice (list-ref rod 1))
        )
        (set! inside true)
      )
    )
    ;list of rods to go through
    rod-list
  )
  (if inside
    (make dielectric (index inside-index))
    (make dielectric (index outside-index))
  )
)

(set! default-material (make material-function (material-func RCD-func)))

;; (exit)
;; 
;; (map
;;   (lambda (rod)
;;     (print (object-property-value rod 'axis) "\n")
;;   )
;; 
;;   unitcell
;; ;;   (geometric-objects-lattice-duplicates unitcell
;; ;;     1
;; ;;     1
;; ;;     1
;; ;;   )
;; )
;; 
;; (exit)
(set! geometry (list))

(set! resolution 50)
;; (set! eps-averaging? false)

;; (init-fields) ; for MEEP
;; (output-epsilon)

(init+output-epsilon-mpb)

;; (system* "h5tovtk" "meep-RCD-elliptical-rods-eps-000000.00.h5")
;; (system* "paraview" "meep-RCD-elliptical-rods-eps-000000.00.vtk")

(system* "h5tovtk" "meep-RCD-elliptical-rods-epsilon.h5")
(system* "paraview" "meep-RCD-elliptical-rods-epsilon.vtk")

(exit)
