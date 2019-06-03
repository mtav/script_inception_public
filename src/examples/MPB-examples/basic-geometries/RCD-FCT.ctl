;;;; FCT-RCD geometry

;;;; resolution and number of bands
(set-param! resolution 32)
(set-param! num-bands 10)

;;;; dimensions of the cubic unit-cell
(define-param _a (sqrt 2) )
(define-param _b (sqrt 2) )
(define-param _c (sqrt 2) ) ; FCC if _c = _a = _b to BCC if _c = _a/sqrt(2) = _b/sqrt(2)

;;;; sets geometry-lattice and canonical FCC-BZ labels based on given _a,_b,_c parameters
(load-from-path "all_FCT_BZ_labels.ctl")

;;;; set up k-point list
(define-param k-interp 9)
(set! k-points (interpolate k-interp FCC_standard_kpoints))
;; (set! k-points (list))

;;;; set up materials
(define-param backfill-index 1 )
(define-param rod-index (sqrt 9.9) )
(set! default-material (make dielectric (index backfill-index) ) )
(define rod-material (make dielectric (index rod-index)))

;;;; set up rod shape and size
;; (define-param elliptical-rod-shape? true); elliptical rods
(define-param elliptical-rod-shape? false) ; circular rods, in which case the width is used as diametre
(define-param w 0.365 ) ; width of the rods
(define-param h (* 1.27 _c w) ) ; height of rods

(if (not elliptical-rod-shape?)
  (set! h w) ; height of rods
)

;;;;; print summary of essential parameters
(print "_a = " _a "\n")
(print "_b = " _b "\n")
(print "_c = " _c "\n")
(print "rod aspect ratio h/w = " (/ h w) "\n")
(print "backfill-index = " backfill-index "\n")
(print "rod-index = " rod-index "\n")
(print "w = " w "\n")
(print "h = " h "\n")
(print "elliptical-rod-shape? = " elliptical-rod-shape? "\n")

;;;;; set up geometry

; point definitions in FCC lattice coordinates
;; (define p000 (vector3 0 0 0))
(define p000 (vector3 -0.125 -0.125 -0.125))
;; (define p000 (vector3 -0.5 -0.5 -0.5))
(define p100 (vector3+ p000 (vector3 1 0 0)) )
(define p010 (vector3+ p000 (vector3 0 1 0)) )
(define p001 (vector3+ p000 (vector3 0 0 1)) )
(define pmid (vector3+ p000 (vector3 0.25 0.25 0.25)) )

(define (cylinder_from_A_to_B A B r mat)
  (make cylinder
    (material mat)
    (center (vector3* 0.5 (vector3+ A B)) )
    (radius r)
    (height (vector3-norm (lattice->cartesian (vector3- B A))) )
    (axis (vector3- B A) )
  )
)

(set! geometry
  (if elliptical-rod-shape?
    (begin
      (print "Error: Not yet implemented.\n")
      (exit)
    )
    (begin
      (list
        (cylinder_from_A_to_B pmid p000 (* 0.5 w) rod-material)
        (cylinder_from_A_to_B pmid p100 (* 0.5 w) rod-material)
        (cylinder_from_A_to_B pmid p010 (* 0.5 w) rod-material)
        (cylinder_from_A_to_B pmid p001 (* 0.5 w) rod-material)
      )
    )
  )
)

;;;;; create a custom prefix for output files
(set-param! filename-prefix
  (string-append
    "RCD-FCT"
    "_c-" (number->string _c)
    "_"
  )
)

;;;;; run simulation
(run)
