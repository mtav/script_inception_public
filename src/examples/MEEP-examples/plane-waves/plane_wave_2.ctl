;; (define-param sx 6) ; the size of the computational cell NOT including PML inthe x direction
;; (define-param sy 6) ; the size of the computational cell NOT including PML inthe y direction

(define-param sx 7) ; size of cell in X direction
(define-param sy 3) ; size of cell in Y direction
(define-param sz no-size) ; size of cell in Z direction

;; (define-param dpml 4) ; the thickness of PML layers
(define-param dpml 1) ; the thickness of PML layers

;; (define-param sx_final (+ sx (* 2 dpml)))
(define-param sx_final sx)

;; (define-param fcen 1)
(define-param fcen 1.3333333333333333)
(define-param df 0.6666666666666666)

;; (define-param res 25)
(define-param res 50)
(define-param theta (/ pi 4))

(set! geometry-lattice (make lattice (size sx_final sy no-size)))

(set! k-point (vector3 0 0 0))

(set! sources (list
  (make source
;;     (src (make continuous-src (frequency fcen)))
    (src (make gaussian-src (frequency fcen) (fwidth df)))
    (component Ez)
    (center (+ (/ sx -2) dpml) 0)
    (size 0 sy)
  )
))

(set! pml-layers (list (make pml (thickness dpml) (direction X))))
(set! resolution res)

(define src_time (* 2 5 (/ 1 df)) )
(print "src_time = " src_time "\n")

(run-sources
;;   output-efield-z
  (to-appended "ez" output-efield-z)
)

;; (run-until 75
;;   (at-end (output-png Ex "-Zc dkbluered"))
;;   (at-end (output-png Ey "-Zc dkbluered"))
;;   (at-end (output-png Ez "-Zc dkbluered"))
;;   (at-end (output-png Hx "-Zc dkbluered"))
;;   (at-end (output-png Hy "-Zc dkbluered"))
;;   (at-end (output-png Hz "-Zc dkbluered"))
;; )
