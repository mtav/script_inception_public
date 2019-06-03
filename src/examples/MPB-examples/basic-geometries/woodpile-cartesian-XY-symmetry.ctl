; woodpile using cartesian lattice

(define-param output_epsilon_only? false) ; if true, exit after outputting epsilon

(define au_microns 1 )

(define-param rod_width (/ 0.240 au_microns) ) ; width of the logs
(define-param rod_height (/ 0.580 au_microns) ) ; height of logs (should be 1/4 for fcc to not overlap)

(define-param interLayerDistance 0.25) ; distance between layers (VerticalPeriod/4)
(define-param interRodDistance 1) ; distance between rods in one layer (horizontal period)

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
(set-param! num-bands 16)

;;;; set up materials
(define-param backfill-index 1 )
(define-param rod-index 1.52 )

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
    (begin
      (list
        (make ellipsoid (material rod-material)
          (center 0 0 0)
          (size rod_width rod_height infinity )
        )
        (make ellipsoid (material rod-material)
          (center 0.5 0.5 0)
          (size rod_width rod_height infinity)
        )
        (make ellipsoid (material rod-material)
          (center 0 0.25 0)
          (size infinity rod_height rod_width)
        )
        (make ellipsoid (material rod-material)
          (center 0 -0.25 0.5)
          (size infinity rod_height rod_width)
        )
      )
    )
)

(define U_B1 (vector3 0 0 1))
(define L_B1 (vector3 (/ (sqrt 0.5) 2) (/ (sqrt 0.5) 2) 0.5))
(define K_B1 (vector3 (sqrt 0.5) (sqrt 0.5) 0))

(define X2_B1 (unit-vector3 1 1 0))
(define Y2_B1 (unit-vector3 0 0 1))
(define Z2_B1 (unit-vector3 1 -1 0))

(define M2to1 (matrix3x3 X2_B1 Y2_B1 Z2_B1))

(define M1to2 (matrix3x3-inverse M2to1))

(define U_B2 (matrix3x3* M1to2 U_B1))
(define L_B2 (matrix3x3* M1to2 L_B1))
(define K_B2 (matrix3x3* M1to2 K_B1))

(define U_B2 (vector3 0 1 0))
(define L_B2 (vector3 0.5 0.5 0))
(define K_B2 (vector3 1 0 0))

(define-param k-interp 9)
(set! k-points (interpolate k-interp (list U_B2 L_B2 K_B2) ))

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
(run-tm)

(exit)
