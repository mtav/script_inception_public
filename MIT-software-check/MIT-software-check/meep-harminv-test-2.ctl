(define-param n 3.4)                     ; index of waveguide
(define-param w 1)                       ; width of waveguide
(define-param r 1)                       ; inner radius of ring
(define-param pad 4)                     ; padding between waveguide and edge of PML
(define-param dpml 2)                    ; thickness of PML
(define sxy (* 2 (+ r w pad dpml)))      ; cell size
(set! geometry-lattice (make lattice (size sxy sxy no-size)))

(set! geometry (list
                (make cylinder (center 0 0) (height infinity)
                      (radius (+ r w)) (material (make dielectric (index n))))
                (make cylinder (center 0 0) (height infinity)
                      (radius r) (material air))))
(set! pml-layers (list (make pml (thickness dpml))))
(set-param! resolution 10)

(define-param fcen 0.15)   ; pulse center frequency
(define-param df 0.1)      ; pulse frequency width
(set! sources (list
               (make source
                 (src (make gaussian-src (frequency fcen) (fwidth df)))
                 (component Ez) (center (+ r 0.1) 0))))

(run-sources+ 300
              (at-beginning output-epsilon)
              (after-sources (harminv Ez (vector3 (+ r 0.1)) fcen df)))
