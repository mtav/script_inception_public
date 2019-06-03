(set! num-bands 10)
(set! default-material (make dielectric (index 2.6)))
(set! resolution 16)
(set! mesh-size 5)



(set! geometry-lattice
   (make lattice
     (basis1 0 1 1)
     (basis2 1 0 1)
     (basis3 1 1 0)
     (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
     (size 1 1 1)
   )
)

(set! geometry
   (list
     (make sphere
       (center 0 0 0)
       (radius (/ (sqrt 0.5) 2))
       (material
         (make dielectric
           (index 1.0)
         )
       )
     )
   )
)


(set! k-points
   (interpolate 4
     (list
                                 (vector3 0 0.5 0.5)            ; X
                                 (vector3 0 0.625 0.375)        ; U
                                 (vector3 0 0.5 0)              ; L
                                 (vector3 0 0 0)                ; Gamma
                                 (vector3 0 0.5 0.5)            ; X
                                 (vector3 0.25 0.75 0.5)        ; W
                                 (vector3 0.375 0.75 0.375)     ; K
     )
   )
)

(run)
