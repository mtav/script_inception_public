(define-class molotov geometric-object
  (define-post-processed-property axis (vector3 0 0 1) 'vector3 unit-vector3)
  (define-property radius no-default 'number non-negative?)
  (define-property height no-default 'number non-negative?)
  (define-property fufu no-default 'number non-negative?)
)

(define lol
  (make molotov
    (material (make dielectric (index 4)))
    (center 0 0 0.25)
    (radius 0.1)
    (height 0.5)
    (axis 1 1 -1)
    (fufu 56)
  )
)

(define lal
  (make cylinder
    (material (make dielectric (index 4)))
    (center 0 0 0.25)
    (radius 0.1)
    (height 0.5)
    (axis 1 1 -1)
  )
)

(define-class elliptical-cylinder-RCD geometric-object
  ; class specifically meant for elliptical cylinders used in RCD, with the cartesian Z-axis always in the "cutoff-planes".
  (define-post-processed-property axis (vector3 0 0 1) 'vector3 unit-vector3)
  (define-property radius-vertical no-default 'number non-negative?)
  (define-property radius-horizontal no-default 'number non-negative?)
  (define-property height no-default 'number non-negative?)
)

(define (projected-distance d u v)
; d: distance to project
; u: vector direction of d
; v: vector direction to project on
; returns d' = abs( d / cos(angle(u,v)) )
; with cos(angle(u,v)) = dot(u,v)/(norm(u)*norm(v))
(abs (/ d (/ (vector3-dot u v) (* (vector3-norm u) (vector3-norm v)))))
)

(define (get_components ell-cyl-RCD)
  ; TODO: l->c, c->l
  (let*
  
    ; local variables
    (
      ; centers
      ( ellipsoid-center (object-property-value ell-cyl-RCD 'center) )
      ( block-center (object-property-value ell-cyl-RCD 'center) )

      ; axes
      ( block-e2 (vector3 0 0 1) )
      ( block-e3 (object-property-value ell-cyl-RCD 'axis) )
      ( block-e1 (vector3-cross block-e2 block-e3) )

      ( ellipsoid-e3 (object-property-value ell-cyl-RCD 'axis) )
      ( ellipsoid-e1 block-e1)
      ( ellipsoid-e2 (vector3-cross ellipsoid-e3 ellipsoid-e1) )

      ; sizes
      (h (object-property-value ell-cyl-RCD 'radius-vertical) )
      (w (object-property-value ell-cyl-RCD 'radius-horizontal) )
      (hz (projected-distance h ellipsoid-e2 block-e2) )
      ( ellipsoid-size (vector3 w h infinity ) )
      ( block-size (vector3 w hz (object-property-value ell-cyl-RCD 'height) ) )
    )

    ; return value
    (list
      (make ellipsoid (center ellipsoid-center)  (size ellipsoid-size) (e1 ellipsoid-e1) (e2 ellipsoid-e2) (e3 ellipsoid-e3))
      (make block  (center block-center)  (size block-size) (e1 block-e1) (e2 block-e2) (e3 block-e3))
    )
  )
)

(define rod0 (make elliptical-cylinder-RCD
  (center (/ -1 8) (/ -1 8) (/ -1 8))
  (axis 1 1 1)
  (radius-horizontal 0.2)
  (radius-vertical 0.5)
  (height (/ (sqrt 3) 4) )
))

(define rod1 (make elliptical-cylinder-RCD
  (center (/ 1 8) (/ 1 8) (/ -1 8))
  (axis 1 1 -1)
  (radius-horizontal 0.2)
  (radius-vertical 0.5)
  (height (/ (sqrt 3) 4) )
))

(define rod-list (list
  (get_components rod0)
  (get_components rod1)
))

;; (define point (vector3 0 0 1))
;; 
;; (print "inside: " inside "\n")

(define (RCD-func point)
  (define inside false)
  (map
    (lambda (rod)
      (if
        (and
          (point-in-object? point (list-ref rod 0))
          (point-in-object? point (list-ref rod 1))
        )
        (set! inside true)
      )
    )
    ;list of rods to go through
    rod-list
  )
  (if inside
    (make dielectric (index 4))
    (make dielectric (index 2))
  )
)

;; (define (point-in-RCD? point obj)
;; 
;; ret=false
;; for i in obj:
;;   if p in i[0] and p in i[1]:
;;    ret=true
;;       
;; ret
;; )
;; 
;; (let
;;   (obj-list (get_components rod))
;;   
;; )
;; 
;; )
;; 
;; 
;; (define mylist (get_components toto))
;; 
;; 
;; 
(set! default-material (make material-function (material-func RCD-func)))
;; 
;; (set-param! mesh-size 1)
;; (set-param! resolution 32)
;; 
(run)
