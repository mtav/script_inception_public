(set-param! resolution 50)

(set! geometry-lattice (make lattice (size 3 3 3)))

(set! geometry (list (make sphere (radius 1) (material (make medium (index 3.5))) (center 0 0 0))
                     (make cone (radius 0.8) (radius2 0.1) (height 2) (material air) (center 0 0 0))))

(set! eps-averaging? false)

(init-fields)

(output-epsilon)

(exit)
