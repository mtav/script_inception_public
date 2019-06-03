;------------------------------------------------------------------
;; from the Imagawa paper:
;; n=3
;; d=3mm
;; r=0.26*d
;; d=sqrt(3)/4*a
;; r/a=0.26*sqrt(3)/4
;------------------------------------------------------------------

(define-param rod-height (/ (sqrt 3) 4) )
(define-param rod-radius (* 0.26 rod-height) )
(define-param rod-index 3)
(define-param backfill-index 1)


(define-param fmin (/ 0.18 rod-height))
(define-param fmax (/ 0.35 rod-height))

(define-param nfreq 500) ; number of frequencies at which to compute flux

(define-param is-reference? false) ; if true, have crystal, else vaccuum

;------------------------------------------------------------------
(set! geometry-lattice (make lattice (size 14 14 14)))
(set! resolution 16)

(set! default-material (make dielectric (index backfill-index) ) )
(set! pml-layers (list (make pml (thickness 1.0))))

(define fcen (* 0.5 (+ fmin fmax))) ; pulse center frequency
(define df 2)    ; pulse width (in frequency)

(define (tetra delta)
  (list
    (make cylinder
      (center (vector3+ (vector3 (/ -3 8) (/ -3 8) (/ -3 8)) delta ) )
      (material (make dielectric (index rod-index)) )
      (radius rod-radius)
      (height rod-height)
      (axis (vector3 1 1 1) )
    )
    (make cylinder
      (center (vector3+ (vector3 (/ -3 8) (/ -1 8) (/ -1 8)) delta ) )
      (material (make dielectric (index rod-index)) )
      (radius rod-radius)
      (height rod-height)
      (axis (vector3 -1 1 1) )
    )
    (make cylinder
      (center (vector3+ (vector3 (/ -1 8) (/ -3 8) (/ -1 8)) delta ) )
      (material (make dielectric (index rod-index)) )
      (radius rod-radius)
      (height rod-height)
      (axis (vector3 1 -1 1) )
    )
    (make cylinder
      (center (vector3+ (vector3 (/ -1 8) (/ -1 8) (/ -3 8)) delta ) )
      (material (make dielectric (index rod-index)) )
      (radius rod-radius)
      (height rod-height)
      (axis (vector3 1 1 -1) )
    )
  )
)

;; (define tetra
;;   (list
;;     (make cylinder
;;       (center (/ -3 8) (/ -3 8) (/ -3 8) )
;;       (material (make dielectric (index rod-index)) )
;;       (radius rod-radius)
;;       (height rod-height)
;;       (axis 1 1 1 )
;;     )
;;     (make cylinder
;;       (center (/ -3 8) (/ -1 8) (/ -1 8) )
;;       (material (make dielectric (index rod-index)) )
;;       (radius rod-radius)
;;       (height rod-height)
;;       (axis -1 1 1 )
;;     )
;;     (make cylinder
;;       (center (/ -1 8) (/ -3 8) (/ -1 8) )
;;       (material (make dielectric (index rod-index)) )
;;       (radius rod-radius)
;;       (height rod-height)
;;       (axis 1 -1 1)
;;     )
;;     (make cylinder
;;       (center (/ -1 8) (/ -1 8) (/ -3 8) )
;;       (material (make dielectric (index rod-index)) )
;;       (radius rod-radius)
;;       (height rod-height)
;;       (axis 1 1 -1)
;;     )
;;   )
;; )

;; (define lol
;;   (list
;;       (shift-geometric-object tetra (vector3 0   0   0  ))
;;       (shift-geometric-object tetra (vector3 0   0.5 0.5))
;;       (shift-geometric-object tetra (vector3 0.5 0   0.5))
;;       (shift-geometric-object tetra (vector3 0.5 0.5 0  ))
;;     )
;; )

(define unit-cell
  (append
;;     (tetra (vector3 0 0 0))
;;     (tetra (vector3 0   0.5 0.5))
;;     (tetra (vector3 0.5 0   0.5))
;;     (tetra (vector3 0.5 0.5 0  ))

    (tetra (vector3 0.5 0.5 0   ))
    (tetra (vector3 0.5 1   0.5 ))
    (tetra (vector3 1   0.5 0.5 ))
    (tetra (vector3 1   1   0   ))

  )
)

(if (not is-reference?)
  (set! geometry

    (geometric-objects-duplicates (vector3 1 0 0) -5 4
      (geometric-objects-duplicates (vector3 0 1 0) -5 4
        (geometric-objects-duplicates (vector3 0 0 1) -2 2
          unit-cell
        )
      )
    )

  ;;   (geometric-objects-lattice-duplicates unit-cell)
  )
)

(set! sources (list
               (make source
                 (src (make gaussian-src (frequency fcen) (fwidth df)))
                 (component Ex)
                 (center 0 0 (+ 1 (* -0.5 sz)))
                 (size 1 0 0))))

(init-fields)
(output-epsilon)
(exit)
