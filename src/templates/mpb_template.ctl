(load-from-path "utilities_mpb.ctl")

(set! geometry (list
  (make block
    (center -0.25 0 0)
    (material (make dielectric (epsilon 2)))
    (size 0.5 infinity infinity)
  )
  (make block
    (center 0.25 0 0)
    (material (make dielectric (epsilon 3)))
    (size 0.5 infinity infinity)
  )
))

(run-mpb run)
(exit)
