; This program simulates a triangular lattice

(define-param h .74)
(define-param r 0.25)
(define-param supercell-h 4)
(define-param eps 4.4521)
(define-param loweps 1)
(define diel (make dielectric (epsilon eps)))
(set! num-bands 8)
(set! geometry-lattice (make lattice(size 1 1 supercell-h)
(basis1 (/ (sqrt 3) 2) 0.5)
(basis2 (/ (sqrt 3) 2) -0.5)))

;(define-param sd (list 0 1))
;(set! sd (interpolate 5 sd))

(set! geometry (list
  (make block
  (center 0 0 0)(size 1 1 supercell-h)
  (material (make dielectric(epsilon loweps))))
  (make block
  (center 0 0 0)(size 1 1 h)
  (material (make dielectric(epsilon eps))))
  (make cylinder
  (center 0 0 0) (radius r) (height supercell-h)
  (axis 0 0 1)
  (material air))))

(define Gamma (vector3 0 0 0))
(define M (vector3 0 0.5 0))
(define K (vector3 (/ -3)(/ 3) 0))
(define Kreq (vector3 0 0.2 0))

(set! k-points (list Gamma ; Gamma
  M ; M
  K ; K
  Gamma)) ; Gamma

;(set! k-points (list ; Gamma
; M ; M
; K ; K
; )) ; Gamma
;

(set! k-points (interpolate 4 k-points))
(set! resolution 32)
  (run-tm)
  (run-te)

;(run-te (output-at-kpoint (vector3 0 0.5 0)
; (vector3 (/ -3)(/ 3) 0)
; fix-efield-phase output-efield-z))
;(run-zeven fix-efield-phase output-hfield-z)
;(run-tm (output-at-kpoint (vector3 0 0.5 0)(vector3 (/-3)(/ 3) 0) fix-hfield-phase output-h;field))