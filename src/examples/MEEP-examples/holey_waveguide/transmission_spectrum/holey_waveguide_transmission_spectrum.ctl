; -----------------------------------------------------
;;;;; Values from the official MEEP tutorial
; Some parameters to describe the geometry:
;; (define-param eps 13) ; dielectric constant of waveguide
;; (define-param w 1.2) ; width of waveguide
;; (define-param r 0.36) ; radius of holes
;; (define-param d 1.4) ; defect spacing (ordinary spacing = 1)
;; (define-param N 3) ; number of holes on either side of defect

;; (define-param fcen 0.25) ; pulse center frequency
;; (define-param df 0.2)  ; pulse width (in frequency)

;; (define-param fcen (/ (+ 0.25 0.2) 2)) ; pulse center frequency
;; (define-param df (- 0.25 0.2 ))  ; pulse width (in frequency)
; -----------------------------------------------------
;;;;; Values for a quarter-wave DBR with n1=1, n2=2.4, w=0.34mum, lambda0=0.637mum
; Some parameters to describe the geometry:
(define lambda0_mum 0.637)
(define n1 1)
(define n2 2.4)
(define d1_mum (/ lambda0_mum (* 4 n1)))
(define d2_mum (/ lambda0_mum (* 4 n2)))
(define a_mum (+ d1_mum d2_mum))
(define w_mum 0.34)
(define d1 (/ d1_mum a_mum))
(define d2 (/ d2_mum a_mum))
(define-param eps (expt n2 2)) ; dielectric constant of waveguide
;; (define-param w (/ w_mum a_mum)) ; width of waveguide
(define-param w 1) ; width of waveguide
(define-param r (/ d1 2)) ; radius of holes
(define-param d 1) ; defect spacing (ordinary spacing = 1)
(define-param N 3) ; number of holes on either side of defect

(define midgap (/ (+ n1 n2) (* 4 n1 n2)) )
(define gapsize (* (/ 4 pi) (asin (/ (abs (- n1 n2)) (+ n1 n2)) ) )); relative gap size: omega/(delta(omega))
(define topgap (* midgap (+ 1 (/ gapsize 2))) )
(define botgap (* midgap (- 1 (/ gapsize 2))) )

(define-param fcen
  (/
    (+ d1 d2)
    (* 2 (+ (* n1 d1) (* n2 d2)))
  )
)
(define-param df (* 2 (- topgap botgap)))

(print "fcen = " fcen "\n")
(print "df = " df "\n")
(print "botgap = " botgap "\n")
(print "midgap = " midgap "\n")
(print "topgap = " topgap "\n")
(print "w = " w "\n")
(print "w_mum = " (* w a_mum) "\n")

; -----------------------------------------------------

; The cell dimensions
(define-param sy 6) ; size of cell in y direction (perpendicular to wvg.)
(define-param pad 2) ; padding between last hole and PML edge
(define-param dpml 1) ; PML thickness

(define sx (+ (* 2 (+ pad dpml N)) d -1)) ; size of cell in x direction

(set! geometry-lattice (make lattice (size sx sy no-size)))

(set! geometry
      (append ; combine lists of objects:
       (list (make block (center 0 0) (size infinity w infinity)
                   (material (make dielectric (epsilon eps)))))
       (geometric-object-duplicates (vector3 1 0) 0 (- N 1)
        (make cylinder (center (/ d 2) 0) (radius r) (height infinity)
              (material air)))
       (geometric-object-duplicates (vector3 -1 0) 0 (- N 1)
        (make cylinder (center (/ d -2) 0) (radius r) (height infinity)
              (material air)))))

(set! pml-layers (list (make pml (thickness dpml))))
(set-param! resolution 20)

(define-param nfreq 5000) ; number of frequencies at which to compute flux

(set! sources (list
               (make source
                 (src (make gaussian-src (frequency fcen) (fwidth df)))
                 (component Ey)
                 (center (+ dpml (* -0.5 sx)) 0)
                 (size 0 w))))

(set! symmetries (list (make mirror-sym (direction Y) (phase -1))))

(define trans ; transmitted flux
        (add-flux fcen df nfreq
                  (make flux-region
                    (center (- (* 0.5 sx) dpml 0.5) 0) (size 0 (* w 2)))))

; TODO: why only during sources and not after?
(run-sources+ (stop-when-fields-decayed
               50 Ey
               (vector3 (- (* 0.5 sx) dpml 0.5) 0)
               1e-3)
              (at-beginning output-epsilon)
              (during-sources
               (in-volume (volume (center 0 0) (size sx 0))
                (to-appended "hz-slice" (at-every 0.4 output-hfield-z)))))

(display-fluxes trans) ; print out the flux spectrum
