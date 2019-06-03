; First BZ points for generic FCT lattices
; WARNING: Does not check to make sure the passed _a,_b,_c parameters lead to a valid FCT lattice!

; example usage (enable (exit) at end of this script for these to work):
; BCC: mpb _c=0.70710678118654746 all_FCT_BZ_labels.ctl > FCT-BZ-points_BCC.txt
; mpb _c=0.8 all_FCT_BZ_labels.ctl > FCT-BZ-points_c0.8.txt
; mpb _c=0.9 all_FCT_BZ_labels.ctl > FCT-BZ-points_c0.9.txt
; FCC: mpb _c=1 all_FCT_BZ_labels.ctl > FCT-BZ-points_FCC.txt

; Loading:
; in .bashrc or equivalent:
;   export GUILE_LOAD_PATH=$HOME/Development/script_inception_public/MPB/library
; in .ctl file:
;   (load-from-path "all_FCT_BZ_labels.ctl")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; The following variables should be defined before calling this script. However, if they are not previously set, this sets the default values.

; dimensions of the cubic unit-cell
(define-param _a 1)
(define-param _b 1)
(define-param _c 0.8) ; FCC if _c = _a = _b to BCC if _c = _a/sqrt(2) = _b/sqrt(2)

; dimensions of the super-cell if you use one (used as lattice size parameters)
; Note: only homogeneous scaling used at the moment, as inhomogeneous scaling can deform the unit-cell so much that the first Brillouin zone coordinates would have to be redefined in a more complex way.
(define-param _S 1)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; FCT lattice basis definition.
; NOTE: basis1, basis2 and basis3 are normalized to be as long as specified in "basis-size".

; lattice basis vectors
(define _a1 (vector3 0          (* 0.5 _b) (* 0.5 _c) ) )
(define _a2 (vector3 (* 0.5 _a) 0          (* 0.5 _c) ) )
(define _a3 (vector3 (* 0.5 _a) (* 0.5 _b) 0          ) )

; size of the "super-cell cube"
(define _A (* _S _a))
(define _B (* _S _b))
(define _C (* _S _c))

(set! geometry-lattice (make lattice
  (size
    _S
    _S
    _S
  )
  (basis-size
    (vector3-norm _a1)
    (vector3-norm _a2)
    (vector3-norm _a3)
  )
  (basis1 _a1)
  (basis2 _a2)
  (basis3 _a3))
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Corners of the irreducible/first Brillouin zone for a generic FCT lattice.
; NOTE: k-points are specified in the reciprocal lattice!!! (the reciprocal of the specified geometry-lattice)

; Gamma point
(define Gamma (cons "Gamma" (vector3 0 0 0)))

; X points: X_i
(define X+x (cons "X+x" (vector3  0    0.5  0.5)))
(define X-x (cons "X-x" (vector3  0   -0.5 -0.5)))
(define X+y (cons "X+y" (vector3  0.5  0    0.5)))
(define X-y (cons "X-y" (vector3 -0.5  0   -0.5)))
(define X+z (cons "X+z" (vector3  0.5  0.5  0  )))
(define X-z (cons "X-z" (vector3 -0.5 -0.5  0  )))

; L points: L_ijk
(define L+x+y+z (cons "L+x+y+z" (vector3  0.5  0.5  0.5)))
(define L-x-y-z (cons "L-x-y-z" (vector3 -0.5 -0.5 -0.5)))

(define L-x+y+z (cons "L-x+y+z" (vector3  0.5  0    0  )))
(define L+x-y-z (cons "L+x-y-z" (vector3 -0.5  0    0  )))

(define L+x-y+z (cons "L+x-y+z" (vector3  0    0.5  0  )))
(define L-x+y-z (cons "L-x+y-z" (vector3  0   -0.5  0  )))

(define L+x+y-z (cons "L+x+y-z" (vector3  0    0    0.5)))
(define L-x-y+z (cons "L-x-y+z" (vector3  0    0   -0.5)))

; define intermediate variables
(define _s_x (+ (/ -1 (expt _A 2)) (/  1 (expt _B 2)) (/  1 (expt _C 2)) ) )
(define _s_y (+ (/  1 (expt _A 2)) (/ -1 (expt _B 2)) (/  1 (expt _C 2)) ) )
(define _s_z (+ (/  1 (expt _A 2)) (/  1 (expt _B 2)) (/ -1 (expt _C 2)) ) )

; W points:
(define W+x+y (cons "W+x+y" (cartesian->reciprocal (vector3 (/  1 _A)             (* (/    _B  2) _s_x) 0                     ))))
(define W+x-y (cons "W+x-y" (cartesian->reciprocal (vector3 (/  1 _A)             (* (/ (- _B) 2) _s_x) 0                     ))))
(define W+x+z (cons "W+x+z" (cartesian->reciprocal (vector3 (/  1 _A)             0                     (* (/    _C  2) _s_x) ))))
(define W+x-z (cons "W+x-z" (cartesian->reciprocal (vector3 (/  1 _A)             0                     (* (/ (- _C) 2) _s_x) ))))

(define W-x+y (cons "W-x+y" (cartesian->reciprocal (vector3 (/ -1 _A)             (* (/    _B  2) _s_x) 0                     ))))
(define W-x-y (cons "W-x-y" (cartesian->reciprocal (vector3 (/ -1 _A)             (* (/ (- _B) 2) _s_x) 0                     ))))
(define W-x+z (cons "W-x+z" (cartesian->reciprocal (vector3 (/ -1 _A)             0                     (* (/    _C  2) _s_x) ))))
(define W-x-z (cons "W-x-z" (cartesian->reciprocal (vector3 (/ -1 _A)             0                     (* (/ (- _C) 2) _s_x) ))))

(define W+y+x (cons "W+y+x" (cartesian->reciprocal (vector3 (* (/    _A  2) _s_y) (/  1 _B)             0                     ))))
(define W+y-x (cons "W+y-x" (cartesian->reciprocal (vector3 (* (/ (- _A) 2) _s_y) (/  1 _B)             0                     ))))
(define W+y+z (cons "W+y+z" (cartesian->reciprocal (vector3 0                     (/  1 _B)             (* (/    _C  2) _s_y) ))))
(define W+y-z (cons "W+y-z" (cartesian->reciprocal (vector3 0                     (/  1 _B)             (* (/ (- _C) 2) _s_y) ))))

(define W-y+x (cons "W-y+x" (cartesian->reciprocal (vector3 (* (/    _A  2) _s_y) (/ -1 _B)             0                     ))))
(define W-y-x (cons "W-y-x" (cartesian->reciprocal (vector3 (* (/ (- _A) 2) _s_y) (/ -1 _B)             0                     ))))
(define W-y+z (cons "W-y+z" (cartesian->reciprocal (vector3 0                     (/ -1 _B)             (* (/    _C  2) _s_y) ))))
(define W-y-z (cons "W-y-z" (cartesian->reciprocal (vector3 0                     (/ -1 _B)             (* (/ (- _C) 2) _s_y) ))))

(define W+z+x (cons "W+z+x" (cartesian->reciprocal (vector3 (* (/    _A  2) _s_z) 0                     (/  1 _C)             ))))
(define W+z-x (cons "W+z-x" (cartesian->reciprocal (vector3 (* (/ (- _A) 2) _s_z) 0                     (/  1 _C)             ))))
(define W+z+y (cons "W+z+y" (cartesian->reciprocal (vector3 0                     (* (/    _B  2) _s_z) (/  1 _C)             ))))
(define W+z-y (cons "W+z-y" (cartesian->reciprocal (vector3 0                     (* (/ (- _B) 2) _s_z) (/  1 _C)             ))))

(define W-z+x (cons "W-z+x" (cartesian->reciprocal (vector3 (* (/    _A  2) _s_z) 0                     (/ -1 _C)             ))))
(define W-z-x (cons "W-z-x" (cartesian->reciprocal (vector3 (* (/ (- _A) 2) _s_z) 0                     (/ -1 _C)             ))))
(define W-z+y (cons "W-z+y" (cartesian->reciprocal (vector3 0                     (* (/    _B  2) _s_z) (/ -1 _C)             ))))
(define W-z-y (cons "W-z-y" (cartesian->reciprocal (vector3 0                     (* (/ (- _B) 2) _s_z) (/ -1 _C)             ))))

; U points: U_ijk = (W_ij + W_ik)/2
(define U+x+y+z (cons "U+x+y+z" (vector3* 0.5 (vector3+ (cdr W+x+y) (cdr W+x+z))) ))
(define U+x+y-z (cons "U+x+y-z" (vector3* 0.5 (vector3+ (cdr W+x+y) (cdr W+x-z))) ))
(define U+x-y+z (cons "U+x-y+z" (vector3* 0.5 (vector3+ (cdr W+x-y) (cdr W+x+z))) ))
(define U+x-y-z (cons "U+x-y-z" (vector3* 0.5 (vector3+ (cdr W+x-y) (cdr W+x-z))) ))
(define U-x+y+z (cons "U-x+y+z" (vector3* 0.5 (vector3+ (cdr W-x+y) (cdr W-x+z))) ))
(define U-x+y-z (cons "U-x+y-z" (vector3* 0.5 (vector3+ (cdr W-x+y) (cdr W-x-z))) ))
(define U-x-y+z (cons "U-x-y+z" (vector3* 0.5 (vector3+ (cdr W-x-y) (cdr W-x+z))) ))
(define U-x-y-z (cons "U-x-y-z" (vector3* 0.5 (vector3+ (cdr W-x-y) (cdr W-x-z))) ))

(define U+y+x+z (cons "U+y+x+z" (vector3* 0.5 (vector3+ (cdr W+y+x) (cdr W+y+z))) ))
(define U+y+x-z (cons "U+y+x-z" (vector3* 0.5 (vector3+ (cdr W+y+x) (cdr W+y-z))) ))
(define U+y-x+z (cons "U+y-x+z" (vector3* 0.5 (vector3+ (cdr W+y-x) (cdr W+y+z))) ))
(define U+y-x-z (cons "U+y-x-z" (vector3* 0.5 (vector3+ (cdr W+y-x) (cdr W+y-z))) ))
(define U-y+x+z (cons "U-y+x+z" (vector3* 0.5 (vector3+ (cdr W-y+x) (cdr W-y+z))) ))
(define U-y+x-z (cons "U-y+x-z" (vector3* 0.5 (vector3+ (cdr W-y+x) (cdr W-y-z))) ))
(define U-y-x+z (cons "U-y-x+z" (vector3* 0.5 (vector3+ (cdr W-y-x) (cdr W-y+z))) ))
(define U-y-x-z (cons "U-y-x-z" (vector3* 0.5 (vector3+ (cdr W-y-x) (cdr W-y-z))) ))

(define U+z+x+y (cons "U+z+x+y" (vector3* 0.5 (vector3+ (cdr W+z+x) (cdr W+z+y))) ))
(define U+z+x-y (cons "U+z+x-y" (vector3* 0.5 (vector3+ (cdr W+z+x) (cdr W+z-y))) ))
(define U+z-x+y (cons "U+z-x+y" (vector3* 0.5 (vector3+ (cdr W+z-x) (cdr W+z+y))) ))
(define U+z-x-y (cons "U+z-x-y" (vector3* 0.5 (vector3+ (cdr W+z-x) (cdr W+z-y))) ))
(define U-z+x+y (cons "U-z+x+y" (vector3* 0.5 (vector3+ (cdr W-z+x) (cdr W-z+y))) ))
(define U-z+x-y (cons "U-z+x-y" (vector3* 0.5 (vector3+ (cdr W-z+x) (cdr W-z-y))) ))
(define U-z-x+y (cons "U-z-x+y" (vector3* 0.5 (vector3+ (cdr W-z-x) (cdr W-z+y))) ))
(define U-z-x-y (cons "U-z-x-y" (vector3* 0.5 (vector3+ (cdr W-z-x) (cdr W-z-y))) ))

; K points: K_ij = (W_ij + W_ji)/2
(define K+x+y (cons "K+x+y" (vector3* 0.5 (vector3+ (cdr W+x+y) (cdr W+y+x))) ))
(define K+x-y (cons "K+x-y" (vector3* 0.5 (vector3+ (cdr W+x-y) (cdr W-y+x))) ))
(define K-x+y (cons "K-x+y" (vector3* 0.5 (vector3+ (cdr W-x+y) (cdr W+y-x))) ))
(define K-x-y (cons "K-x-y" (vector3* 0.5 (vector3+ (cdr W-x-y) (cdr W-y-x))) ))

(define K+y+z (cons "K+y+z" (vector3* 0.5 (vector3+ (cdr W+y+z) (cdr W+z+y))) ))
(define K+y-z (cons "K+y-z" (vector3* 0.5 (vector3+ (cdr W+y-z) (cdr W-z+y))) ))
(define K-y+z (cons "K-y+z" (vector3* 0.5 (vector3+ (cdr W-y+z) (cdr W+z-y))) ))
(define K-y-z (cons "K-y-z" (vector3* 0.5 (vector3+ (cdr W-y-z) (cdr W-z-y))) ))

(define K+x+z (cons "K+x+z" (vector3* 0.5 (vector3+ (cdr W+x+z) (cdr W+z+x))) ))
(define K+x-z (cons "K+x-z" (vector3* 0.5 (vector3+ (cdr W+x-z) (cdr W-z+x))) ))
(define K-x+z (cons "K-x+z" (vector3* 0.5 (vector3+ (cdr W-x+z) (cdr W+z-x))) ))
(define K-x-z (cons "K-x-z" (vector3* 0.5 (vector3+ (cdr W-x-z) (cdr W-z-x))) ))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; load point lists
(load-from-path "FCT_BZ_label_lists.ctl")
