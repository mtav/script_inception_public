(define-param output_epsilon_only? true) ; if true, exit after outputting epsilon

;; (load-from-path "utilities.ctl")
;; (load-from-path "all_FCC_BZ_labels.ctl")
(load-from-path "rod.ctl")

(define A (vector3 -0.25 -0.25 -0.25))
(define B (vector3  0.25  0.25  0.25))
(define rod_material (make dielectric (epsilon 2)))
(define rod_type 0)
(define axis_e1 (c->l 1 0 0))
(define axis_e2 (c->l 0 1 0))
(define axis_e3 (c->l 0 0 1))
(define _size (vector3 0.05 0.05 0.05))
;; (define size_e1 0.1)
;; (define size_e2 0.1)
;; (define size_e3 0.3)
;; (define Nvoxels 3)
(define Nvoxels_or_interVoxelDistance 0.1)
(define Nvoxels? false)

(define axes_in_rod_axis_referential? false)

(define (processCoords x y z)
  (vector3- (c->l x y z) (vector3 0.5 0.5 0.5))
)

(define (tetra x y z)
  (append
;;     (rod (processCoords x y z) (processCoords (- x 0.25) (- y 0.25) (- z 0.25) ) rod_material rod_type axis_e1 axis_e2 axis_e3 size_e1 size_e2 size_e3 Nvoxels)
;;     (rod (processCoords x y z) (processCoords (- x 0.25) (+ y 0.25) (+ z 0.25) ) rod_material rod_type axis_e1 axis_e2 axis_e3 size_e1 size_e2 size_e3 Nvoxels)
;;     (rod (processCoords x y z) (processCoords (+ x 0.25) (- y 0.25) (+ z 0.25) ) rod_material rod_type axis_e1 axis_e2 axis_e3 size_e1 size_e2 size_e3 Nvoxels)
;;     (rod (processCoords x y z) (processCoords (+ x 0.25) (+ y 0.25) (- z 0.25) ) rod_material rod_type axis_e1 axis_e2 axis_e3 size_e1 size_e2 size_e3 Nvoxels)

    (rod (processCoords x y z) (processCoords (- x 0.25) (- y 0.25) (- z 0.25) ) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
    (rod (processCoords x y z) (processCoords (- x 0.25) (+ y 0.25) (+ z 0.25) ) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
    (rod (processCoords x y z) (processCoords (+ x 0.25) (- y 0.25) (+ z 0.25) ) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
    (rod (processCoords x y z) (processCoords (+ x 0.25) (+ y 0.25) (- z 0.25) ) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
  )
)

(set! geometry (append
;;   (rod A B rod_material rod_type axis_e1 axis_e2 axis_e3 size_e1 size_e2 size_e3 Nvoxels)
;;   (tetra 0.25 0.25 0.25)
;;   (tetra 0.25 0.75 0.75)
;;   (tetra 0.75 0.25 0.75)
;;   (tetra 0.75 0.75 0.25)
  (rod (processCoords 0.25 0.25 0.25) (processCoords 0.75 0.75 0.75) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
  
  (rod (processCoords 0.25 0.25 0.25) (processCoords 0.25 0.75 0.75) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
  (rod (processCoords 0.25 0.25 0.25) (processCoords 0.75 0.25 0.75) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
  (rod (processCoords 0.25 0.25 0.25) (processCoords 0.75 0.75 0.25) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)

  (rod (processCoords 0.25 0.25 0.25) (processCoords 0.75 0.25 0.25) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
  (rod (processCoords 0.25 0.25 0.25) (processCoords 0.25 0.75 0.25) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
  (rod (processCoords 0.25 0.25 0.25) (processCoords 0.25 0.25 0.75) rod_material rod_type axis_e1 axis_e2 axis_e3 _size axes_in_rod_axis_referential? Nvoxels_or_interVoxelDistance Nvoxels?)
))

(set! resolution 100)
(run-mpb run)

(exit)
