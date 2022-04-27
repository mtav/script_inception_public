;; Example of two moving sources, each orbiting in a circle around different points.

(set-param! resolution 10)

(define-param sx 60)
(define-param sy 60)
(set! geometry-lattice (make lattice (size sx sy no-size)))

(define-param dpml 1.0)
(set! pml-layers (list (make pml (thickness dpml))))

(set! default-material (make dielectric (index 1.5)))

(define pi (acos -1)) ; a clever way to define Pi

;;;;; Parameters for source 1
(define-param v1 0.7) ; velocity of point charge
(define-param cx1 -10) ; centre X
(define-param cy1 0) ; centre Y
(define-param r1 10) ; radius
(define-param phi1 0) ; initial phase shift
(define omega1 (/ v1 r1)) ; angular velocity
(print "omega1:" omega1 "\n")

;;;;; Parameters for source 2
(define-param v2 0.7) ; velocity of point charge
(define-param cx2 10) ; centre X
(define-param cy2 0) ; centre Y
(define-param r2 10) ; radius
(define-param phi2 pi) ; initial phase shift
(define omega2 (/ v2 r2)) ; angular velocity
(print "omega2:" omega2 "\n")

;;;;; put output in a subdirectory
(use-output-directory) ; put output in a subdirectory
; (use-output-directory "mydir") ; put output in subdirectory "mydir"

;;;;; function to print debugging information
;;;;; See https://meep.readthedocs.io/en/latest/The_Run_Function_Is_Not_A_Loop/ for why we need to create a function.
(define (debug_info)
  (let
    (
      (x (+ cx1 (* r1 (cos (+ (* omega1 (meep-time)) phi1)))) )
      (y (+ cy1 (* r1 (sin (+ (* omega1 (meep-time)) phi1)))) )
    )
    (print "DEBUG:, " (meep-time) ", " x ", " y "\n")
  )
)

(run-until 100
  (lambda ()
    (change-sources! (list
      (make source
        (src (make continuous-src (frequency 1e-10)))
        ; (component Ex)
        (component Hz)
        (center
          (+ cx1 (* r1 (cos (+ (* omega1 (meep-time)) phi1))))
          (+ cy1 (* r1 (sin (+ (* omega1 (meep-time)) phi1))))
        )
      )
      (make source
        (src (make continuous-src (frequency 1e-10)))
        ; (component Ex)
        (component Hz)
        (center
          (+ cx2 (* r2 (cos (+ (* omega2 (meep-time)) phi2))))
          (+ cy2 (* r2 (sin (+ (* omega2 (meep-time)) phi2))))
        )
      )
    ))
  )
  debug_info ;; to print some debugging infos
  (at-every 2 (output-png Hz "-vZc dkbluered -M 1"))
)
