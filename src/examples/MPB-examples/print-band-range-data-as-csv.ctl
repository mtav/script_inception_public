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
(define-param eps 11.56) ; the dielectric constant of the spheres
(define-param r 0.25)    ; the radius of the spheres

(define diel (make dielectric (epsilon eps)))

; A diamond lattice has two "atoms" per unit cell:
(set! geometry (list (make sphere (center 0.125 0.125 0.125) (radius r)
                          (material diel))
                    (make sphere (center -0.125 -0.125 -0.125) (radius r)
                          (material diel))))

; (A simple fcc lattice would have only one sphere/object at the origin.)

(set-param! resolution 16) ; use a 16x16x16 grid
(set-param! mesh-size 5)
(set-param! num-bands 5)

(define (print-gap-list-as-csv L)
  (if (>= (length L) 1)
    (begin
      (let ( (first-gap (list-ref L 0)) )
        (print (length L) "; " (list-ref first-gap 0) "; " (list-ref first-gap 1) "; " (list-ref first-gap 2) ";\n")
      )
    )
    (begin
      (print (length L) "; " "-1" "; " "-1" "; " "-1" ";\n")
    )
  )
)

(define (print-band-range-data-as-csv L)
  (let
    ((foo ; this let statement is just so that map does not lead to a returned list (i.e. for clean printing output)
      (map (lambda (x)
;;         (print "===> " x "\n")
        (let 
          (
            (min_value  (car (car x)))
            (min_kpoint (cdr (car x)))
            (max_value  (car (cdr x)))
            (max_kpoint (cdr (cdr x)))
          )
          (print min_value "; ")
          (print (vector3-x min_kpoint) "; " (vector3-y min_kpoint) "; " (vector3-z min_kpoint) "; ")
          (print max_value "; ")
          (print (vector3-x max_kpoint) "; " (vector3-y max_kpoint) "; " (vector3-z max_kpoint) "; ")
        )
;;         (print "====\n")
      ) L )
    ))
    (print "\n")
  )
)

; This define inside define placement works.
(define (func_a x)
  (define koko 5)
  (if (< x 0)
    (begin (* koko x))
    (begin (+ koko x))
  )
)

; This define inside define placement does not work.
(define (func_b x)
  (if (< x 0)
    (begin (define koko 5) (* koko x)) 
    (begin (define koko 3) (+ koko x))
  )
)

; When define cannot be used, just use the let statement.
(define (func_c x)
  (if (< x 0)
  (let ((koko 5)) (* koko x))
  (let ((koko 3)) (+ koko x)))
)
