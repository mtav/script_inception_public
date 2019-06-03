;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; defines a generic "face-centred orthorhombic lattice" with cell edges of length _a,_b,_c
;;
;; if _a != _b != _c: orthorhombic-F (face-centred)
;; if _a == _b != _c: tetragonal-I (body-centred/face-centred)
;; if _a == _b == _c: cubic-F (fcc, face-centred)
;;
;; cf: http://en.wikipedia.org/wiki/Bravais_lattice
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; To load:
;; (load-from-path "lattice_orthorhombic_face-centred.ctl")
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(load-from-path "utilities_mpb.ctl")
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; The following variables should be defined before calling this script. However, if they are not previously set, this sets the default values.

; dimensions of the orthorhombic unit-cell
(define-param _a 1)
(define-param _b 2)
(define-param _c 3)

; dimensions of the super-cell if you use one (used as lattice size parameters)
(define-param _S1 1)
(define-param _S2 1)
(define-param _S3 1)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(if verbose?
  (begin
    (print "<----------------------------------------------\n")
    (print "Loading lattice_orthorhombic.ctl with:\n")
    (print "  _a = " _a "\n")
    (print "  _b = " _b "\n")
    (print "  _c = " _c "\n")
    (print "  _S1 = " _S1 "\n")
    (print "  _S2 = " _S2 "\n")
    (print "  _S3 = " _S3 "\n")
  )
)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; lattice definition
(set! geometry-lattice (make lattice
  (size
    _S1
    _S2
    _S3
  )
  (basis-size
    _a
    _b
    _c
  )
))

;; size of the "super-cell cube"
(define _A (* _S1 _a))
(define _B (* _S2 _b))
(define _C (* _S3 _c))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Corners of the irreducible/first Brillouin zone for a generic orthorhombic lattice.
; NOTE: k-points are specified in the reciprocal lattice!!! (the reciprocal of the specified geometry-lattice)

; Gamma point
(define Gamma (cons "Gamma" (vector3 0 0 0)))

; X points: X_i = 0.5*i
(define X+x (cons "X+x" (vector3  0.5  0    0  )))
(define X-x (cons "X-x" (vector3 -0.5  0    0  )))
(define X+y (cons "X+y" (vector3  0    0.5  0  )))
(define X-y (cons "X-y" (vector3  0   -0.5  0  )))
(define X+z (cons "X+z" (vector3  0    0    0.5)))
(define X-z (cons "X-z" (vector3  0    0   -0.5)))

; A points: A_ijk = 0.5*(i+j+k)
(define A+x+y+z (cons "A+x+y+z" (vector3  0.5  0.5  0.5)))
(define A+x+y-z (cons "A+x+y-z" (vector3  0.5  0.5 -0.5)))
(define A+x-y+z (cons "A+x-y+z" (vector3  0.5 -0.5  0.5)))
(define A+x-y-z (cons "A+x-y-z" (vector3  0.5 -0.5 -0.5)))
(define A-x+y+z (cons "A-x+y+z" (vector3 -0.5  0.5  0.5)))
(define A-x+y-z (cons "A-x+y-z" (vector3 -0.5  0.5 -0.5)))
(define A-x-y+z (cons "A-x-y+z" (vector3 -0.5 -0.5  0.5)))
(define A-x-y-z (cons "A-x-y-z" (vector3 -0.5 -0.5 -0.5)))

; M points: M_ij = 0.5*(i+j)
(define M+x+y (cons "M+x+y" (vector3  0.5  0.5  0  )))
(define M+x-y (cons "M+x-y" (vector3  0.5 -0.5  0  )))
(define M-x+y (cons "M-x+y" (vector3 -0.5  0.5  0  )))
(define M-x-y (cons "M-x-y" (vector3 -0.5 -0.5  0  )))

(define M+y+z (cons "M+y+z" (vector3  0    0.5  0.5)))
(define M+y-z (cons "M+y-z" (vector3  0    0.5 -0.5)))
(define M-y+z (cons "M-y+z" (vector3  0   -0.5  0.5)))
(define M-y-z (cons "M-y-z" (vector3  0   -0.5 -0.5)))

(define M+x+z (cons "M+x+z" (vector3  0.5  0    0.5)))
(define M+x-z (cons "M+x-z" (vector3  0.5  0   -0.5)))
(define M-x+z (cons "M-x+z" (vector3 -0.5  0    0.5)))
(define M-x-z (cons "M-x-z" (vector3 -0.5  0   -0.5)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; canonical lists for convenience
(define kpoints_X (list
  X+x
  X-x
  X+y
  X-y
  X+z
  X-z
))

(define kpoints_A (list
  A+x+y+z
  A+x+y-z
  A+x-y+z
  A+x-y-z
  A-x+y+z
  A-x+y-z
  A-x-y+z
  A-x-y-z
))

(define kpoints_M (list
  M+x+y
  M+x-y
  M-x+y
  M-x-y
  M+y+z
  M+y-z
  M-y+z
  M-y-z
  M+x+z
  M+x-z
  M-x+z
  M-x-z
))

(define kpoints_all (append
  (list Gamma)
  kpoints_X
  kpoints_A
  kpoints_M
))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(if verbose?
  (begin
    (print "---------------------------------------------->\n")
  )
)
