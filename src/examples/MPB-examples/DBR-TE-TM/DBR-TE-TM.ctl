(define-param te? true) ; if true, exit after outputting epsilon

(define-param n1 1.5)
(define-param n2 3.5)

(define-param d1 0.5)
(define-param d2 0.5)

(set-param! resolution 64)
(set-param! num-bands 6)
(define-param output_epsilon_only? false) ; if true, exit after outputting epsilon

(load-from-path "utilities.ctl")

(define a (+ d1 d2))
(define c1 (- (/ d1 2) (/ a 2)) )
(define c2 (- (/ a 2) (/ d2 2)) )

(define d1n (/ d1 a) )
(define d2n (/ d2 a) )

(define c1n (/ c1 a) )
(define c2n (/ c2 a) )

(define n_average (/ (+ (* n1 d1) (* n2 d2)) a ))
(define omega_bragg_normalized (/ 1 (* 2 n_average)) )
(define brewster_angle (atan (/ n2 n1) ) )

;;; Note: we make the lattice smaller in the X direction, to make the reciprocal lattice bigger in the X direction, thereby making the bands fold at bigger kx values
(set! geometry-lattice
  (make lattice
    (basis-size 0.25 1 1)
    (size 1 1 no-size)
  )
)

(set! geometry (list
  (make block
    (center 0 c1n )
    (size infinity d1n )
    (material (make dielectric (index n1)) )
  )
  (make block
    (center 0 c2n )
    (size infinity d2n )
    (material (make dielectric (index n2)) )
  )
))

;; ; define k-points
;; (set! k-points (list))
;; (define k_points
;;   (map (lambda (kx)
;;     (map (lambda (ky)
;;   ;;     (print "k=(" kx ", " ky ")\n")
;;       (vector3  kx ky 0)
;;     ) (interpolate 9 (list 0 0.5)) )
;;   ) (interpolate 9 (list 0 0.5)) )
;; )
;; 
;; (set! k-points (apply append! k_points))

;; (set! k-points (list
;;   (vector3  0 ky 0); Gamma
;;   (vector3  1 ky 0)
;; ))

;; (set! k-points (list
;;   (vector3  kx -0.5); Gamma
;;   (vector3  kx  0.5)
;; ))

;; (set! k-points (list
;;   (vector3  (* -0.5 (/ n2 n1)) -0.5)
;;   (vector3  (* 0 (/ n2 n1)) 0)
;;   (vector3  (* 0.5 (/ n2 n1))  0.5)
;; ))

;; (set! k-points (interpolate k-interp k-points))

(map (lambda (ky)
  (print "ky = " ky "\n")

  (set! k-points (list
    (vector3  0 ky 0); Gamma
    (vector3  0.25 ky 0)
  ))
  (set! k-points (interpolate k-interp k-points))

  (if te?
    (begin
      (print "TE run")
      (run-mpb run-te)
    )
    (begin
      (print "TM run")
      (run-mpb run-tm)
    )
  )

) (interpolate 9 (list 0 0.5)) )

(print "=========================================================\n")
(print "a=" a "\n")
(print "n1=" n1 " d1=" d1 "=" d1n "*a" " c1=" c1 "=" c1n "*a" "\n")
(print "n2=" n2 " d2=" d2 "=" d2n "*a" " c2=" c2 "=" c2n "*a" "\n")
(print "n_average=" n_average "\n")
(print "omega_bragg_normalized = " omega_bragg_normalized "\n")
(print "brewster_angle = " brewster_angle " rad = " (rad->deg brewster_angle) " deg" "\n")
(print "=========================================================\n")

(exit)
