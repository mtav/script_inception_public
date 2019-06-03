(define-param output_epsilon_only? true) ; if true, exit after outputting epsilon

(load-from-path "spiral.ctl")

(define steps 4)
(define turns 4)
(define dir -1)

(set! geometry-lattice
  (make lattice
    (size 1 1 1)
  )
)

(set! geometry
  (spiral
    ; general object properties
    (vector3 0 0 0) ; object_center
    (make dielectric (epsilon 2)) ; object_material
    (vector3 1 1 1) ; (vector3 (* 0.25 (sqrt 2)) (* 0.125 (sqrt 2)) 0.75) ; object_size
    (vector3 1 0 0) ; (vector3 1 1 0) ; object_e1
    (vector3 0 1 0) ; (vector3 -1 1 0) ; object_e2
    (vector3 0 0 1) ; (vector3 1 1 1) ; object_e3

    ; curve creation properties
    true ; curve_use_rods?

    ; voxel/rod creation properties
    0 ; rod_type
    (vector3 0.05 0.05 0.1) ; voxel_size
    (vector3 1 0 0) ; voxel_e1
    (vector3 0 1 0) ; voxel_e2
    (vector3 0 0 1) ; voxel_e3
    false ; voxel_axes_in_rod_axis_referential?
    0.05 ; Nvoxels_or_interVoxelDistance
    false ; Nvoxels?

    ; spiral properties
    2 ; spiral_type
    0.05 ; spiral_radius ; a
    0.08 ; spiral_radius_growth ; b
    0 ; (* dir (/ 1 turns)) ; spiral_pitch ; c
    0 ; (* -1 turns pi) ; spiral_theta_start
    (* 2 turns pi) ; (* turns pi) ; spiral_theta_end
    (* turns 100); (+ (* turns steps) 1) ; spiral_Npoints
  )
)

(set-param! resolution 64)
(run-mpb run)

(exit)
