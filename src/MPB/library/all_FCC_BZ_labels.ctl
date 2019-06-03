; TODO: Use in combination with (load-from-path "loadme.ctl"), export GUILE_LOAD_PATH=./subdir/, include-dir, modules, etc
; example:
;; export GUILE_LOAD_PATH=$HOME/Development/script_inception_public/reference/examples_MPB/woodpile_extendedDiagrams
;; (load-from-path "all_FCC_BZ_labels.ctl")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; FCC lattice basis definition. The "MPB unit size" is the side of the cubic unit cell.
; NOTE: basis1, basis2 and basis3 are normalized to be as long as specified in "basis-size"
(set! geometry-lattice (make lattice
                         (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
                         (basis1 0 1 1)
                         (basis2 1 0 1)
                         (basis3 1 1 0)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Corners of the irreducible Brillouin zone for the FCC lattice.
; NOTE: k-points are specified in the reciprocal lattice!!! (the reciprocal of the specified geometry-lattice)
; We use cartesian->reciprocal here because it's easier to visualize the k-points in the normal cartesian basis.

; Gamma point
(define Gamma (cons "Gamma" (cartesian->reciprocal (vector3 0 0 0))))

; X points: X_i = i
(define X+x (cons "X+x" (cartesian->reciprocal (vector3  1  0  0))))
(define X-x (cons "X-x" (cartesian->reciprocal (vector3 -1  0  0))))
(define X+y (cons "X+y" (cartesian->reciprocal (vector3  0  1  0))))
(define X-y (cons "X-y" (cartesian->reciprocal (vector3  0 -1  0))))
(define X+z (cons "X+z" (cartesian->reciprocal (vector3  0  0  1))))
(define X-z (cons "X-z" (cartesian->reciprocal (vector3  0  0 -1))))

; U points: U_ijk = i + 1/4*j + 1/4*k
(define U+x+y+z (cons "U+x+y+z" (cartesian->reciprocal (vector3  1  0.25  0.25))))
(define U+x+y-z (cons "U+x+y-z" (cartesian->reciprocal (vector3  1  0.25 -0.25))))
(define U+x-y+z (cons "U+x-y+z" (cartesian->reciprocal (vector3  1 -0.25  0.25))))
(define U+x-y-z (cons "U+x-y-z" (cartesian->reciprocal (vector3  1 -0.25 -0.25))))
(define U-x+y+z (cons "U-x+y+z" (cartesian->reciprocal (vector3 -1  0.25  0.25))))
(define U-x+y-z (cons "U-x+y-z" (cartesian->reciprocal (vector3 -1  0.25 -0.25))))
(define U-x-y+z (cons "U-x-y+z" (cartesian->reciprocal (vector3 -1 -0.25  0.25))))
(define U-x-y-z (cons "U-x-y-z" (cartesian->reciprocal (vector3 -1 -0.25 -0.25))))

(define U+y+x+z (cons "U+y+x+z" (cartesian->reciprocal (vector3  0.25  1  0.25))))
(define U+y+x-z (cons "U+y+x-z" (cartesian->reciprocal (vector3  0.25  1 -0.25))))
(define U+y-x+z (cons "U+y-x+z" (cartesian->reciprocal (vector3 -0.25  1  0.25))))
(define U+y-x-z (cons "U+y-x-z" (cartesian->reciprocal (vector3 -0.25  1 -0.25))))
(define U-y+x+z (cons "U-y+x+z" (cartesian->reciprocal (vector3  0.25 -1  0.25))))
(define U-y+x-z (cons "U-y+x-z" (cartesian->reciprocal (vector3  0.25 -1 -0.25))))
(define U-y-x+z (cons "U-y-x+z" (cartesian->reciprocal (vector3 -0.25 -1  0.25))))
(define U-y-x-z (cons "U-y-x-z" (cartesian->reciprocal (vector3 -0.25 -1 -0.25))))

(define U+z+x+y (cons "U+z+x+y" (cartesian->reciprocal (vector3  0.25  0.25  1))))
(define U+z+x-y (cons "U+z+x-y" (cartesian->reciprocal (vector3  0.25 -0.25  1))))
(define U+z-x+y (cons "U+z-x+y" (cartesian->reciprocal (vector3 -0.25  0.25  1))))
(define U+z-x-y (cons "U+z-x-y" (cartesian->reciprocal (vector3 -0.25 -0.25  1))))
(define U-z+x+y (cons "U-z+x+y" (cartesian->reciprocal (vector3  0.25  0.25 -1))))
(define U-z+x-y (cons "U-z+x-y" (cartesian->reciprocal (vector3  0.25 -0.25 -1))))
(define U-z-x+y (cons "U-z-x+y" (cartesian->reciprocal (vector3 -0.25  0.25 -1))))
(define U-z-x-y (cons "U-z-x-y" (cartesian->reciprocal (vector3 -0.25 -0.25 -1))))

; L points: L_ijk = 1/2*(i+j+k)
(define L+x+y+z (cons "L+x+y+z" (cartesian->reciprocal (vector3  0.5  0.5  0.5))))
(define L+x+y-z (cons "L+x+y-z" (cartesian->reciprocal (vector3  0.5  0.5 -0.5))))
(define L+x-y+z (cons "L+x-y+z" (cartesian->reciprocal (vector3  0.5 -0.5  0.5))))
(define L+x-y-z (cons "L+x-y-z" (cartesian->reciprocal (vector3  0.5 -0.5 -0.5))))
(define L-x+y+z (cons "L-x+y+z" (cartesian->reciprocal (vector3 -0.5  0.5  0.5))))
(define L-x+y-z (cons "L-x+y-z" (cartesian->reciprocal (vector3 -0.5  0.5 -0.5))))
(define L-x-y+z (cons "L-x-y+z" (cartesian->reciprocal (vector3 -0.5 -0.5  0.5))))
(define L-x-y-z (cons "L-x-y-z" (cartesian->reciprocal (vector3 -0.5 -0.5 -0.5))))

; W points: W_ij = i + 1/2*j
(define W+x+y (cons "W+x+y" (cartesian->reciprocal (vector3  1  0.5  0))))
(define W+x-y (cons "W+x-y" (cartesian->reciprocal (vector3  1 -0.5  0))))
(define W+x+z (cons "W+x+z" (cartesian->reciprocal (vector3  1  0  0.5))))
(define W+x-z (cons "W+x-z" (cartesian->reciprocal (vector3  1  0 -0.5))))
(define W-x+y (cons "W-x+y" (cartesian->reciprocal (vector3 -1  0.5  0))))
(define W-x-y (cons "W-x-y" (cartesian->reciprocal (vector3 -1 -0.5  0))))
(define W-x+z (cons "W-x+z" (cartesian->reciprocal (vector3 -1  0  0.5))))
(define W-x-z (cons "W-x-z" (cartesian->reciprocal (vector3 -1  0 -0.5))))

(define W+y+x (cons "W+y+x" (cartesian->reciprocal (vector3  0.5  1  0  ))))
(define W+y-x (cons "W+y-x" (cartesian->reciprocal (vector3 -0.5  1  0  ))))
(define W+y+z (cons "W+y+z" (cartesian->reciprocal (vector3  0    1  0.5))))
(define W+y-z (cons "W+y-z" (cartesian->reciprocal (vector3  0    1 -0.5))))
(define W-y+x (cons "W-y+x" (cartesian->reciprocal (vector3  0.5 -1  0  ))))
(define W-y-x (cons "W-y-x" (cartesian->reciprocal (vector3 -0.5 -1  0  ))))
(define W-y+z (cons "W-y+z" (cartesian->reciprocal (vector3  0   -1  0.5))))
(define W-y-z (cons "W-y-z" (cartesian->reciprocal (vector3  0   -1 -0.5))))

(define W+z+x (cons "W+z+x" (cartesian->reciprocal (vector3  0.5  0    1))))
(define W+z-x (cons "W+z-x" (cartesian->reciprocal (vector3 -0.5  0    1))))
(define W+z+y (cons "W+z+y" (cartesian->reciprocal (vector3  0    0.5  1))))
(define W+z-y (cons "W+z-y" (cartesian->reciprocal (vector3  0   -0.5  1))))
(define W-z+x (cons "W-z+x" (cartesian->reciprocal (vector3  0.5  0   -1))))
(define W-z-x (cons "W-z-x" (cartesian->reciprocal (vector3 -0.5  0   -1))))
(define W-z+y (cons "W-z+y" (cartesian->reciprocal (vector3  0    0.5 -1))))
(define W-z-y (cons "W-z-y" (cartesian->reciprocal (vector3  0   -0.5 -1))))

; K points: K_ij = 3/4*(i+j)
(define K+x+y (cons "K+x+y" (cartesian->reciprocal (vector3  0.75  0.75  0))))
(define K+x-y (cons "K+x-y" (cartesian->reciprocal (vector3  0.75 -0.75  0))))
(define K-x+y (cons "K-x+y" (cartesian->reciprocal (vector3 -0.75  0.75  0))))
(define K-x-y (cons "K-x-y" (cartesian->reciprocal (vector3 -0.75 -0.75  0))))

(define K+y+z (cons "K+y+z" (cartesian->reciprocal (vector3  0  0.75  0.75))))
(define K+y-z (cons "K+y-z" (cartesian->reciprocal (vector3  0  0.75 -0.75))))
(define K-y+z (cons "K-y+z" (cartesian->reciprocal (vector3  0 -0.75  0.75))))
(define K-y-z (cons "K-y-z" (cartesian->reciprocal (vector3  0 -0.75 -0.75))))

(define K+x+z (cons "K+x+z" (cartesian->reciprocal (vector3  0.75  0  0.75))))
(define K+x-z (cons "K+x-z" (cartesian->reciprocal (vector3  0.75  0 -0.75))))
(define K-x+z (cons "K-x+z" (cartesian->reciprocal (vector3 -0.75  0  0.75))))
(define K-x-z (cons "K-x-z" (cartesian->reciprocal (vector3 -0.75  0 -0.75))))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; load point lists
(load-from-path "FCT_BZ_label_lists.ctl")
