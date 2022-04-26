;;; By setting the size in Z to no-size, we make this a 2D simulation.
(set! geometry-lattice (make lattice (size 5 5 no-size)))
(set! sources (list (make source
      (src (make continuous-src
        (frequency 1)
        (width 1)
      ))
      (component Ez)
      (center 0 0 0)
      (size 0 0 0)
)))
(set! pml-layers (list (make pml (thickness 1.0))))
(set! resolution 10)
(run-until 5
  (at-beginning output-epsilon)
;;   (to-appended "fields" (at-every 0.1 output-efield output-hfield))
;;   (at-every 0.1 output-efield output-hfield)
  (to-appended "fields" (at-every 0.1 output-efield-z))  ;; store everything in one file
  (at-every 0.1 output-efield-z) ;; store each time slice in a separate file
)
