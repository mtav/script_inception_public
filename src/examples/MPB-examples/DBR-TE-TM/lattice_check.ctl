(set! geometry-lattice
  (make lattice
    (basis-size 0.25 2 1)
    (size 1 1 no-size)
  )
)

(print (reciprocal->cartesian (vector3 1 0 0)) "\n")
(print (reciprocal->cartesian (vector3 0 1 0)) "\n")
