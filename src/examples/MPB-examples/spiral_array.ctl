(define-param output_epsilon_only? true) ; if true, exit after outputting epsilon

(load-from-path "spiral.ctl")

(define Nx 5)
(define Ny 5)

(define square_array
  (apply append
    (map
      (lambda (x)
        (map
          (lambda (y)
            (vector3 x y 0)
          )
          (interpolate (- Ny 2) (list -0.4 0.4))
        )
      )
      (interpolate (- Nx 2) (list -0.4 0.4))
    )
  )
)

(define Nturns 3)

(define spiral_array
  (get_spiral_coordinates
    0 ; spiral_type
    0.1 ; radius ; a
    (/ 0.1 (* 2 pi)); radius_growth ; b
    0 ; pitch ; c
    0 ; theta_start
    (* Nturns 2 pi) ; theta_end
    (+ (* Nturns (- 10 1)) 1) ; Npoints
  )
)

(define object_material (make dielectric (epsilon 2)))
(define voxel_size (vector3 0.05 0.05 0.1))
(define voxel_e1 (vector3 1 0 0))
(define voxel_e2 (vector3 0 1 0))
(define voxel_e3 (vector3 0 0 1))

(define (voxel_function pos)
  (make ellipsoid
    (center pos)
    (material object_material)
    (size voxel_size)
    (e1 voxel_e1)
    (e2 voxel_e2)
    (e3 voxel_e3)
  )
)

(define Nturns_object 3)
(define steps_object 4)

(define (spiral_function pos)
  (spiral
    ; general object properties
    pos ; object_center
    object_material
    (vector3 0.1 0.1 0.8) ; object_size
    (vector3 1 0 0) ; object_e1
    (vector3 0 1 0) ; object_e2
    (vector3 0 0 1) ; object_e3

    ; curve creation properties
    true ; curve_use_rods?

    ; voxel/rod creation properties
    2 ; rod_type
    voxel_size
    voxel_e1
    voxel_e2
    voxel_e3
    false ; voxel_axes_in_rod_axis_referential?
    0.1 ; Nvoxels_or_interVoxelDistance
    false ; Nvoxels?

    ; spiral properties
    0 ; spiral_type
    0.5 ; spiral_radius ; a
    0 ; spiral_radius_growth ; b
    (/ 1 Nturns_object) ; spiral_pitch ; c
    (* -1 (* Nturns_object pi)) ; spiral_theta_start
    (*  1 (* Nturns_object pi)) ; spiral_theta_end
    (+ (* Nturns_object steps_object) 1); spiral_Npoints
  )
)

(set! geometry
;;   (spiral_function (vector3 0 0 0))
;;   (list
;;     (voxel_function (vector3 0 0 0))
;;   )
;;   (map
;;     voxel_function
;;     square_array
;; ;;     spiral_array
;;   )
  (apply append (map
    spiral_function
;;     square_array
    spiral_array
  ))
)

(set! resolution 100)
(run-mpb run)
(exit)
