(set! geometry-lattice (make lattice (size 5 3 3)))

(define motif
    (list
      (make sphere
        (center 0 0 0)
        (material (make dielectric (epsilon 12)))
        (radius 0.1)
      )
    )
)

;; (set! geometry 
;;   (append
;;     (geometric-objects-lattice-duplicates 
;;     motif
;;     0.5)
;;     (list
;;       (make sphere
;;         (center 0.75 0 0)
;;         (material (make dielectric (epsilon 12)))
;;         (radius 0.2)
;;       )
;;     )
;;   )
;; )

(set! geometry
  (geometric-objects-duplicates (vector3 0.5 0 0) -1 1
    (geometric-objects-duplicates (vector3 0 0.5 0) -1 2
      (geometric-objects-duplicates (vector3 0 0 0.5) -2 2 motif)
    )
  )
)

(run-until 1
           (at-beginning output-epsilon)
)
