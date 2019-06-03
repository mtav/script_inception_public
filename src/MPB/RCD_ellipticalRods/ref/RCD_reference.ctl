; normal RCD reference code

(define-param r 0.1)
(define-param n_inner 1.52 )
(define-param n_outer 1 )
(set-param! resolution 100)
(set-param! num-bands 10)
(set-param! filename-prefix "RCD_reference-")

;; (set! geometry-lattice (make lattice
;;                          (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
;;                          (basis1 0 1 1)
;;                          (basis2 1 0 1)
;;                          (basis3 1 1 0)))

;; export GUILE_LOAD_PATH=$HOME/Development/script_inception_public/reference/examples_MPB/woodpile_extendedDiagrams
(load-from-path "all_FCC_BZ_labels.ctl")

(set! k-points (interpolate num-k-points FCC_standard_kpoints ))

(define diel_inner (make dielectric (index n_inner)))
(define diel_outer (make dielectric (index n_outer)))

(set! default-material diel_outer)

(define (c->l . args) (cartesian->lattice (apply vector3 args)))

(define L (/ (sqrt 3) 4))

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

(run)

(exit)
