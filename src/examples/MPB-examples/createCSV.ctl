;--------------------------------------------------------------
; script to create a .csv file to plot the bandgap from band 2 to 3 as a function of w/c
;--------------------------------------------------------------

;--------------------------------------------------------------
; these parameters can be specified by command-line with "name=value"
(define-param n_log 3.3) ; the refractive index of the "log" material
(define-param n_outer 1) ; the refractive index of the "outer" surrounding material
(define-param wmin 0.1)
(define-param wmax 0.7)
(define-param wstep 0.01)
(define-param csvfile "test.csv")
(define-param k-interp 9)
(define-param h 0.25 ) ; height of logs (should be 1/4 for fcc to not overlap)
; Variables defined by MPB. They can only be set, not defined.
(set-param! resolution 32)
(set-param! num-bands 24)
;--------------------------------------------------------------

(set! geometry-lattice (make lattice
                         (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
                         (basis1 0 1 1)
                         (basis2 1 0 1)
                         (basis3 1 1 0)))

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
;(set! k-points (interpolate k-interp (list X U L Gamma X' W' K')))

(define diel_log (make dielectric (index n_log)))
(define diel_outer (make dielectric (index n_outer)))

(set! default-material diel_outer);

; shortcut for cartesian->lattice function:
(define (c->l . args) (cartesian->lattice (apply vector3 args)))

; function which returns the gap between bands 2 and 3
(define gap -1)
(define (second-gap warg)  ; warg = width of the rods

;;   (print "============================\n")
;;   (print "width factor w = " warg "\n")

  (set! geometry
          (list
          (make block (material diel_log)
                (center (c->l 0 0 0))
                (e1 (c->l 1 1 0))
                (e2 (c->l 1 -1 0))
                (e3 (c->l 0 0 1))
                (size infinity warg h))
          (make block (material diel_log)
                (center (c->l 0.125 0.125 h))
                (e1 (c->l 1 1 0))
                (e2 (c->l 1 -1 0))
                (e3 (c->l 0 0 1))
                (size warg infinity h))))

;;   (run)
;; 
;;   (set! gap (retrieve-gap 2))
;;   (print "width factor w = " warg " gap = " gap "\n")
;;   (print "============================\n")

  gap
) ; return the gap from band 2 to band 3

; write function results to a CSV file
(define (createCSV dx xmin xmax filename)
  (define result 0)

  (define outfile (open-output-file filename))
  (display "w; gap2-3\n" outfile)

  (do ((x xmin (+ x dx))) ((> x xmax))
    (set! result (second-gap x))
    (print "f(" x ") = " result "\n")
    (display x outfile)
    (display "; " outfile)
    (display result outfile)
    (display "\n" outfile)
  )

  (close-output-port outfile)
)

; for quick testing (~10s per run)
;; (set! k-points (list X U L Gamma))
;; (set-param! num-bands 3)

;; (second-gap 0.2)

(createCSV wstep wmin wmax csvfile)

(exit)
