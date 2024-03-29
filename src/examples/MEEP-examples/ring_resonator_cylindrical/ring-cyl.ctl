(define-param n 3.4) ; index of waveguide
(define-param w 1) ; width of waveguide
(define-param r 1) ; inner radius of ring
(define-param pad 4) ; padding between waveguide and edge of PML
(define-param dpml 2) ; thickness of PML

(define sr (+ r w pad dpml)) ; radial size (cell is from 0 to sr)
(set! dimensions CYLINDRICAL)
(set! geometry-lattice (make lattice (size sr no-size no-size)))

(set-param! m 3)

(set! geometry (list
                (make block (center (+ r (/ w 2))) (size w infinity infinity)
                      (material (make dielectric (index n))))))
(set! pml-layers (list (make pml (thickness dpml))))
(set-param! resolution 10)

(define-param fcen 0.15) ; pulse center frequency                            
(define-param df 0.1)  ; pulse width (in frequency) 
(set! sources (list
               (make source
                 (src (make gaussian-src (frequency fcen) (fwidth df)))
                 (component Ez) (center (+ r 0.1) 0 0))))

(run-sources+ 200 (after-sources (harminv Ez (vector3 (+ r 0.1)) fcen df)))

(run-until (/ 1 fcen) 
           (in-volume (volume (center 0) (size (* 2 sr)))
                      (at-beginning output-epsilon)
                      (to-appended "ez" 
                                   (at-every (/ 1 fcen 20) output-efield-z))))
