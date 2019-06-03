; A list of the labels for future use.
; TODO: pair each point with a label for easier printing of label lists (will require some getter functions)

(define reciprocal_lattice_vectors (list
  (vector3 1 0 0)
  (vector3 0 1 0)
  (vector3 0 0 1)
))

(define X_kpoints (list
  X+x
  X-x
  X+y
  X-y
  X+z
  X-z
))

(define U_kpoints (list
  U+x+y+z
  U+x+y-z
  U+x-y+z
  U+x-y-z
  U-x+y+z
  U-x+y-z
  U-x-y+z
  U-x-y-z
  U+y+x+z
  U+y+x-z
  U+y-x+z
  U+y-x-z
  U-y+x+z
  U-y+x-z
  U-y-x+z
  U-y-x-z
  U+z+x+y
  U+z+x-y
  U+z-x+y
  U+z-x-y
  U-z+x+y
  U-z+x-y
  U-z-x+y
  U-z-x-y
))

(define L_kpoints (list
  L+x+y+z
  L+x+y-z
  L+x-y+z
  L+x-y-z
  L-x+y+z
  L-x+y-z
  L-x-y+z
  L-x-y-z
))

(define W_kpoints (list
  W+x+y
  W+x-y
  W+x+z
  W+x-z
  W-x+y
  W-x-y
  W-x+z
  W-x-z
  W+y+x
  W+y-x
  W+y+z
  W+y-z
  W-y+x
  W-y-x
  W-y+z
  W-y-z
  W+z+x
  W+z-x
  W+z+y
  W+z-y
  W-z+x
  W-z-x
  W-z+y
  W-z-y
))

(define K_kpoints (list
  K+x+y
  K+x-y
  K-x+y
  K-x-y
  K+y+z
  K+y-z
  K-y+z
  K-y-z
  K+x+z
  K+x-z
  K-x+z
  K-x-z
))

(define kpoints_all (append
  (list Gamma)
  X_kpoints
  U_kpoints
  L_kpoints
  W_kpoints
  K_kpoints
))

(define RotAround_-x+y (list Gamma
K-x-y
L-x-y+z
U+z-x-y
X+z
U+z+x+y
L+x+y+z
K+x+y
L+x+y-z
U-z+x+y
X-z
))

(define RotAround_y (list Gamma
X-x
W-x+z
K-x+z
W+z-x
X+z
W+z+x
K+x+z
W+x+z
X+x
))

(define RotAround_z (list Gamma
K+x-y
W+x-y
X+x
W+x+y
K+x+y
W+y+x
X+y
W+y-x
K-x+y
))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define RotAround_-x+y_quarter (list Gamma
X+z
U+z+x+y
L+x+y+z
K+x+y
))

(define RotAround_y_quarter (list Gamma
X+z
W+z+x
K+x+z
W+x+z
X+x
))

(define RotAround_z_quarter (list Gamma
X+x
W+x+y
K+x+y
W+y+x
X+y
))

(define RotAround_-y+z_quarter (list Gamma
X+x
U+x+y+z
L+x+y+z
K+y+z
))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define FCC_standard_kpoints (append
RotAround_-x+y_quarter
RotAround_y_quarter
RotAround_z_quarter
RotAround_-y+z_quarter
))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define RCD_kpoints (list Gamma
W+x+z
X+x
U+x+y+z
L+x+y+z
K+y+z
))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; load coordinate conversion functions and other utilities
(load-from-path "utilities.ctl")

; Loop through the k-points and do stuff.
; We do multiple single runs, because otherwise it crashes. MPB apparently does not like a too discontinuous k-point list.
;; (map (lambda (x)
;;   (print x "\n")
;;   (set! k-points (list x))
;;   (run)
;; 
;; ) label_list )
;; ) RotAround_-x+y )
;; ) RotAround_y )
;; ) RotAround_z )

;; (print "number of labels: " (length label_list) "\n")

;; (exit)
