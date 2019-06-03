(set! geometry (list
  (make sphere
    (material (make dielectric (epsilon 12)))
    (center 0 0 0)
    (radius 1)
  )
  (make cylinder
    (material (make dielectric (epsilon 12)))
    (center 0 0 0)
    (radius 1)
    (height 2)
    (axis 3 4 5)
  )
  (make cone
    (material (make dielectric (epsilon 12)))
    (center 0 0 0)
    (radius 1)
    (height 2)
    (axis 3 4 5)
    (radius2 6)
  )
  (make block
    (material (make dielectric (epsilon 12)))
    (center 0 0 0)
    (size 1 2 3)
    (e1 4 5 6)
    (e2 7 8 9)
    (e3 10 11 12)
  )
  (make ellipsoid
    (material (make dielectric (epsilon 12)))
    (center 0 0 0)
    (size 1 2 3)
    (e1 4 5 6)
    (e2 7 8 9)
    (e3 10 11 12)
  )
))

(init-fields)
;; (output-epsilon)

(exit)
