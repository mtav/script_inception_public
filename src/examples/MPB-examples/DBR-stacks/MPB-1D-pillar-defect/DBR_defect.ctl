; TODO:
; -resonance freq vs index, defect size plots
; -reproduce SJ defect plots
; -finish MPB defect tutorials
; -make sure edge of BZ is reached and supercell size is a nice multiple of basis-size (i.e. set t1,t2 and cavity_length accordingly)
; -try to plot field of the 3 bands we find inside bandgap to compare them

;;;;; simulation mode:
(define-param defect-mode? false) ; if true, compute frequency of expected resonance only, at k=(0.5,0,0) only + output fields, else create usual band diagram

;;;;; DBR index values
(define-param n1 1)
(define-param n2 3.5)
;; (define-param n1 3.5)
;; (define-param n2 1)

;;;;; midgap "a/lambda"
(define a_over_lambda_midgap (/ (+ n1 n2) (* 4 n1 n2) ) )

;;;;; a = 1, "normalized lambda0"
(define a 1)
(define lambda0 (/ a a_over_lambda_midgap) )

;;;;; lambda0 = 1, "normalized a" (a = primitive unit-cell size = DBR_pair_thickness)
;; (define lambda0 1)
;; (define a (* lambda0 a_over_lambda_midgap) )

(define-param cavity_index n2)
(define-param cavity_length (/ lambda0 (* 1 n2)))

(define-param N_mirror_pairs 10)

; layer thicknesses
(define-param t1 (/ lambda0 (* 4 n1)) )
(define-param t2 (/ lambda0 (* 4 n2)) )
(define DBR_pair_thickness (+ t1 t2))

(define lattice_basis_size 1) ; TODO: Make sure defines are robust against param change. If supposed to be "a", this should actually also intervene in t1, t2, etc definitions...
(define lattice_size (+ cavity_length (* 2 N_mirror_pairs DBR_pair_thickness) ))

(define pi (acos -1))

(define midgap (/ (/ (+ n1 n2) (* 4 n1 n2)) DBR_pair_thickness) )
(define gapsize (* (/ 4 pi) (asin (/ (abs (- n1 n2)) (+ n1 n2)) ) ))

(define topgap (* midgap (+ 1 (/ gapsize 2))) )
(define botgap (* midgap (- 1 (/ gapsize 2))) )

; extreme values of n, which should lead the resonance frequency to the band edges:
; L=lam/n => n = lam/L = c/(f*L) = 1/(fn*L) = (1/L)/fn
(define nmin (/ (/ 1 cavity_length) topgap) )
(define nmax (/ (/ 1 cavity_length) botgap) )

; expected resonance frequency:
; L = lam/n = (c/f)/n = 1/(fn*n) => fn = 1/(n*L)
(define f0n (/ 1 (* cavity_index cavity_length)))

(print "n1 = " n1 "\n")
(print "n2 = " n2 "\n")
(print "cavity_index = " cavity_index "\n")
(print "cavity_length = " cavity_length "\n")
(print "t1 = " t1 "\n")
(print "t2 = " t2 "\n")
(print "DBR_pair_thickness = " DBR_pair_thickness "\n")
(print "midgap = " midgap "\n")
(print "gapsize = " gapsize "\n")
(print "topgap = " topgap "\n")
(print "botgap = " botgap "\n")
(print "nmin = " nmin "\n")
(print "nmax = " nmax "\n")
(print "f0n = " f0n "\n")

(set! geometry-lattice
  (make lattice
    (basis-size lattice_basis_size 1       1      )
    (size       lattice_size       no-size no-size)
;;     (basis-size lattice_basis_size 1 no-size)
;;     (size       lattice_size       1 no-size)
  )
)

; resolution of one "basis cell"
;; (set! resolution (* 32 (+ 2 (* 2 N_mirror_pairs)) ))
;; (set! resolution 256)
(set! resolution 32)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; define geometry
(define center1 0)
(define center2 0)

;;; mirror pairs
(print "===> mirror pairs:\n")
(do ((idx 0 (+ idx 1))) ((>= idx N_mirror_pairs))
  (set! center1 (+ (/ cavity_length 2) (* idx DBR_pair_thickness) (/ t1 2) ) )
  (set! center2 (+ center1 (/ t1 2) (/ t2 2)) )

  (set! center1 (/ center1 lattice_basis_size) )
  (set! center2 (/ center2 lattice_basis_size) )

  (print "idx = " idx "\n")
  (print "  center1 " idx " -> " center1 "\n")
  (print "  center2 " idx " -> " center2 "\n")

  (set! geometry (append geometry (list
    (make block
      (center center1 0 0)
      (material (make dielectric (index n1)))
      (size t1 infinity infinity)
    )
    (make block
      (center center2 0 0)
      (material (make dielectric (index n2)))
      (size t2 infinity infinity)
    )

    (make block
      (center (- center1) 0 0)
      (material (make dielectric (index n1)))
      (size t1 infinity infinity)
    )
    (make block
      (center (- center2) 0 0)
      (material (make dielectric (index n2)))
      (size t2 infinity infinity)
    )

  )))
)

;;; cavity
(print "===> cavity:")
(set! geometry (append geometry (list
  (make block
    (center 0 0 0)
    (material (make dielectric (index cavity_index)))
    (size cavity_length infinity infinity)
  )
)))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define mybandfunc (combine-band-functions
  fix-hfield-phase output-hfield output-bpwr
  fix-dfield-phase output-dfield output-dpwr
  fix-efield-phase output-efield
))

(set-param! filename-prefix
  (string-append
    "DBR_defect_ncav_"
    (format false "~,2f" cavity_index) ; printf style formatting :)
;;     (number->string cavity_index)
    "-"
  )
)

(define N_unfolded_bands 2)

; INFO: resonance bands seem to be bands 22-24
; ncav=4 resonances: 0.28670   0.32138   0.40614 -> fmid = 0.34642

(if defect-mode?

  (begin
    ; define k-points
    (set! k-points (list (vector3 0.5 0 0) ))

    ; define number of bands
    (set-param! num-bands 3)
    (set-param! target-freq midgap)
    ;; (set-param! target-freq f0n)
    (set! tolerance 1e-8)

    ; run simulation
    (optimize-grid-size!)
    (run-tm mybandfunc)
  )
  
  (begin
    ; define k-points
    (set! k-points (list
      (vector3 -0.5 0 0)
      (vector3 0 0 0); Gamma
      (vector3 0.5 0 0)
    ))
    (set! k-points (interpolate 10 k-points))

    ; define number of bands
    (set-param! num-bands (* N_unfolded_bands (+ 2 (* 2 N_mirror_pairs))))

    ; run simulation
    (optimize-grid-size!)
    (run-tm)
  )
  
)

; output expected resonance frequency for reference
(print "f0n = " f0n "\n")

;; The TE and TM polarizations are defined has having electric and magnetic fields in the xy plane, respectively.
;; Equivalently, the H/E field of TE/TM light has only a z component (making it easier to visualize).
;; (run-te) ; H=Hz
;; (run-tm (output-at-kpoint (vector3  0.5 0 0)
;;   fix-hfield-phase output-hfield output-hpwr
;;   fix-dfield-phase output-dfield output-dpwr
;;   fix-efield-phase output-efield
;;   )) ; E=Ez

;; (run)

;; (run-tm (output-at-kpoint (vector3  0.5 0 0)
;;   mybandfunc
;; )) ; E=Ez
