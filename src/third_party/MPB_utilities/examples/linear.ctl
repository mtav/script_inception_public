; x linear lattice of layers
;
; Layer thickness is R*Lattice size
; Layer permitivity is E*Eo
;
; +------------------+
; | Input parameters |
; +------------------+
;

(define n1 1)
(define n2 3.5)

(define t1 (/ n2 (+ n1 n2)))
(define t2 (/ n1 (+ n1 n2)))

;; (define-param E 8)
;; (define-param R 0.5)
(define-param E (* n2 n2))
(define-param R t2)

;
; +----------------+
; | Setup geometry |
; +----------------+
;
(set! geometry (list
  (make block
    (center 0 0 0)
    (size R infinity infinity)
    (material (make dielectric (epsilon E)))
  )
))
;
; +--------------+
; | Quantization |
; +--------------+
;
(set! resolution (vector3 32 1 1))

(set! k-points (list
;;   (vector3 -0.5 0 0)
  ; -X
  (vector3 0 0 0)
  ; G
  (vector3 0.5 0 0)
  ; X
))

(set! k-points (interpolate 32 k-points)) ; total of 34 points
(set! num-bands 20)
(run-te display-group-velocities
; (output-at-kpoint (vector3 0.5 0 0) fix-efield-phase output-efield-y)
)
