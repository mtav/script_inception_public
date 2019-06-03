(set! geometry-lattice (make lattice (size 16 8 8)))
(set! geometry (list
                (make block (center 0 0 0) (size infinity 1 1)
                      (material (make medium (epsilon 12))))))
(set! sources (list
               (make source
                 (src (make continuous-src (frequency 0.2)))
                 (component Ez)
                 (center -7 0)
                 (size 0 1 1)
               )
))
(set! pml-layers (list (make pml (thickness 1.0))))
(set! resolution 10)
(run-until 100
           (at-beginning output-epsilon)
;;            (at-end output-efield-z)
;;            (to-appended "ez" 
            (at-every 0.6 output-efield-z)
;;            )
            (at-end (output-png Ez "-0x0 -Zc dkbluered -o final-x.png"))
            (at-end (output-png Ez "-0y0 -Zc dkbluered -o final-y.png"))
            (at-end (output-png Ez "-0z0 -Zc dkbluered -o final-z.png"))
            
            (at-every 0.6 output-dpwr)
;;            )
            (at-end output-dpwr)
)

;; h5topng -S3 eps-000000.00.h5
;; h5topng -S3 -Zc dkbluered -a yarg -A eps-000000.00.h5 ez-000200.00.h5
;; unix% h5topng -t 0:329 -R -Zc dkbluered -a yarg -A eps-000000.00.h5 ez.h5
;; unix% convert ez.t*.png ez.gif
;;            (to-appended "ez" (at-every 0.6 output-efield-z)))

;;        -Z     Center the color scale on the value zero in the data.
;;        -c colormap
;;    -R     When multiple files are specified, set the bottom and top of the color maps according to the minimum and maximum over all the data.  This is useful to process many files using a consistent color scale, since otherwise the scale is set for each  file
;;               individually.
;; h5topng -0z0 -t 0:332 -R -Zc dkbluered bent-waveguide-ez-all.h5
;; h5topng -0z0 -R -Zc dkbluered straight-waveguide-ez-*.h5
