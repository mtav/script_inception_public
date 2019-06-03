(define-param rod-radius 0.1 )
(define-param rod-index 2 )
(define-param backfill-index 1 )

(set-param! resolution 32)

(set! default-material (make dielectric (index backfill-index) ) )
(define rod-material (make dielectric (index rod-index)))

;;; The tetrahedron centres
(define __R0__ (vector3 (/ (sqrt 2) 4) (/ 1 (sqrt 6)) (/ (sqrt 3) 4)) )
(define __R1__ (vector3 (/ (- (sqrt 2)) 4) (/ 1 (sqrt 6)) (/ (sqrt 3) 4) ) )
(define __R2__ (vector3 0 (/ -1 (sqrt 24)) (/ (sqrt 3) 4)) )

(define __G0__ (vector3 (/ (sqrt 2) 4) 0 (/ (* 7 (sqrt 3)) 12)) )
(define __G1__ (vector3 0 (/ (sqrt 6) 4) (/ (* 7 (sqrt 3)) 12)) )
(define __G2__ (vector3 (- (/ (sqrt 2) 4)) 0 (/ (* 7 (sqrt 3)) 12)) )

(define __B0__ (vector3 (/ (sqrt 2) 4) (/ -1 (sqrt 6)) (/ (* 11 (sqrt 3)) 12)) )
(define __B1__ (vector3 0 (/ 1 (sqrt 24)) (/ (* 11 (sqrt 3)) 12)) )
(define __B2__ (vector3 (- (/ (sqrt 2) 4)) (/ -1 (sqrt 6)) (/ (* 11 (sqrt 3)) 12)) )

;;; cell type 1 parameters
(define __offset1__ (vector3 (/ (sqrt 2) 4) 0 (/ (* 11 (sqrt 3)) 24)) )
(define __u1__ (vector3 (/ (sqrt 2) 4) (- (/ (sqrt 6) 4)) 0) )
(define __v1__ (vector3 (/ (sqrt 2) 4) (/ (sqrt 6) 4) 0) )
(define __w1__ (vector3 0 0 (sqrt 3)) )

;;; cell type 2 parameters
(define __offset2__ (vector3 (- (/ (sqrt 2) 4)) 0 (/ (* 11 (sqrt 3)) 24)) )
(define __u2__ (vector3 (/ (sqrt 2) 2) 0 0) )
(define __v2__ (vector3 0 (/ (sqrt 6) 2) 0) )
(define __w2__ (vector3 0 0 (sqrt 3)) )

(define RCD111_origin (vector3 0 0 0))
(define-param Nx 3)
(define-param Ny 3)
(define-param Nz 3)

(define-param buffer 1)

;; (define RCD_size_x ((* 2 Nx)-1+1/2)*(vector3-norm __u2__) )
;; (define RCD_size_y ((* 2 Ny)-1+2/6)*(vector3-norm __v2__) )
;; (define RCD_size_z ((* 2 Nz)-1)*(vector3-norm __w2__) )
;; 
;; (define RCD_min_x -(Nx-1+1/2)*(vector3-norm __u2__) )
;; (define RCD_min_y -(Ny-1+1/2+1/6)*(vector3-norm __v2__) )
;; (define RCD_min_z -(Nz-1)*(vector3-norm __w2__) -  (vector3-z __offset2__) )
;; 
;; (define RCD_max_x (+ RCD_min_x RCD_size_x))
;; (define RCD_max_y (+ RCD_min_y RCD_size_y))
;; (define RCD_max_z (+ RCD_min_z RCD_size_z))

(* Nx (vector3-norm __u2__))
(* Ny (vector3-norm __v2__))
(* Nz (vector3-norm __w2__))

;; (set! geometry-lattice (make lattice (size sx sy sy)))

;; (set! geometry
;;   (list
;;     (make cylinder
;;       (material mat)
;;       (center (vector3* 0.5 (vector3+ A B)) )
;;       (radius rod-radius)
;;       (height (/ (sqrt 3) 4))
;;       (axis (vector3- B A) )
;;     )
;;   )
;; )
;; (load-from-path "RCD111_geometry.ctl")

;;; create RCD111_1x1x1.geo.ctl with:
; geotoctl.py -o RCD111_geometry.ctl ./RCD111_1x1x1.geo --no-offset

(print %load-path "\n")
;; (define %load-path (append %load-path (list ".")) )
;; (define %load-path ("." . %load-path) )
;; (add-to-load-path ".") ; not available on BC3 :( (older/newer guile version?)
;; (print %load-path "\n")
(load "RCD111_1x1x1.geo.ctl")
;; (load-from-path "RCD111_1x1x1.geo.ctl")
;; (load-from-path "./RCD111_1x1x1.geo.ctl")

(set-param! eps-averaging? false)

(run-until 1
  (at-beginning output-epsilon)
)
