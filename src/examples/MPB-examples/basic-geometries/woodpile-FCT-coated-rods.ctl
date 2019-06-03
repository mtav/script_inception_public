;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; FCT-woodpile geometry with optional coated rods
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; geometry parameters
;;;;; all dimensions normalized by the VerticalPeriod, i.e. height of 4 layers
(define-param rod_width  0.278) ; width of the logs
(define-param rod_height 0.500) ; height of logs (should be 1/4 for fcc to not overlap)
(define-param _interRodDistance (sqrt 0.5)) ; distance between rods in one layer (horizontal period)

(define-param elliptical-rod-shape? true); if true, use elliptical rods, else blocks

(define-param coated-rods? true); if true, add coating
(define-param coating-thickness 0.075)

(define-param backfill-index 1.00 )
(define-param rod-index      1.52 )
(define-param coating-index  3.60 )

(define-param _lattice_mode 0) ; 0=FCT, 1=FCC, 2=BCC (FCC and BCC will override any interRodDistance setting)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; simulation parameters
(set-param! verbose? true)
(set-param! resolution 32)
(set-param! num-bands 10)
(define-param k-interp 9)
(define-param output_epsilon_only? false) ; if true, exit after outputting epsilon
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; load woodpile function (includes lattice setup)
(load-from-path "MPB_woodpile_FCT.ctl")
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; non-user-defined parameters
(define interLayerDistance 0.25) ; distance between layers (usually VerticalPeriod/4)
(define overlap (- 1 (/ interLayerDistance rod_height)) )
(define VerticalPeriod (* 4 interLayerDistance))
(define rod_coated_height (+ rod_height (* 2 coating-thickness)))
(define rod_coated_width  (+ rod_width  (* 2 coating-thickness)))

;;; set up k-point list
;; (set! k-points (interpolate k-interp FCC_standard_kpoints))
(set_kpoints FCC_standard_kpoints)

;;; set up materials
(set! default-material (make dielectric (index backfill-index) ) )
(define rod-material (make dielectric (index rod-index)))
(define coating-material (make dielectric (index coating-index)))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; print summary of essential parameters
(print "_lattice_mode = " _lattice_mode "\n")
(print "_a = " _a "\n")
(print "_b = " _b "\n")
(print "_c = " _c "\n")

(print "backfill-index = " backfill-index "\n")
(print "rod-index = " rod-index "\n")

(print "rod_width = " rod_width "\n")
(print "rod_height = " rod_height "\n")
(print "_interRodDistance = " _interRodDistance "\n")
(print "interLayerDistance = " interLayerDistance "\n")
(print "VerticalPeriod = " VerticalPeriod "\n")

(print "rod aspect ratio rod_height/rod_width = " (/ rod_height rod_width) "\n")
(print "overlap = " overlap "\n")

(print "elliptical-rod-shape? = " elliptical-rod-shape? "\n")
(print "coated-rods? = " coated-rods? "\n")
(print "coating-index = " coating-index "\n")
(print "coating-thickness = " coating-thickness "\n")
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; set up geometry
(set! geometry
  (append
    (if coated-rods?
      (MPB_woodpile_FCT elliptical-rod-shape? coating-material rod_coated_width rod_coated_height)
      (list)
    )
    (MPB_woodpile_FCT elliptical-rod-shape? rod-material rod_width rod_height)
  )
)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; create a custom prefix for output files
(set-param! filename-prefix
  (string-append
    "woodpile-FCT"
    "_w-" (format #f "~,3f" rod_width)
    "_h-" (format #f "~,3f" rod_height)
    "_i-" (format #f "~,3f" _interRodDistance)
    "_t-" (format #f "~,3f" coating-thickness)
    "_nb-" (format #f "~,2f" backfill-index)
    "_nr-" (format #f "~,2f" rod-index)
    "_nc-" (format #f "~,2f" coating-index)
    "_l-" (format #f "~d" _lattice_mode)
    "_e-" (if elliptical-rod-shape? "true" "false")
    "_c-" (if coated-rods? "true" "false")
    "_"
    )
)

(print "filename-prefix = " filename-prefix "\n")
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; run simulation
(init-params NO-PARITY true); for MPB

;;; output epsilon.h5 file only
(if output_epsilon_only?
  (begin
    ;; (init-fields) ; for MEEP
    (output-epsilon)
    (exit)
  )
)

;;; calculate bands
(run)
