; compound object test

(set! geometry (list

  (make compound-geometric-object
    (material (make dielectric (index 4)))
    (center 0 0 0)
    (component-objects
      (make cylinder (center -0.25 -0.25 0) (radius 0.1) (height 0.2))
      (make cylinder (center -0.25 0.25 0) (radius 0.1) (height 0.3))
      (make cylinder (center 0.25 -0.25 0) (radius 0.1) (height 0.4))
      (make cylinder (center 0.25 0.25 0) (radius 0.1) (height 0.5))
    )
  )
  
  (make cone
    (material (make dielectric (index 4)))
    (center 0 0 0.25)
    (radius 0.1)
    (height 0.5)
    (axis 1 1 -1)
  )

  (make cone
    (material (make dielectric (index 4)))
    (center 0 0 -0.25)
    (radius 0.1)
    (height 0.5)
    (axis -1 -1 1)
  )

  (make cone
    (material (make dielectric (index 4)))
    (center 0 0 0.5)
    (radius 0.1)
    (height 0.5)
    (axis -1 0 0)
  )

))

(set-param! resolution 100)

(run)
