(set! geometry-lattice (make lattice
  (size
    1
    2
    3
  )
  (basis-size
    1
    2
    3
  )
  (basis1 0 1 1)
  (basis2 1 0 1)
  (basis3 1 1 0)
))

(set! geometry (list
  (make sphere
    (material (make dielectric (epsilon 4)))
    (center 0 0 0)
    (radius 0.5)
  )
  (make sphere
    (material (make dielectric (epsilon 9)))
    (center 1 0 0)
    (radius 0.5)
  )
  (make sphere
    (material (make dielectric (epsilon 16)))
    (center 0 1 0)
    (radius 0.5)
  )
  (make sphere
    (material (make dielectric (epsilon 25)))
    (center 0 0 1)
    (radius 0.5)
  )
))

(run)
