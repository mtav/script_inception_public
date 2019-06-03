(define-param sy 6) ; the size of the computational cell NOT including PML inthe y direction
(define-param sx 6) ; the size of the computational cell including PML inthe x direction
(define-param dpml 4) ; the thickness of PML layer
(define-param svert (+ sy (* 2 dpml)))
(define-param frec 1)
(define-param res 25)
(define-param theta (/ pi 4))

(define kx (* frec (sin theta)))
(define (my-amp-func p)(exp (* 0+2i pi kx (vector3-x p))))

(set! k-point (vector3 kx 0 0))
(set! geometry-lattice (make lattice (size sx svert no-size)))
(set! sources (list
             (make source
              (src (make continuous-src (frequency frec)))
              (component Hz)
              (center 0 (/ sy -2))
              (size sx 0)
              (amp-func my-amp-func))))

(set! pml-layers (list (make pml (thickness dpml) (direction Y))))
(set! resolution res)

(run-until 100
  (at-end (output-png Ex "-Zc dkbluered"))
  (at-end (output-png Ey "-Zc dkbluered"))
  (at-end (output-png Hz "-Zc dkbluered"))
)
