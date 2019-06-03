(set-param! resolution 56.851324 )
(set! geometry-lattice (make lattice (size 2.97267 4.57883 5.94533)))

;geometry specification
(set! geometry
(list

(make block	( center 1.486333 -2.0394165          0)	( size 5.945333 0.5 5.945333 )	(material (make dielectric (epsilon 5.76))))
(make block	( center 1.4863335 -0.6746665      5e-07)	( size 1 2.2295 1 )	(material (make dielectric (epsilon 5.76))))
(make sphere
  (center 1.48633 -1.78942  0.00000)
  (radius 2.22950)
    
  (material (make dielectric (epsilon 0.00000))))
(make cylinder
  (center 0.5043895       -0.9116885 5.0000000007e-07)
  (radius 0.079625)
  (height 2.2295)
  (axis (vector3 0    1    0))(material (make dielectric (epsilon 1))))
(make cylinder
  (center 0.5043895       -0.6860845 5.0000000007e-07)
  (radius 0.079625)
  (height 2.2295)
  (axis (vector3 0    1    0))(material (make dielectric (epsilon 1))))
(make cylinder
  (center 0.5043895       -0.4604805 5.0000000007e-07)
  (radius 0.079625)
  (height 2.2295)
  (axis (vector3 0    1    0))(material (make dielectric (epsilon 1))))
(make cylinder
  (center 0.5043895       -0.2348765 5.0000000007e-07)
  (radius 0.079625)
  (height 2.2295)
  (axis (vector3 0    1    0))(material (make dielectric (epsilon 1))))
(make cylinder
  (center 0.5043895       -0.0092725 5.0000000007e-07)
  (radius 0.079625)
  (height 2.2295)
  (axis (vector3 0    1    0))(material (make dielectric (epsilon 1))))
(make cylinder
  (center 0.5043895        0.2163325 5.0000000007e-07)
  (radius 0.079625)
  (height 2.2295)
  (axis (vector3 0    1    0))(material (make dielectric (epsilon 1))))
(make cylinder
  (center 0.5043895        0.6409985 5.0000000007e-07)
  (radius 0.079625)
  (height 2.2295)
  (axis (vector3 0    1    0))(material (make dielectric (epsilon 1))))
(make cylinder
  (center 0.5043895        0.8666025 5.0000000007e-07)
  (radius 0.079625)
  (height 2.2295)
  (axis (vector3 0    1    0))(material (make dielectric (epsilon 1))))
(make cylinder
  (center 0.5043895        1.0922075 5.0000000007e-07)
  (radius 0.079625)
  (height 2.2295)
  (axis (vector3 0    1    0))(material (make dielectric (epsilon 1))))
(make block	( center 1.486333  -1.5394165 -2.67539985)	( size 5.945333 0.5 -0.5945333 )	(material (make dielectric (epsilon 5.76))))
(make block	( center 4.161733 -1.5394165          0)	( size 0.594533 0.5 5.945333 )	(material (make dielectric (epsilon 5.76))))
(make block	( center 1.486333 -1.5394165     2.6754)	( size -5.945333 0.5 0.594533 )	(material (make dielectric (epsilon 5.76))))
(make block	( center -1.18906685  -1.5394165           0)	( size -0.5945333 0.5 -5.945333 )	(material (make dielectric (epsilon 5.76))))

))

;;excitations specification
(set! sources
(list
(make source
(src (make gaussian-src (frequency 1.5698587) (width 1.1991698)
))
(component Ex)
(center 1.46864 -0.33626  0.00000)
(size 0.03539 0.00000 0.00000))
)
)
;boundaries specification
(set! pml-layers
(list
(make pml (direction X) (side Low) (thickness 0.300000))
(make pml (direction Y) (side Low) (thickness 0.300000))
(make pml (direction Z) (side Low) (thickness 0.300000))
(make pml (direction X) (side High) (thickness 0.300000))
(make pml (direction Y) (side High) (thickness 0.300000))
(make pml (direction Z) (side High) (thickness 0.300000))
))
(init-fields)
(run-until 0.035179
(at-beginning output-epsilon)
(to-appended "Slice1"
(at-every 0.03518
(in-volume (volume (center 1.486333 0.000000 0.000000) (size 0.000000 4.578833 5.945333))
output-efield-x)))

(to-appended "Slice2"
(at-every 0.03518
(in-volume (volume (center 0.000000 0.000000 0.000000) (size 2.972667 0.000000 5.945333))
output-efield-x)))

(to-appended "Slice3"
(at-every 0.03518
(in-volume (volume (center 0.000000 0.000000 0.000001) (size 2.972667 4.578833 0.000000))
output-efield-x)))

)
