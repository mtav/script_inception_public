;===============================
;;; parameters

(define-param dim 1)

(define-param is-reference? true) ; if true, have waveguide, else vaccuum

;; TODO: periodic boundaries
;; TODO: plane wave source
;; TODO: plane wave source with specific incidence angle
;; TODO: fix Ncells calc in case non-3D sim
;; TODO: Implement 1/2/3D case logic

(define-param sx 7) ; size of cell in X direction
(define-param sy 3) ; size of cell in Y direction
(define-param sz 3) ; size of cell in Z direction

(case dim
  ((1)(begin
    (print "=== 1D ===\n")
    (set! sy no-size) ; size of cell in Y direction
    (set! sz no-size) ; size of cell in Z direction
  ))
  ((2)(begin
    (print "=== 2D ===\n")
    (set! sz no-size) ; size of cell in Z direction
  ))
  ((3)(begin
    (print "=== 3D ===\n")
  ))
  (else
    (print "ERROR: INVALID DIMENSIONALITY\n")
    (exit -1)
  )
)

(set-param! resolution 50)
;; (set-param! resolution 28)

; block size
(define-param wx 1.125)
(define-param wy infinity)
(define-param wz infinity)

; flux plane size
(define-param flux_wx 0)
(define-param flux_wy 1)
(define-param flux_wz 1)

(define-param pml_thickness 1)

(define-param n_block 2)

(define fabry_perot_period (/ 1 (* 2 n_block wx)) ) ; theoretical Fabry-Perot period of the transmission and reflection curves at normal incidence

(define-param fcen (* 6 fabry_perot_period)) ; pulse center frequency
(define-param df (* 3 fabry_perot_period))    ; pulse width (in frequency)
(define-param nfreq 500) ; number of frequencies at which to compute flux

(define-param sim_time_factor 5)

;===============================
;;; local variables

(define src_time (* 2 5 (/ 1 df)) )
(define sim_time (* sim_time_factor src_time))

; defining various positions
(define pml-edge-low (+ (- (/ sx 2)) pml_thickness) )
(define pml-edge-high (- (/ sx 2) pml_thickness ) )
(define flux_trans_pos_x (/ (+ (/ wx 2) pml-edge-high ) 2) )
(define flux_ref_pos_x (- flux_trans_pos_x) )
(define source_pos_x (/ (+ pml-edge-low flux_ref_pos_x) 2) )

; condition 1: Ncells<=100^3
(define Ncells_X (ceiling (* sx resolution)))
(define Ncells_Y (ceiling (* sy resolution)))
(define Ncells_Z (ceiling (* sz resolution)))
(define Ncells (* Ncells_X Ncells_Y Ncells_Z) )
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

; PML thickness should be at least 1 time the longest wavelength (5 times even better)
(define condition4
  (>= pml_thickness lambda_max)
)

; enough cells inside slab
(define Ncells_slab (/ wx delta))
(define condition5
  (>= Ncells_slab 5)
)

;===============================
;;; print info
(print "is-reference? = " is-reference? "\n")

(print "sx = " sx "\n")
(print "sy = " sy "\n")
(print "sz = " sz "\n")
(print "resolution = " resolution "\n")

(print "src_time = " src_time "\n")
(print "sim_time_factor = " sim_time_factor "\n")
(print "sim_time = " sim_time "\n")

(print "wx = " wx "\n")
(print "wy = " wy "\n")
(print "wz = " wz "\n")
(print "n_block = " n_block "\n")

(print "Ncells_X = " Ncells_X "\n")
(print "Ncells_Y = " Ncells_Y "\n")
(print "Ncells_Z = " Ncells_Z "\n")
(print "Ncells = " Ncells "\n")
(print "Ncells <= 100^3 = " condition1 "\n")

(print "wx/2 = " (/ wx 2) "\n")
(print "pml_thickness = " pml_thickness "\n")
(print "pml-edge-low = " pml-edge-low "\n")
(print "pml-edge-high = " pml-edge-high "\n")

(print "source_pos_x = " source_pos_x "\n")
(print "flux_ref_pos_x = " flux_ref_pos_x  "\n")
(print "flux_trans_pos_x = " flux_trans_pos_x  "\n")

(print "fmin = " fmin "\n")
(print "fcen = " fcen "\n")
(print "fmax = " fmax "\n")
(print "df = " df "\n")
(print "fabry_perot_period = " fabry_perot_period "\n")
(print "nfreq = " nfreq "\n")

(print "lambda_min = " lambda_min "\n")
(print "lambda_cen = " lambda_cen "\n")
(print "lambda_max = " lambda_max "\n")

(print "delta_max = " delta_max "\n")
(print "delta = " (format #f "~,3f" delta ) "\n")
(print "delta <= delta_max = " condition2 "\n")

(print "Ncells_slab = " Ncells_slab "\n")

(print "condition1 = " condition1 "\n")
(print "condition2 = " condition2 "\n")
(print "condition3 = " condition3 "\n")
(print "condition4 = " condition4 "\n")
(print "condition5 = " condition5 "\n")

(if (and condition1 condition2 condition3 condition4 condition5)
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

(set! pml-layers (list
  (make pml
;;   (make absorber
    (thickness pml_thickness)
    (direction X)
  )
))

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

;; point gaussian source
;; (set! sources (list
;;   (make source
;;     (src (make gaussian-src (frequency fcen) (fwidth df)))
;;     (component Ez)
;;     (center source_pos_x 0 0)
;;     (size 0 0 0)
;;   )
;; ))

;; plane-wave + periodic boundary conditions
;; IMPORTANT: src must be on PML edge!!!
(set! k-point (vector3 0 0 0))

(set! sources (list
  (make source
;;     (src (make continuous-src (frequency fcen)))
    (src (make gaussian-src (frequency fcen) (fwidth df)))
    (component Ez)
    (center (+ (/ sx -2) pml_thickness) 0)
    (size 0 sy)
  )
))

;; WARNING: using no-size for any flux plane dimension leads to null output! infinity can also not be used!
(define trans ; transmitted flux
  (add-flux fcen df nfreq
    (make flux-region
      (center flux_trans_pos_x 0 0)
      (size flux_wx flux_wy flux_wz)
      (direction X)
    )
  )
)

(define refl ; reflected flux
  (add-flux fcen df nfreq
    (make flux-region
      (center flux_ref_pos_x 0 0)
      (size flux_wx flux_wy flux_wz)
      (direction X)
    )
  )
)

;; (if (not is-reference?) (load-minus-flux "refl-flux" refl))

;; (stop-when-fields-decayed dT c pt decay-by)
;; Return a cond? function, suitable for passing to run-until/run-sources+, that examines the component c (e.g. Ex, etc.) at the point pt (a vector3) and keeps running until its absolute value squared has decayed by at least decay-by from its maximum previous value. In particular, it keeps incrementing the run time by dT (in Meep units) and checks the maximum value over that time period—in this way, it won't be fooled just because the field happens to go through 0 at some instant.
;; Note that, if you make decay-by very small, you may need to increase the cutoff property of your source(s), to decrease the amplitude of the small high-frequency components that are excited when the source turns off. (High frequencies near the Nyquist frequency of the grid have slow group velocities and are absorbed poorly by PML.)

(set-param! filename-prefix
  (string-append
    "transmission"
    "_is-reference-" (if is-reference? "true" "false")
  )
)

; running time ~ 35m26.823s

;; (run-sources+
;;   (stop-when-fields-decayed
;;     50
;;     Ez
;;     (vector3 flux_trans_pos_x 0 0)
;;     1e-3
;;   )
;;   (at-beginning output-epsilon)
;;   (to-appended "ez" output-efield-z)
;; )

; method 2: run for a specific time
(run-until sim_time
  (at-beginning output-epsilon)
;;   output-efield-z ; so we can check if it has decayed enough
;;   (to-appended "ez" output-efield-z)
  (to-appended "ez" (at-every (/ 1 fcen 4) output-efield-z))
  (at-end (output-png Ex "-Zc dkbluered"))
  (at-end (output-png Ey "-Zc dkbluered"))
  (at-end (output-png Ez "-Zc dkbluered"))
  (at-end (output-png Hx "-Zc dkbluered"))
  (at-end (output-png Hy "-Zc dkbluered"))
  (at-end (output-png Hz "-Zc dkbluered"))
)

;; (if is-reference? (save-flux "refl-flux" refl))

(display-fluxes trans refl)
