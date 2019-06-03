(define-param output_epsilon_only? true) ; if true, exit after outputting epsilon
(define-param use_rods? true)
(define-param rod_type 2)

(load-from-path "utilities.ctl")
(load-from-path "rod.ctl")

(define rod_material (make dielectric (epsilon 2)))
(define Nvoxels 5)
(define voxel_size (vector3 0.1 0.1 0.3))
(define voxel_e1 (vector3 1 0 0))
(define voxel_e2 (vector3 0 1 0))
(define voxel_e3 (vector3 0 0 1))

(define object_center (vector3 0 0 0))
(define object_size (vector3 1 1 1))
(define object_e1 (vector3 1 0 0))
(define object_e2 (vector3 0 1 0))
(define object_e3 (vector3 0 0 1))

(define (voxel_function pos)
  (make ellipsoid
    (center pos)
    (material rod_material)
    (size voxel_size)
    (e1 voxel_e1)
    (e2 voxel_e2)
    (e3 voxel_e3)
  )
)

(define (rod_function A B)
  (print "A = " A " to B = " B "\n")
  (rod A B rod_material rod_type voxel_e1 voxel_e2 voxel_e3 voxel_size Nvoxels)
)

(define vertex_list (list
  (vector3  0.25  0    0)
  (vector3  0     0.25 0)
  (vector3 -0.25  0    0)
  (vector3  0    -0.25 0)
))

(set! geometry (append
  (curve_from_coordinates
    (vector3 0 0 0)
    object_size
    object_e1
    object_e2
    object_e3
    use_rods?
    voxel_function
    rod_function
    vertex_list
  )

  (curve_from_coordinates
    (vector3 0 0 0.25)
    (vector3 0.5 0.5 0.5)
    object_e1
    object_e2
    object_e3
    use_rods?
    voxel_function
    rod_function
    vertex_list
  )

  (curve_from_coordinates
    (vector3 0 0 -0.25)
    object_size
    (vector3 1 1 0)
    (vector3 -1 1 0)
    object_e3
    use_rods?
    voxel_function
    rod_function
    vertex_list
  )

  (curve_from_coordinates
    (vector3 0 0 -0.25)
    (vector3 (* 1 (sqrt 2)) (* 1 (sqrt 2)) 1)
    (vector3 1 1 0)
    (vector3 -1 1 0)
    (vector3 0 0 1)
    use_rods?
    voxel_function
    rod_function
    vertex_list
  )

  (curve_from_coordinates
    (vector3 -0.25 0 0)
    (vector3 (* 1 (sqrt 2)) (* 1 (sqrt 2)) 1)
    (vector3 0  1 1)
    (vector3 0 -1 1)
    (vector3 1  0 0)
    use_rods?
    voxel_function
    rod_function
    vertex_list
  )

  (curve_from_coordinates
    (vector3 0 -0.25 0)
    (vector3 (* 1 (sqrt 2)) (* 1 (sqrt 2)) 1)
    (vector3 1  0  1)
    (vector3 1  0 -1)
    (vector3 0  1  0)
    use_rods?
    voxel_function
    rod_function
    vertex_list
  )

))

(run-mpb run)

(exit)
