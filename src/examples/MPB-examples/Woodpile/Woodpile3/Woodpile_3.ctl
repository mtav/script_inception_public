; Woodpile structure.  Note that a general woodpile is an fct lattice,

; but with the correct log height it is fcc, and that is what is used here.

; (It turns out that the optimal structure is pretty close to fcc
; anyway, so we don't gain much by going to fct.)

(set! geometry-lattice (make lattice
                         (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
                         (basis1 0 1 1)
                         (basis2 1 0 1)
                         (basis3 1 1 0)))

(define-param k-interp 9)

; Corners of the irreducible Brillouin zone for the fcc lattice,
; in a canonical order.  In this case, woodpile breaks some of
; the symmetry so we have additional points W'', X', etc.
(define X (vector3 0 0.5 0.5))
(define U (vector3 0.25 0.625 0.625))
(define L (vector3 0.5 0.5 0.5))
(define Gamma (vector3 0 0 0))
(define W (vector3 0.25 0.5 0.75))
(define K (vector3 0.375 0.375 0.75))

; inequivalent points due to broken symmetry
(define W'' (rotate-reciprocal-vector3 X (deg->rad 90) W))
(define X' (vector3 0.5 0.5 0)) ; z (stacking) direction
(define K' (rotate-reciprocal-vector3 L (deg->rad -120) K))
(define W' (rotate-reciprocal-vector3 L (deg->rad -120) W))
(define U' (rotate-reciprocal-vector3 L (deg->rad -120) U))


(set! k-points (interpolate k-interp (list X U L Gamma W K X' U' W' K' W'')))

(define-param eps 13) ; the dielectric constant of the "log" material

(define diel (make dielectric (epsilon eps)))

(define-param w 0.20) ; width of the logs

(define-param h 0.25) ; height of logs (should be 1/4 for fcc to not overlap)

; shortcut for cartesian->lattice function:
(define (c->l . args) (cartesian->lattice (apply vector3 args)))

(set! geometry
        (list
         (make block (material diel)
               (center (c->l 0 0 0))
               (e1 (c->l 1 1 0))
               (e2 (c->l 1 -1 0))
               (e3 (c->l 0 0 1))
               (size infinity w h))
         (make block (material diel)
               (center (c->l 0.125 0.125 h))
               (e1 (c->l 1 1 0))
               (e2 (c->l 1 -1 0))
               (e3 (c->l 0 0 1))
               (size w infinity h))))

(set-param! resolution 32)
(set-param! num-bands 10)
(run)
