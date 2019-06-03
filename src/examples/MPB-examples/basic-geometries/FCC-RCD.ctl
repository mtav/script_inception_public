; basic FCC-RCD geometry

(load-from-path "all_FCC_BZ_labels.ctl")

(define-param cube-size 1 )
(define-param rod-height (* (/ (sqrt 3) 4) cube-size) )

;; (define-param rod-radius 0.10 )
;; (define-param rod-index 3.6 )
;; (define-param backfill-index 1 )

(define-param rod-radius 0.27 )
(define-param rod-index 1 )
(define-param backfill-index 3.6 )

(set-param! resolution 32)
(set-param! num-bands 12)
(set-param! mesh-size 3)

(define-param num-k-points 10)

(set! default-material (make dielectric (index backfill-index) ) )
(define rod-material (make dielectric (index rod-index)))

; point definitions in FCC lattice coordinates
(define p000 (vector3 0 0 0))
(define p100 (vector3 1 0 0))
(define p010 (vector3 0 1 0))
(define p001 (vector3 0 0 1))
(define pmid1 (vector3 0.25 0.25 0.25))

(define (cylinder_from_A_to_B A B r h mat)
  (make cylinder
    (material mat)
    (center (vector3* 0.5 (vector3+ A B)) )
    (radius r)
    (height h )
    (axis (vector3- B A) )
  )
)

(set! geometry (list
  (cylinder_from_A_to_B pmid1 p000 rod-radius rod-height rod-material)
  (cylinder_from_A_to_B pmid1 p100 rod-radius rod-height rod-material)
  (cylinder_from_A_to_B pmid1 p010 rod-radius rod-height rod-material)
  (cylinder_from_A_to_B pmid1 p001 rod-radius rod-height rod-material)
))

;; (set! k-points (list))
;; (set! k-points (interpolate num-k-points (list
;; Gamma
;; X+z
;; U+z+x+y
;; L+x+y+z
;; K+x+y
;; Gamma
;; X+z
;; W+z+x
;; K+x+z
;; W+x+z
;; X+x
;; )))
;; (set! k-points (interpolate k-interp FCC_standard_kpoints))
(set_kpoints FCC_standard_kpoints)

(run)

(exit)
