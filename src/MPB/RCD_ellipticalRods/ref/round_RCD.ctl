; validation runs:
; w=0.240 h=0.240 inside-index=1 outside-index=2.4
; w=0.200 h=0.200 inside-index=1.52 outside-index=1
; w=0.200 h=0.600 inside-index=1.52 outside-index=1
; w=0.300 h=0.600 inside-index=1.52 outside-index=1
; w=0.400 h=0.600 inside-index=1.52 outside-index=1

(define-param r 0.24)
(define-param inside-index 1)
(define-param outside-index 2.4)
(define-param num-k-points 10)
(set-param! mesh-size 3)
(set-param! resolution 32)
(set-param! num-bands 10)

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

(define L (/ (sqrt 3) 4))

(define diel_inner (make dielectric (index inside-index)))
(define diel_outer (make dielectric (index outside-index)))

(set! geometry (list
  (make cylinder
    (center (c->l (/ -3 8) (/ -3 8) (/ -3 8)))
    (axis (c->l 1 1 1))
    (radius r)
    (height L)
    (material diel_inner))
  (make cylinder
    (center (c->l (/ -3 8) (/ -1 8) (/ -1 8)))
    (axis (c->l -1 1 1))
    (radius r)
    (height L)
    (material diel_inner))
  (make cylinder
    (center (c->l (/ -1 8) (/ -3 8) (/ -1 8)))
    (axis (c->l 1 -1 1))
    (radius r)
    (height L)
    (material diel_inner))
  (make cylinder
    (center (c->l (/ -1 8) (/ -1 8) (/ -3 8)))
    (axis (c->l 1 1 -1))
    (radius r)
    (height L)
    (material diel_inner))
))

(set! default-material diel_outer)

; general k-points
(set! k-points (interpolate num-k-points FCC_standard_kpoints ))

; from photon14 talk
;; (set! k-points (interpolate num-k-points (list
;;   Gamma
;;   X+z
;;   U+z+x+y
;;   L+x+y+z
;;   K+x+y
;;   Gamma
;;   W+z+x
;;   K+x+z
;;   W+x+z
;;   X+x
;; ) ))

;; ; for a quick test run
;; (set! default-material (make dielectric (index 1)))
;; (set! k-points (list))
;; (set! num-bands 1)

(run)
