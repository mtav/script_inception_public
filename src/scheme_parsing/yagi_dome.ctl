;preamble - some interesting settings
(set! filename-prefix false)
(set! output-single-precision? true)
(set-param! resolution 56.8513)

;simulation size
(define-param sx 2.97267) ; x size
(define-param sy 4.57883) ; y size
(define-param sz 5.94533) ; z size
(set! geometry-lattice (make lattice (size 2.97267 4.57883 5.94533)))

;geometry specification
(set! geometry
  (list
    (make block
      (center 1.48633 2.03942 0)
      (size 5.94533 0.5 5.94533)
      (material (make dielectric (epsilon 5.76))))
    (make block
      (center 1.48633 0.674667 4.76837e-07)
      (size 1 2.2295 1)
      (material (make dielectric (epsilon 5.76))))
    (make cylinder
      (center 0.50439 0.911689 4.76837e-07)
      (radius 0.079625)
      (height 2.2295)
      (material (make dielectric (epsilon 1))))
    (make cylinder
      (center 0.50439 0.686085 4.76837e-07)
      (radius 0.079625)
      (height 2.2295)
      (material (make dielectric (epsilon 1))))
    (make cylinder
      (center 0.50439 0.460481 4.76837e-07)
      (radius 0.079625)
      (height 2.2295)
      (material (make dielectric (epsilon 1))))
    (make cylinder
      (center 0.50439 0.234877 4.76837e-07)
      (radius 0.079625)
      (height 2.2295)
      (material (make dielectric (epsilon 1))))
    (make cylinder
      (center 0.50439 0.00927258 4.76837e-07)
      (radius 0.079625)
      (height 2.2295)
      (material (make dielectric (epsilon 1))))
    (make cylinder
      (center 0.50439 -0.216332 4.76837e-07)
      (radius 0.079625)
      (height 2.2295)
      (material (make dielectric (epsilon 1))))
    (make cylinder
      (center 0.50439 -0.640998 4.76837e-07)
      (radius 0.079625)
      (height 2.2295)
      (material (make dielectric (epsilon 1))))
    (make cylinder
      (center 0.50439 -0.866602 4.76837e-07)
      (radius 0.079625)
      (height 2.2295)
      (material (make dielectric (epsilon 1))))
    (make cylinder
      (center 0.50439 -1.09221 4.76837e-07)
      (radius 0.079625)
      (height 2.2295)
      (material (make dielectric (epsilon 1))))
    (make block
      (center 1.48633 1.53942 -2.6754)
      (size 5.94533 0.5 -0.594533)
      (material (make dielectric (epsilon 5.76))))
    (make block
      (center 4.16173 1.53942 0)
      (size 0.594533 0.5 5.94533)
      (material (make dielectric (epsilon 5.76))))
    (make block
      (center 1.48633 1.53942 2.6754)
      (size -5.94533 0.5 0.594533)
      (material (make dielectric (epsilon 5.76))))
    (make block
      (center -1.18907 1.53942 0)
      (size -0.594533 0.5 -5.94533)
      (material (make dielectric (epsilon 5.76))))
  )
)

;;excitations specification
(set! sources
  (list
    (make source
      (src (make gaussian-src (frequency 1.56986) (width 1.19917)
        (start-time 8.0944)))
      (component Ex)
      (center 1.46864 0.336261 4.76837e-07)
      (size 0.0353889 0 0))
  )
)

;boundaries specification
(set! pml-layers
  (list
    (make pml (direction Y) (side Low) (thickness 0.140718))
    (make pml (direction Z) (side Low) (thickness 0.140718))
    (make pml (direction X) (side High) (thickness 0.140718))
    (make pml (direction Y) (side High) (thickness 0.140718))
    (make pml (direction Z) (side High) (thickness 0.140718))
  ))
(init-fields)
(meep-fields-set-boundary fields Low X Metallic)

;simulation run specification
(run-until 1
  (after-time 0.00879487 (to-appended "x1id" (at-every 0.00879487 (in-volume (volume (center 1.48633 -0 0) (size 0 4.57883 5.94533))
    ))))
  (after-time 0.00879487 (to-appended "y2id" (at-every 0.00879487 (in-volume (volume (center 0 -4.76837e-07 0) (size 2.97267 0 5.94533))
    ))))
  (after-time 0.00879487 (to-appended "z3id" (at-every 0.00879487 (in-volume (volume (center 0 -0 4.76837e-07) (size 2.97267 4.57883 0))
    ))))
)
