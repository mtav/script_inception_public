; woodpile using cartesian lattice

(define-param output_epsilon_only? false) ; if true, exit after outputting epsilon

(define au_microns (* 4 0.900 (- 1 0.5)) )

(define-param rod_width  (/ 0.500 au_microns)) ; width of the logs
(define-param rod_height (/ 0.900 au_microns)) ; height of logs (should be 1/4 for fcc to not overlap)
(define-param interLayerDistance 0.25) ; distance between layers (VerticalPeriod/4)
(define-param interRodDistance (sqrt 0.5)) ; distance between rods in one layer (horizontal period)

(define-param elliptical-rod-shape? true); elliptical rods
;(define-param elliptical-rod-shape? false); rectangular rods

(define overlap (- 1 (/ interLayerDistance rod_height)) )

(define VerticalPeriod (* 4 interLayerDistance))

(set! geometry-lattice (make lattice
  (size
    1
    1
    1
  )
  (basis-size
    interRodDistance
    interRodDistance
    VerticalPeriod
  )
  (basis1 1 0 0)
  (basis2 0 1 0)
  (basis3 0 0 1)
))

;;;; resolution and number of bands
(set-param! resolution 32)
(set-param! num-bands 10)

;;;; set up materials
(define-param backfill-index 1 )
(define-param rod-index 3.6 )
(set! default-material (make dielectric (index backfill-index) ) )
(define rod-material (make dielectric (index rod-index)))

;;;;; print summary of essential parameters
(print "rod aspect ratio h/w = " (/ rod_height rod_width) "\n")
(print "backfill-index = " backfill-index "\n")
(print "rod-index = " rod-index "\n")
(print "w = " rod_width "\n")
(print "h = " rod_height "\n")
(print "dw = " interRodDistance "\n")
(print "dh = " interLayerDistance "\n")
(print "overlap = " overlap "\n")
(print "elliptical-rod-shape? = " elliptical-rod-shape? "\n")

(set! geometry
  (if elliptical-rod-shape?
    (begin
      (list
        (make ellipsoid (material rod-material)
          (center 0.00 0.00 0.00)
          (size rod_width infinity rod_height)
        )
        (make ellipsoid (material rod-material)
          (center 0.00 0.00 0.25)
          (size infinity rod_width rod_height)
        )
        (make ellipsoid (material rod-material)
          (center 0.50 0.00 0.50)
          (size rod_width infinity rod_height)
        )
        (make ellipsoid (material rod-material)
          (center 0.00 0.50 0.75)
          (size infinity rod_width rod_height)
        )
      )
    )
    (begin
      (list
        (make block (material rod-material)
          (center 0.00 0.00 0.00)
          (size rod_width infinity rod_height)
        )
        (make block (material rod-material)
          (center 0.00 0.00 0.25)
          (size infinity rod_width rod_height)
        )
        (make block (material rod-material)
          (center 0.50 0.00 0.50)
          (size rod_width infinity rod_height)
        )
        (make block (material rod-material)
          (center 0.00 0.50 0.75)
          (size infinity rod_width rod_height)
        )
      )
    )
  )
)

(define Gamma (vector3 0   0   0  ))
(define X     (vector3 0.5 0   0  ))
(define Y     (vector3 0   0.5 0  ))
(define Z     (vector3 0   0   0.5))
(define XY    (vector3 0.5 0.5 0  ))
(define YZ    (vector3 0   0.5 0.5))
(define ZX    (vector3 0.5 0   0.5))
(define XYZ   (vector3 0.5 0.5 0.5))

(set! k-points (append
  (list Gamma X XY Y)
  (list Gamma Y YZ Z)
  (list Gamma Z ZX X)
  (list Gamma XY XYZ Z)
  (list Gamma YZ XYZ X)
  (list Gamma ZX XYZ Y)
  (list Gamma)
))

(set! k-points (interpolate 9 k-points))

;; output epsilon.h5 file only
(if output_epsilon_only?
  (begin
    (init-params NO-PARITY true); for MPB
    ;; (init-fields) ; for MEEP
    (output-epsilon)
    (exit)
  )
)

;;;;; run simulation
(run)

(exit)
