; validation runs:
; w=0.240 h=0.240 inside-index=1 outside-index=2.4
; w=0.200 h=0.200 inside-index=1.52 outside-index=1
; w=0.200 h=0.600 inside-index=1.52 outside-index=1
; w=0.300 h=0.600 inside-index=1.52 outside-index=1
; w=0.400 h=0.600 inside-index=1.52 outside-index=1

(define-param w 0.1)
(define-param h 0.2)
(define-param inside-index 4)
(define-param outside-index 2)
(define-param k-interp 10)
(set-param! mesh-size 3)
(set-param! resolution 10)
(set-param! num-bands 10)

; times:
;; mesh-size 3, resolution 32, num-bands 10, k-interp 10 -> 24m49.576s

;; export GUILE_LOAD_PATH=$HOME/Development/script_inception_public/reference/examples_MPB/woodpile_extendedDiagrams
(load-from-path "all_FCC_BZ_labels.ctl")

;; (set! geometry-lattice (make lattice
;;                          (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
;;                          (basis1 0 1 1)
;;                          (basis2 1 0 1)
;;                          (basis3 1 1 0)))

(define L (/ (sqrt 3) 4))

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
  (get_components rod0)
  (get_components rod1)
  (get_components rod2)
  (get_components rod3)
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

; (set! k-points (interpolate k-interp FCC_standard_kpoints ))
(set_kpoints FCC_standard_kpoints)

;; ; for a quick test run
;; (set! default-material (make dielectric (index 1)))
;; (set! k-points (list))
;; (set! num-bands 1)

(init+output-epsilon-mpb)

;; (run)
(exit)
