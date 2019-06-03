;;;;; function to create a line/rod using various methods
;; To load:
;; (load-from-path "rod.ctl")
;;
;; TODO: define e1,e2,e3 in referential based on A->B direction to avoid singular matrix problems? (would make it harder to keep constant "voxel size", so maybe make optional?) -> probably best to implement later in proper class system

(load-from-path "utilities.ctl")

(define (rod
          A
          B
          rod_material
          rod_type
          axis_e1
          axis_e2
          axis_e3
          _size
          axes_in_rod_axis_referential?
          Nvoxels_or_interVoxelDistance
          Nvoxels?
        )
  (let*
    (
      (geometry_list (list))
      (rod_center (vector3* 0.5 (vector3+ A B)) )
      (rod_axis (vector3- B A) )
      (rod_length (vector3-norm (lattice->cartesian rod_axis)))
      (size_e1 (vector3-x _size))
      (size_e2 (vector3-y _size))
      (size_e3 (vector3-z _size))
      (M_axis->lattice (get_axis_referential rod_axis))
      (axis_e1_lattice (if axes_in_rod_axis_referential?  (matrix3x3* M_axis->lattice axis_e1) axis_e1))
      (axis_e2_lattice (if axes_in_rod_axis_referential?  (matrix3x3* M_axis->lattice axis_e2) axis_e2))
      (axis_e3_lattice (if axes_in_rod_axis_referential?  (matrix3x3* M_axis->lattice axis_e3) axis_e3))
      (Nvoxels (if Nvoxels?
        Nvoxels_or_interVoxelDistance
        (+ (ceiling (/ rod_length Nvoxels_or_interVoxelDistance)) 1)
      ))
    )
    
    (case rod_type
      ((0)(begin
        (print "rod_type: ellipsoid sequence\n")
        (set! geometry_list
          (map
            (lambda (pos)
              (print "pos = " pos "\n")
              (make ellipsoid
                (material rod_material)
                (center pos)
                (e1 axis_e1_lattice)
                (e2 axis_e2_lattice)
                (e3 axis_e3_lattice)
                (size _size)
              )
            )
            (interpolate (- Nvoxels 2) (list A B))
          )
        )
      ))
      ((1)(begin
        (print "rod_type: elliptical cylinder\n")
        (error "not yet implemented (in this script)")
      ))
      ((2)(begin
        (print "rod_type: cylinder\n")
        (set! geometry_list
          (list
            (make cylinder
              (material rod_material)
              (center rod_center)
              (axis rod_axis)
              (height rod_length)
              (radius (/ size_e1 2))
            )
          )
        )
      ))
      ((3)(begin
        (print "rod_type: ellipsoid\n")
        (set! geometry_list
          (list
            (make ellipsoid
              (material rod_material)
              (center rod_center)
              (e1 axis_e1_lattice)
              (e2 axis_e2_lattice)
              (e3 rod_axis)
              (size size_e1 size_e2 rod_length)
            )
          )
        )
      ))
      ((4)(begin
        (print "rod_type: block\n")
        (set! geometry_list
          (list
            (make block
              (material rod_material)
              (center rod_center)
              (e1 axis_e1_lattice)
              (e2 axis_e2_lattice)
              (e3 rod_axis)
              (size size_e1 size_e2 rod_length)
            )
          )
        )
      ))
      ((5)(begin
        (print "rod_type: cylinder with sphere caps\n")
        (set! geometry_list
          (list
            (make sphere
              (material rod_material)
              (center A)
              (radius (/ size_e1 2))
            )
            (make cylinder
              (material rod_material)
              (center rod_center)
              (axis rod_axis)
              (height rod_length)
              (radius (/ size_e1 2))
            )
            (make sphere
              (material rod_material)
              (center B)
              (radius (/ size_e1 2))
            )
          )
        )
      ))
      (else
        (error "unknown rod_type value\n")
      )
    )

    geometry_list
  )
)
