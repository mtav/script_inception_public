;;;; FCT-woodpile geometry

;; cf fig5.1 on p64 in ~/WORK/references/Theses/Nanoscribe-theses/thesis - 2011 - Isabelle Philippa Staude - Functional Elements in Three-Dimensional Photonic Bandgap Materials.pdf

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
;; (set! k-points (interpolate k-interp FCC_standard_kpoints))
(set_kpoints FCC_standard_kpoints)
;; (set! k-points (list))

;;;; set up materials
(define-param backfill-index 1 )
(define-param rod-index (sqrt 9.9) )
(set! default-material (make dielectric (index backfill-index) ) )
(define rod-material (make dielectric (index rod-index)))

;;;; set up rod shape and size
(define-param elliptical-rod-shape? true); elliptical rods
;(define-param elliptical-rod-shape? false); rectangular rods
(define-param w 0.365 ) ; width of the logs
(define-param h (* 1.27 _c w) ) ; height of logs (should be h = _c/4 to just touch)

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
(define rod1_center (c->l (*  0     _a) (*  0     _b) (*  0     _c)))
(define rod1_e1     (c->l (*  1     _a) (*  1     _b) (*  0     _c)))
(define rod1_e2     (c->l (*  1     _a) (* -1     _b) (*  0     _c)))
(define rod1_e3     (c->l (*  0     _a) (*  0     _b) (*  1     _c)))

(define rod2_center (c->l (*  0.125 _a) (*  0.125 _b) (*  0.250 _c)))
(define rod2_e1     (c->l (*  1     _a) (*  1     _b) (*  0     _c)))
(define rod2_e2     (c->l (*  1     _a) (* -1     _b) (*  0     _c)))
(define rod2_e3     (c->l (*  0     _a) (*  0     _b) (*  1     _c)))

(set! geometry
  (if elliptical-rod-shape?
    (begin
      (list
        (make ellipsoid (material rod-material)
          (center rod1_center)
          (e1 rod1_e1)
          (e2 rod1_e2)
          (e3 rod1_e3)
          (size infinity w h))
        (make ellipsoid (material rod-material)
          (center rod2_center)
          (e1 rod2_e1)
          (e2 rod2_e2)
          (e3 rod2_e3)
          (size w infinity h))
      )
    )
    (begin
      (list
        (make block (material rod-material)
          (center rod1_center)
          (e1 rod1_e1)
          (e2 rod1_e2)
          (e3 rod1_e3)
          (size infinity w h))
        (make block (material rod-material)
          (center rod2_center)
          (e1 rod2_e1)
          (e2 rod2_e2)
          (e3 rod2_e3)
          (size w infinity h))
      )
    )
  )
)

;;;;; create a custom prefix for output files
(set-param! filename-prefix
  (string-append
    "woodpile-FCT"
    "_c-" (number->string _c)
    "_"
  )
)

;;;;; run simulation
(run)
