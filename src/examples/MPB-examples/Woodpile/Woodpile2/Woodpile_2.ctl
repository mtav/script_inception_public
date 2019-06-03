(set! geometry-lattice (make lattice
                         (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
                         (basis1 0 1 1)
                         (basis2 1 0 1)
                         (basis3 1 1 0)))

; Corners of the irreducible Brillouin zone for the fcc lattice,
; in a canonical order:
(set! k-points (interpolate 4 (list
                               (vector3 0 0.5 0.5)            ; X
                               (vector3 0 0.625 0.375)        ; U
                               (vector3 0 0.5 0)              ; L
                               (vector3 0 0 0)                ; Gamma
                               (vector3 0 0.5 0.5)            ; X
                               (vector3 0.25 0.75 0.5)        ; W
                               (vector3 0.375 0.75 0.375))))  ; K

; define a couple of parameters (which we can set from the command-line)
(define-param eps 1) ; the dielectric constant of the cylinders
(define-param r 0.1)    ; the radius of the cylinders
; woodpile lattice ; using diamond lattice from the example files:
; Dielectric spheres in a diamond (fcc) lattice.  This file is used in
; the "Data Analysis Tutorial" section of the MPB manual.

(define si (make dielectric (epsilon eps)))


(set! geometry (list
                (make cylinder
                  (center 0 0 0) (radius r) (axis (vector3 1 1 0))
                  (height infinity) (material si))
                (make cylinder
                  (center 0 0 (/ 1 4)) (radius r) (axis (vector3 1 -1 0))
                  (height infinity) (material si))
                (make cylinder

(center 0 (/ 1 2) (/ 2 4)) (radius r) (axis (vector3 1 1 0))

                  (height infinity) (material si))
                (make cylinder

(center 0 (/ 1 2) (/ 3 4)) (radius r) (axis (vector3 1 -1 0))

                  (height infinity) (material si))
                ))


(set-param! resolution 24) (set-param! num-bands 10)

(run)
