(define-param fcen 2)
(define-param df 1)

;; (set! geometry-lattice (make lattice (size 5 5 no-size)))

;; (set! resolution 50)

(set! sources (list
  (make source
    (src (make gaussian-src (frequency fcen) (fwidth df)))
    (component Hz)
    (center 0 0)
  )
))

(set! pml-layers (list (make pml (thickness 1))))

(run-sources
  (to-appended "hz-probe" (in-point (vector3 0 0) output-hfield-z))
;;   (to-appended "hz-volume" output-hfield-z)
)

;; (in-point pt step-functions...)
