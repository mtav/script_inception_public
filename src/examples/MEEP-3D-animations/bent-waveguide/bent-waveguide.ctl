(reset-meep)
(set! geometry-lattice (make lattice (size 16 16 8)))
(set! geometry (list
                (make block (center -2 -3.5) (size 12 1 1)
                      (material (make medium (epsilon 12))))
                (make block (center 3.5 2) (size 1 12 1)
                      (material (make medium (epsilon 12))))))
(set! pml-layers (list (make pml (thickness 1.0))))
(set! resolution 10)
;; (set! sources (list
;;               (make source
;;                  (src (make continuous-src
;;                         (frequency 0.2)
;; ;;                         (wavelength (* 2 (sqrt 11)))
;; ;;                         (width 20)
;;                  ))
;;                  (component Ez)
;;                  (center -7 -3.5)
;;                  (size 0 1 1 )
;;               )
;; ))

(set! sources (list
               (make source
                 (src (make continuous-src (frequency 0.2)))
                 (component Ez)
                 (center -7 -3.5)
                 (size 0 1 1)
               )
))

;; (init-fields)
;; 
;; (output-epsilon)
;; 
;; 
;; (exit)

(run-until 100
           (at-beginning output-epsilon)
;;            (to-appended "ez-all" (at-every 0.6 output-efield-z))
           (at-every 0.6 output-efield-z)
           (at-every 0.6 output-dpwr)
           (at-end output-efield-z)
           (at-end output-dpwr)
)

(system* "h5tovtk" "./bent-waveguide-eps-000000.00.h5")
