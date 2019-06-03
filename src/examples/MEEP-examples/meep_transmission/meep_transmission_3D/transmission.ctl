;===============================
;;; parameters

(define-param is-reference? true) ; if true, have waveguide, else vaccuum

(define-param sx 5) ; size of cell in X direction
(define-param sy 5) ; size of cell in Y direction
(define-param sz 5) ; size of cell in Z direction

(set-param! resolution 20)

; block size
(define-param wx 1.125)
(define-param wy sy)
(define-param wz sz)

(define-param pml-thickness 1)

(define-param n_block 2)

(define fabry-perot-period (/ 1 (* 2 n_block wx)) ) ; theoretical Fabry-Perot period of the transmission and reflection curves at normal incidence

(define-param fcen fabry-perot-period) ; pulse center frequency
(define-param df fabry-perot-period)    ; pulse width (in frequency)
(define-param nfreq 500) ; number of frequencies at which to compute flux

;===============================
;;; local variables

; defining various positions
(define pml-edge-low (+ (- (/ sx 2)) pml-thickness) )
(define pml-edge-high (- (/ sx 2) pml-thickness ) )
(define flux_trans_pos_x (/ (+ (/ wx 2) pml-edge-high ) 2) )
(define flux_ref_pos_x (- flux_trans_pos_x) )
(define source_pos_x (/ (+ pml-edge-low flux_ref_pos_x) 2) )

; condition 1: Ncells<=100^3
(define Ncells (* sx sy sz resolution resolution resolution) )
(define condition1 (<= Ncells (expt 100 3)) )

; condition 2: ( 1/resolution = delta ) <= ( delta_max = lambda_min/(15*n) )
(define fmax (+ fcen (/ df 2)) )
(define fmin (- fcen (/ df 2)) )
(define lambda_min (/ 1 fmax) )
(define lambda_max (/ 1 fmin) )
(define lambda_cen (/ 1 fcen) )
(define delta_max (/ lambda_min (* 15 n_block)) )
(define delta (/ 1 resolution) )
(define condition2 (<= delta delta_max) )

; correct order of positions
(define condition3
  (<
    (/ (- sx) 2)
    pml-edge-low
    source_pos_x
    flux_ref_pos_x
    (/ (- wx) 2)
    0
    (/ wx 2)
    flux_trans_pos_x
    pml-edge-high
    (/ sx 2)
  )
)

;===============================
;;; print info
(print "is-reference? = " is-reference? "\n")

(print "sx = " sx "\n")
(print "sy = " sy "\n")
(print "sz = " sz "\n")
(print "resolution = " resolution "\n")

(print "wx = " wx "\n")
(print "wy = " wy "\n")
(print "wz = " wz "\n")
(print "n_block = " n_block "\n")

(print "Ncells = " Ncells "\n")
(print "Ncells <= 100^3 = " condition1 "\n")

(print "wx/2 = " (/ wx 2) "\n")
(print "pml-thickness = " pml-thickness "\n")
(print "pml-edge-low = " pml-edge-low "\n")
(print "pml-edge-high = " pml-edge-high "\n")

(print "source_pos_x = " source_pos_x "\n")
(print "flux_ref_pos_x = " flux_ref_pos_x  "\n")
(print "flux_trans_pos_x = " flux_trans_pos_x  "\n")

(print "fmin = " fmin "\n")
(print "fcen = " fcen "\n")
(print "fmax = " fmax "\n")
(print "df = " df "\n")
(print "fabry-perot-period = " fabry-perot-period "\n")
(print "nfreq = " nfreq "\n")

(print "lambda_min = " lambda_min "\n")
(print "lambda_cen = " lambda_cen "\n")
(print "lambda_max = " lambda_max "\n")

(print "delta_max = " delta_max "\n")
(print "delta = " delta "\n")
(print "delta <= delta_max = " condition2 "\n")

(print "condition1 = " condition1 "\n")
(print "condition2 = " condition2 "\n")
(print "condition3 = " condition3 "\n")

(if (and condition1 condition2 condition3)
  (print "All ok.\n")
  (begin
    (print "Check your parameters.\n")
    (exit -1)
  )
)

;; (exit)

;===============================
;;; set up sim based on given parameters

(set! geometry-lattice (make lattice (size sx sy sz)))
(set! pml-layers (list (make pml (thickness pml-thickness))))

(if (not is-reference?)
  (set! geometry
    (list
      (make block
        (center 0 0 0)
        (size wx wy wz)
        (material (make dielectric (index n_block)))
      )
    )
  )
)

(set! sources (list
  (make source
    (src (make gaussian-src (frequency fcen) (fwidth df)))
    (component Ez)
    (center source_pos_x 0 0)
    (size 0 sy sz)
  )
))

(define trans ; transmitted flux
  (add-flux fcen df nfreq
    (make flux-region
      (center flux_trans_pos_x 0 0)
      (size 0 sy sz)
    )
  )
)

(define refl ; reflected flux
  (add-flux fcen df nfreq
    (make flux-region
      (center flux_ref_pos_x 0 0)
      (size 0 sy sz)
    )
  )
)

(if (not is-reference?) (load-minus-flux "refl-flux" refl))

;; (stop-when-fields-decayed dT c pt decay-by)
;; Return a cond? function, suitable for passing to run-until/run-sources+, that examines the component c (e.g. Ex, etc.) at the point pt (a vector3) and keeps running until its absolute value squared has decayed by at least decay-by from its maximum previous value. In particular, it keeps incrementing the run time by dT (in Meep units) and checks the maximum value over that time period—in this way, it won't be fooled just because the field happens to go through 0 at some instant.
;; Note that, if you make decay-by very small, you may need to increase the cutoff property of your source(s), to decrease the amplitude of the small high-frequency components that are excited when the source turns off. (High frequencies near the Nyquist frequency of the grid have slow group velocities and are absorbed poorly by PML.)

; running time ~ 35m26.823s

(run-sources+
  (stop-when-fields-decayed
    50
    Ez
    (vector3 flux_trans_pos_x 0 0)
    1e-3
  )
  (at-beginning output-epsilon)
)

(if is-reference? (save-flux "refl-flux" refl))

(display-fluxes trans refl)
