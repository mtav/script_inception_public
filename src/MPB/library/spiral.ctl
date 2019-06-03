;;;;; function to create spirals
;; based on $HOME/bin/blender-2.77a-linux-glibc211-x86_64/2.77/scripts/addons/add_curve_extra_objects/add_curve_spirals.py
;; (load-from-path "spiral.ctl")

;; TODO: option for regularly spaced points in growing spirals? (need analytic formula for spiral length, etc)

;; (load-from-path "utilities.ctl")
(load-from-path "rod.ctl")

(define (get_spiral_coordinates
          spiral_type
          radius ; a
          radius_growth ; b
          pitch ; c
          theta_start
          theta_end
          Npoints
        )

  (define (pos theta)
    (let*
      (
        ( r
          (case spiral_type
            ((0)(begin
              (print "spiral_type=0 : archimedean\n")
              (+ radius (* radius_growth theta))
            ))
            ((1)(begin
              (print "spiral_type=1 : logarithmic\n")
              (* radius (exp (* radius_growth theta)))
            ))
            ((2)(begin
              (print "spiral_type=2 : golden spiral\n")
              (* radius (exp (* golden_spiral_radius_growth theta)))
            ))
            (else
              (error "unknown spiral_type \n")
            )
          )
        )
        ( x (* r (cos theta)) )
        ( y (* r (sin theta)) )
        ( z (* (/ theta (* 2 pi)) pitch) )
      )
      (vector3 x y z)
    )
  )

  (map 
    pos
    (interpolate (- Npoints 2) (list theta_start theta_end))
  )

)

(define (spiral
    ; general object properties
    object_center
    object_material
    object_size
    object_e1
    object_e2
    object_e3

    ; curve creation properties
    curve_use_rods?

    ; voxel/rod creation properties
    rod_type
    voxel_size
    voxel_e1
    voxel_e2
    voxel_e3
    voxel_axes_in_rod_axis_referential?
    Nvoxels_or_interVoxelDistance
    Nvoxels?

    ; spiral properties
    spiral_type
    spiral_radius ; a
    spiral_radius_growth ; b
    spiral_pitch ; c
    spiral_theta_start
    spiral_theta_end
    spiral_Npoints
  )

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

  (define (rod_function A B)
    (rod A B
      object_material
      rod_type
      voxel_e1
      voxel_e2
      voxel_e3
      voxel_size
      voxel_axes_in_rod_axis_referential?
      Nvoxels_or_interVoxelDistance
      Nvoxels?
    )
  )

  (define vertex_list
    (get_spiral_coordinates
      spiral_type
      spiral_radius ; a
      spiral_radius_growth ; b
      spiral_pitch ; c
      spiral_theta_start
      spiral_theta_end
      spiral_Npoints
    )
  )

  (curve_from_coordinates
    object_center
    object_size
    object_e1
    object_e2
    object_e3
    curve_use_rods?
    voxel_function
    rod_function
    vertex_list
  )
)

;; (define vertex_list
;;   (list
;;           (vector3 0 0 0)
;;           (vector3 1 0 0)
;;           (vector3 1 1 0)
;;           (vector3 0 1 0)
;;   )
;; )
;; 
;; (define vertex_list
;;   (list
;;           (vector3 0 0 0)
;;   )
;; )
;;   (define kiki
;;   (do ((idx 1 (+ idx 1))) ((>= idx (length vertex_list)))
;;     (print "-----\n")
;;     (print "vertex_list [" (- idx 1) "] =" (list-ref vertex_list (- idx 1)) "\n")
;;     (print "vertex_list [" idx "] =" (list-ref vertex_list idx) "\n")
;;     (list (- idx 1) idx)
;; ;;     (rod_function (list-ref vertex_list (- idx 1)) (list-ref vertex_list idx))
;;   )
;;   )
;;   
;; 
;;   (map voxel_function vertex_list)
  
;;   (define _e1_final (cartesian->lattice (vector3-scale (vector3-x _size) (unit-vector3 (lattice->cartesian _e1)))))
;;   (define _e2_final (cartesian->lattice (vector3-scale (vector3-y _size) (unit-vector3 (lattice->cartesian _e2)))))
;;   (define _e3_final (cartesian->lattice (vector3-scale (vector3-z _size) (unit-vector3 (lattice->cartesian _e3)))))
;;   
;;   (define M (matrix3x3 _e1_final _e2_final _e3_final))
;;   (map
;;     (lambda pos)
;;       M
;;     (print "x=" x ", y = " y "\n")
;;     )
;;     new_vertex_list
;;   )

;;         (list
;;           (vector3  0.25  0    -0.25 )
;;           (vector3  0     0.25 -0.125)
;;           (vector3 -0.25  0     0.125)
;;           (vector3  0    -0.25  0.25 )
;;         )
;;     total_steps = steps * turns
;;     z_scale = pitch * turns
;;     
;;     max_phi  = 2*pi*turns
;;     step_phi = max_phi/total_steps
;;     if spiral_direction == 1:
;;         step_phi *= -1
;;         max_phi *= -1
;;     step_z   = z_scale/(total_steps-1)
;;     
;;     verts = []
;;     verts.extend([radius,0,0])
;;     
;;     cur_phi = 0
;;     cur_z   = 0
;; 
;;     cur_rad = radius
;;     step_rad = dif_radius/(total_steps*turns)
;;     
;;     while abs(cur_phi) <= abs(max_phi):
;;         cur_phi += step_phi
;;         cur_z   += step_z
;;         
;;         if spiral_type == 1:
;;             cur_rad += step_rad
;;         if spiral_type == 2:
;;             #r = a*e^{|theta| * b}
;;             cur_rad = radius * pow(B_force, abs(cur_phi)) 
;;     
;;         px = cur_rad * cos(cur_phi)
;;         py = cur_rad * sin(cur_phi)
;;         verts.extend( [px,py,cur_z] )
;; 
;;     return verts
