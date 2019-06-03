; The index will vary sinusoidally between index-min and index-max:

(define-param index-min 2)
(define-param index-max 3)

(define-param a 0.5)
(define-param b 0.1)

(define pi (* 4 (atan 1))) ; 3.14159...

; Define a function of position p (in the lattice basis) that returns
; the material at that position.  In this case, we use the function:
;        index-min + 0.5 * (index-max - index-min)
;                        * (1 + cos(2*pi*x))
; This is periodic, and also has inversion symmetry.
(define (eps-func p-lattice)
;;   if (x/a)^2 + (y/b)^2 < 1:
;;     inside
;;   else:
;;     outside

  (let* (
          (p (lattice->cartesian p-lattice))
          (x (vector3-x p))
          (y (vector3-y p))
          (z (vector3-z p))
         )
    (if (< (+ (expt (/ x a) 2) (expt (/ y b) 2) ) 1)
      (make dielectric (index 4))
      (make dielectric (index 2))
    )
  )

)

(define (c->l . args) (cartesian->lattice (apply vector3 args)))

(make cylinder
  (center (c->l (/ -3 8) (/ -3 8) (/ -3 8)))
  (axis (c->l 1 1 1))
  (radius 0.1)
  (height 1)
;;   (material diel_inner)
)

; elliptical cylinder attributes:
;; center vector3
;; material material-type
;; ellipsoid-e1 vector3
;; ellipsoid-e2 vector3
;; ellipsoid-e3 vector3
;; size vector3
;; block-e1 vector3
;; block-e2 vector3
;; block-e3 vector3
;; size vector3

(define elliptical_cylinder
  (let* ((w 0.1) (h 0.5) (L 0.5))
    (list
      (make ellipsoid (center 0 0 0)  (size w h infinity) (e1 -1 1 0) (e2 -1 -1 2) (e3 1 1 1))
      (make block  (center 0 0 0)  (size 0.5 0.5 1) (e1 -1 1 0) (e2 1 1 0) (e3 0 0 1))
    )
  )
)

;; (define e1 (vector3 -1 1 0))
;; (define e2 (vector3 -1 -1 2))
;; (define e3 (vector3 1 1 1))
;; 
;; (define e1 (vector3 -1 1 0))
;; (define e2 (vector3 1 1 2))
;; (define e3 (vector3 1 1 -1))
;; 
;; (define e1 (vector3 -1 1 0))
;; (define e2 (vector3 1 1 2))
;; (define e3 (vector3 1 1 -1))
;; 
;; (define e1 (vector3 -1 1 0))
;; (define e2 (vector3 1 1 2))
;; (define e3 (vector3 1 1 -1))

(define ellipsoid_object (list-ref elliptical_cylinder 0) )
(define block_object (list-ref elliptical_cylinder 1) )

(define elliptical_cylinder2
  (let* ((w 0.1) (h 0.5) (L 0.5))
    (list
      (make ellipsoid (center 0 0 0)  (size w h infinity) (e1 -1 1 0) (e2 1 1 2) (e3 1 1 -1))
      (make block  (center 0 0 0)  (size 0.5 0.5 1) (e1 -1 1 0) (e2 1 1 0) (e3 0 0 1))
    )
  )
)

(define ellipsoid_object (list-ref elliptical_cylinder 0) )
(define block_object (list-ref elliptical_cylinder 1) )

(make cylinder  (center 0 0 0)  (axis 1 1 1)  (radius 0.1)  (height 1))

(define (ellipcyl-func point)
;; inside = false
;; for (ellipsoid, block) in ellip_cyl_list:
;;   if point in ellipsoid and point in block:
;;     inside = true


(define ellipsoid_object (list-ref elliptical_cylinder 0) )
(define block_object (list-ref elliptical_cylinder 1) )

(define ellipsoid_object2 (list-ref elliptical_cylinder2 0) )
(define block_object2 (list-ref elliptical_cylinder2 1) )


  (define inside false)
  (if (or
        (and (point-in-object? point ellipsoid_object) (point-in-object? point block_object))
        (and (point-in-object? point ellipsoid_object2) (point-in-object? point block_object2))
      )
    (set! inside true)
  )
  (if inside
    (make dielectric (index 4))
    (make dielectric (index 2))
  )
)

(set! default-material (make material-function (material-func ellipcyl-func)))

(set-param! mesh-size 1)
(set-param! resolution 32)

(run)
