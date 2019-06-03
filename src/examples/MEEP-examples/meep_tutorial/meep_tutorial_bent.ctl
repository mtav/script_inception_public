(reset-meep)
(set! geometry-lattice (make lattice (size 16 16 no-size)))

(set! geometry (list
                (make block (center -2 -3.5) (size 12 1 infinity)
                      (material (make dielectric (epsilon 12))))
                (make block (center 3.5 2) (size 1 12 infinity)
                      (material (make dielectric (epsilon 12))))))

(set! pml-layers (list (make pml (thickness 1.0))))
(set! resolution 10)
(set! sources (list
               (make source
                 (src (make continuous-src
                        (wavelength (* 2 (sqrt 12))) (width 20)))
                 (component Ez)
                 (center -7 -3.5) (size 0 1))))
;(run-until 200
;           (at-beginning output-epsilon)
;           (to-appended "ez" (at-every 0.6 output-efield-z)))
(use-output-directory)
;(run-until 200 (at-every 0.6 (output-png Ez "-Zc bluered")))
 (run-until 200 
   (to-appended "ez-slice" 
     (at-every 0.6 
       (in-volume (volume (center 0 -3.5) (size 16 0))
         output-efield-z))))
