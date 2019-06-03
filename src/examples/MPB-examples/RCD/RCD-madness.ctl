(define-param _a 1)
(define-param _b 1)
(define-param _c 1) ; FCC if _c = _a = _b to BCC if _c = _a/sqrt(2) = _b/sqrt(2)
(define-param output_epsilon_only? true) ; if true, exit after outputting epsilon

;; (load-from-path "all_FCT_BZ_labels.ctl")
(load-from-path "spiral.ctl")

(define (processCoords x y z)
  (vector3- (c->l x y z) (vector3 0.5 0.5 0.5))
)

(define object_material (make dielectric (epsilon 2)))
(define axis_e1 (vector3 1 0 0))
(define axis_e2 (vector3 0 1 0))
(define axis_e3 (vector3 0 0 1))
(define axes_in_rod_axis_referential? true)

(define Nturns 2)
(define steps 32)
(define spiral? true)

(define (myCustomRod A B spiral?)
  
  (define rod_axis (vector3- B A))
  (define rod_length (vector3-norm (lattice->cartesian rod_axis)))
  (define M_axis->lattice (get_axis_referential rod_axis))
  (define axis_e1_lattice (if axes_in_rod_axis_referential?  (matrix3x3* M_axis->lattice axis_e1) axis_e1))
  (define axis_e2_lattice (if axes_in_rod_axis_referential?  (matrix3x3* M_axis->lattice axis_e2) axis_e2))
  (define axis_e3_lattice (if axes_in_rod_axis_referential?  (matrix3x3* M_axis->lattice axis_e3) axis_e3))

  (if (not spiral?)
  
    (rod
      A
      B
      object_material
      2 ; rod_type
      axis_e1
      axis_e2
      axis_e3
      (vector3 0.1 0.1 0.3) ; _size
      axes_in_rod_axis_referential?
      5 ; Nvoxels_or_interVoxelDistance
      true ; Nvoxels?
    )

    (spiral
      ; general object properties
      (vector3* 0.5 (vector3+ A B)) ; object_center
      object_material
      (vector3 0.1 0.1 rod_length) ; object_size
      axis_e1_lattice ; object_e1
      axis_e2_lattice ; object_e2
      rod_axis ; object_e3

      ; curve creation properties
      false ; curve_use_rods?

      ; voxel/rod creation properties
      0 ; rod_type
      (vector3 0.05 0.05 0.1) ; voxel_size
      axis_e1_lattice ; voxel_e1
      axis_e2_lattice ; voxel_e2
      axis_e3_lattice ; voxel_e3
      false ; axes_in_rod_axis_referential? ; voxel_axes_in_rod_axis_referential?
      0.05 ; Nvoxels_or_interVoxelDistance
      false ; Nvoxels?

      ; spiral properties
      0 ; spiral_type
      0.5 ; spiral_radius ; a
      0 ; spiral_radius_growth ; b
      (/ 1 Nturns) ; spiral_pitch ; c
      (* -1 (* Nturns pi)) ; spiral_theta_start
      (*  1 (* Nturns pi)) ; spiral_theta_end
      (+ (* Nturns steps) 1) ; spiral_Npoints
    )
  )
)

(define (tetra x y z)
  (append
    (myCustomRod (processCoords x y z) (processCoords (- x 0.25) (- y 0.25) (- z 0.25) ) spiral?)
    (myCustomRod (processCoords x y z) (processCoords (- x 0.25) (+ y 0.25) (+ z 0.25) ) spiral?)
    (myCustomRod (processCoords x y z) (processCoords (+ x 0.25) (- y 0.25) (+ z 0.25) ) spiral?)
    (myCustomRod (processCoords x y z) (processCoords (+ x 0.25) (+ y 0.25) (- z 0.25) ) spiral?)
  )
)

(define test_A (processCoords 0.25 0.25 0.25))
(define test_B (processCoords 0.5 0.5 0.5))

(set! geometry (append
;;   (myCustomRod test_A test_B false)
;;   (myCustomRod test_A test_B true)
  
;;   (rod A B rod_material rod_type axis_e1 axis_e2 axis_e3 size_e1 size_e2 size_e3 Nvoxels)
  (tetra 0.25 0.25 0.25)
  (tetra 0.25 0.75 0.75)
  (tetra 0.75 0.25 0.75)
  (tetra 0.75 0.75 0.25)
;;   (rod (processCoords 0.25 0.25 0.25) (processCoords 0.75 0.75 0.75) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
;;   
;;   (rod (processCoords 0.25 0.25 0.25) (processCoords 0.25 0.75 0.75) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
;;   (rod (processCoords 0.25 0.25 0.25) (processCoords 0.75 0.25 0.75) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
;;   (rod (processCoords 0.25 0.25 0.25) (processCoords 0.75 0.75 0.25) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
;; 
;;   (rod (processCoords 0.25 0.25 0.25) (processCoords 0.75 0.25 0.25) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
;;   (rod (processCoords 0.25 0.25 0.25) (processCoords 0.25 0.75 0.25) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
;;   (rod (processCoords 0.25 0.25 0.25) (processCoords 0.25 0.25 0.75) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
))

(set! resolution 100)

(run-mpb run)
(exit)
