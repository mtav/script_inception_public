; Air spheres in a diamond (fcc) lattice TiO2.  This file is used in
; the "Data Analysis Tutorial" section of the MPB manual.

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
(define-param eps 1) ; the dielectric constant of the spheres
(define-param r 0.25)    ; the radius of the spheres

(define diel (make dielectric (epsilon eps)))


; A diamond lattice has two "atoms" per unit cell:
(set! geometry (list (make sphere (center 0.125 0.125 0.125) (radius r) 
         (material diel))
         (make sphere (center -0.125 -0.125 -0.125) (radius r) 
         (material diel))))

; define the dielectric constant of TiO2 background	   
(define TiO2 (make dielectric (epsilon 6.76))) ; TiO2
(set! default-material TiO2) ; background


; (A simple fcc lattice would have only one sphere/object at the origin.)

(set-param! resolution 16) ; use a 16x16x16 grid
(set-param! mesh-size 5)
(set-param! num-bands 5)

; run calculation, outputting electric-field energy density at the U point:
(run (output-at-kpoint (vector3 0 0.625 0.375) output-dpwr))

(load-from-path "dos.scm")
(print-dos 0 1 100)
