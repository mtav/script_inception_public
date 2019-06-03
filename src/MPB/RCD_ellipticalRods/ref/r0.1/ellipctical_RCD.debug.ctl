; validation runs:
; w=0.240 h=0.240 inside-index=1 outside-index=2.4
; w=0.200 h=0.200 inside-index=1.52 outside-index=1
; w=0.200 h=0.600 inside-index=1.52 outside-index=1
; w=0.300 h=0.600 inside-index=1.52 outside-index=1
; w=0.400 h=0.600 inside-index=1.52 outside-index=1

(define-param w 0.2)
(define-param h 0.2)
(define-param inside-index 1)
(define-param outside-index 2.4)
(define-param num-k-points 10)
(set-param! mesh-size 3)
(set-param! resolution 32)
(set-param! num-bands 10)
(set-param! filename-prefix "ellip-")

; times:
;; mesh-size 3, resolution 32, num-bands 10, num-k-points 10 -> 24m49.576s

;; export GUILE_LOAD_PATH=$HOME/Development/script_inception_public/reference/examples_MPB/woodpile_extendedDiagrams
(load-from-path "all_FCC_BZ_labels.ctl")

;; (set! geometry-lattice (make lattice
;;                          (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
;;                          (basis1 0 1 1)
;;                          (basis2 1 0 1)
;;                          (basis3 1 1 0)))

(define (c->l . args) (cartesian->lattice (apply vector3 args)))
(define (l->c . args) (lattice->cartesian (apply vector3 args)))

(define-class elliptical-cylinder-RCD geometric-object
  ; class specifically meant for elliptical cylinders used in RCD, with the cartesian Z-axis always in the "cutoff-planes".
  (define-post-processed-property axis (vector3 0 0 1) 'vector3 unit-vector3)
  (define-property size-vertical no-default 'number non-negative?)
  (define-property size-horizontal no-default 'number non-negative?)
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
  (let*
  
    ; local variables
    (
      ; centers
      ( ellipsoid-center (object-property-value ell-cyl-RCD 'center) )
      ( block-center (object-property-value ell-cyl-RCD 'center) )

      ; axes
      ( block-e2 (vector3 0 0 1) )
      ( block-e3 (lattice->cartesian (object-property-value ell-cyl-RCD 'axis)) )
      ( block-e1 (vector3-cross block-e2 block-e3) )

      ( ellipsoid-e3 block-e3 )
      ( ellipsoid-e1 block-e1 )
      ( ellipsoid-e2 (vector3-cross ellipsoid-e3 ellipsoid-e1) )

      ; sizes
      (h (object-property-value ell-cyl-RCD 'size-vertical) )
      (w (object-property-value ell-cyl-RCD 'size-horizontal) )
      (hz (projected-distance h ellipsoid-e2 block-e2) )
      ( ellipsoid-size (vector3 w h infinity ) )
      ( block-size (vector3 w hz (object-property-value ell-cyl-RCD 'height) ) )
    )

    ; return value
    (list
      (make ellipsoid
        (center ellipsoid-center)
        (e1 (cartesian->lattice ellipsoid-e1))
        (e2 (cartesian->lattice ellipsoid-e2))
        (e3 (cartesian->lattice ellipsoid-e3))
        (size ellipsoid-size)
      )
      (make block
        (center block-center)
        (e1 (cartesian->lattice block-e1))
        (e2 (cartesian->lattice block-e2))
        (e3 (cartesian->lattice block-e3))
        (size block-size)
      )
    )
  )
)

(define L (/ (sqrt 3) 4))

(define rod-center (make elliptical-cylinder-RCD
  (center (c->l 0 0 0))
  (axis (c->l 1 1 1))
  (size-horizontal w)
  (size-vertical h)
  (height L )
))

(define rod0 (make elliptical-cylinder-RCD
  (center (c->l (/ -3 8) (/ -3 8) (/ -3 8)))
  (axis (c->l 1 1 1))
  (size-horizontal w)
  (size-vertical h)
  (height L )
))

(define rod1 (make elliptical-cylinder-RCD
  (center (c->l (/ -3 8) (/ -1 8) (/ -1 8)))
  (axis (c->l -1 1 1))
  (size-horizontal w)
  (size-vertical h)
  (height L )
))

(define rod2 (make elliptical-cylinder-RCD
  (center (c->l (/ -1 8) (/ -3 8) (/ -1 8)))
  (axis (c->l 1 -1 1))
  (size-horizontal w)
  (size-vertical h)
  (height L )
))

(define rod3 (make elliptical-cylinder-RCD
  (center (c->l (/ -1 8) (/ -1 8) (/ -3 8)))
  (axis (c->l 1 1 -1))
  (size-horizontal w)
  (size-vertical h)
  (height L )
))

(define rod-list (list
  (get_components rod-center)
;;   (get_components rod0)
;;   (get_components rod1)
;;   (get_components rod2)
;;   (get_components rod3)
))

(define (RCD-func point-lattice)
  (define inside false)
  (map
    (lambda (rod)
      (if
        (and
          (point-in-periodic-object? point-lattice (list-ref rod 0))
          (point-in-periodic-object? point-lattice (list-ref rod 1))
        )
        (set! inside true)
      )
    )
    ;list of rods to go through
    rod-list
  )
  (if inside
    (make dielectric (index inside-index))
    (make dielectric (index outside-index))
  )
)

(set! default-material (make material-function (material-func RCD-func)))

(set! k-points (interpolate num-k-points FCC_standard_kpoints ))

;; ; for a quick test run
;; (set! default-material (make dielectric (index 1)))
(set! k-points (list))
(set! num-bands 1)

(run)
