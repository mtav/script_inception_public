(set! geometry-lattice (make lattice
                         (size 1 1 1)))

(set-param! k-points (vector3 0 0 0))
(define-param k-interp 9)
(set! ensure-periodicity true)
; Corners of the irreducible Brillouin zone for the fcc lattice,

(define X (vector3 0 0.5 0.5))
(define U (vector3 0.25 0.625 0.625))
(define L (vector3 0.5 0.5 0.5))
(define Gamma (vector3 0 0 0))
(define W (vector3 0.25 0.5 0.75))
(define K (vector3 0.375 0.375 0.75))

(define-param k-points (list X U L Gamma W K))
(set! k-points (interpolate k-interp k-points))

(define-param eps 12) ; the dielectric constant of the "log" material

(define diel (make dielectric (epsilon eps)))

(define-param w 0.20) ; width of the logs
(define-param h 0.25) ; height of logs (should be 1/4 for fcc to not overlap) 

(set! geometry
      (append
        (list
         (make block (material diel)
               (center  0 (- 0.5 (* 0.5 w)) (* -1.5 h))
               (size infinity w h))
         (make block (material diel)
               (center (+ -0.5 (* 0.5 w)) 0 (* -0.5 h))
               (size w infinity h))
         (make block (material diel)
               (center 0 (* -0.5 w) (* 0.5 h))
               (size infinity w h))
         (make block (material diel)
               (center (* 0.5 w) 0 (* 1.5 h))
               (size w infinity h)))
))

;(set! pml-layers (list (make pml (direction Z) (thickness 0.1))))

(set-param! resolution 10)
(define-param lambda0 2)
(define-param df 2.5)
(set! sources (list
               (make source
                (src (make gaussian-src (wavelength lambda0)
               (fwidth df)
                ))
                 (component Ex) (center 0. 0. 0.0055))
               ))

(run-k-points 300 k-points)
(output-epsilon)
(output-efield-z)
