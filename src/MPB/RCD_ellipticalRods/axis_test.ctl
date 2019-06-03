; generate an "axis object"

(set! geometry (list

  (make block
    (center (/ -1 4) (/ -1 4) (/ -1 4))
    (size 0.5 0.5 0.5)
    (material (make dielectric (epsilon 2)))
  )

  (make block
    (center (/ 1 4) (/ -1 4) (/ -1 4))
    (size 0.5 0.5 0.5)
    (material (make dielectric (epsilon 3)))
  )

  (make block
    (center (/ -1 4) (/ 1 4) (/ -1 4))
    (size 0.5 0.5 0.5)
    (material (make dielectric (epsilon 4)))
  )

  (make block
    (center (/ 1 4) (/ 1 4) (/ -1 4))
    (size 0.5 0.5 0.5)
    (material (make dielectric (epsilon 5)))
  )

  (make block
    (center (/ -1 4) (/ -1 4) (/ 1 4))
    (size 0.5 0.5 0.5)
    (material (make dielectric (epsilon 6)))
  )

  (make block
    (center (/ 1 4) (/ -1 4) (/ 1 4))
    (size 0.5 0.5 0.5)
    (material (make dielectric (epsilon 7)))
  )

  (make block
    (center (/ -1 4) (/ 1 4) (/ 1 4))
    (size 0.5 0.5 0.5)
    (material (make dielectric (epsilon 8)))
  )

  (make block
    (center (/ 1 4) (/ 1 4) (/ 1 4))
    (size 0.5 0.5 0.5)
    (material (make dielectric (epsilon 9)))
  )

))

(set-param! resolution 6)
(set! filename-prefix "axis_test-")

(run)

(exit)
