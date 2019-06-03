; MEEP code for the calculation of the transmission and reflection spectra  
; for a polaritonic SiC slab under normal incidence.
;
; Two calculations are needed. 
;  1) A reference calcuation without the slab (to get the incident flux)
;     meep-mpi ref?=true polaritonic_slab_3D.ctl > flux_inc.out
;  2) With the structure:
;     meep-mpi ref?=false polaritonic_slab_3D.ctl > flux_inc.out
;
(use-output-directory )
(set! eps-averaging? false)
; units
(define a 1e-6) ; define the unit, 1 um
(define cc (/ (* 2 (* pi 3e+8)) a)) ; unit of frequency in meep
(define-param theta_deg 0)     ; angle in degrees.

; cm-1->radpersec
(define (cm-1->radpersec l) 
	(* 2 pi 3e+10 l)
)

; eV->radpersec
(define (ev->radpersec l)
  (/ l 6.5821e-16) ; divide by the reduced Planck's constant
)

; SiC
(define SiC_wTO (/ (cm-1->radpersec 793.0) cc))
(define SiC_gamma (/ (cm-1->radpersec 4.76) cc))
(define SiC_sigma 3.3040529602496)
(define SiC_epsinf 6.7)
(define SiC_fcen 0.08) ; wTO/cc 

(define SiC
  (make dielectric (epsilon SiC_epsinf)
    (E-susceptibilities (make lorentzian-susceptibility
    (omega SiC_wTO)
    (gamma SiC_gamma)
    (sigma SiC_sigma)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;; Dimensions
(define-param pmlthick 3)
(define-param sy 3)
(define-param sz 3)
(define-param sx 14)

; use reference structrure ? true : no slab
(define-param ref? false)

;fields? == true -> use a CW source at a specific frequency to calculate the fields
(define-param fields? false)
(define-param CWfreq 0.06) ; 0.08 is inside the gap
(define-param dfcont 0.15)

;; Frequencies
(define-param fcen SiC_fcen) ; pulse center frequency
(define-param df 0.20) ; pulse bandwidth
(define-param dfe 0.20) ; data extraction bandwidth

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; Geometry 
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(set! geometry-lattice (make lattice (size (+ sx (* pmlthick 2)) sy sz)))
(set! geometry (list
               (make block (center 0 0 0) (size 5.0 sy sz)
                     (if ref?
			 (material (make dielectric (epsilon 1)))
		     ; else
			 (material Ag)
		     )
	       )
	       )
)
; resolution
(set! resolution 10)
(set! Courant 0.25)
(define-param nfreq 400) ; number of frequencies at which to compute flux
;; PML
(set! pml-layers (list (make pml (thickness pmlthick) (direction X))))


(define wlength (/ 1 fcen)) ; pulse wavelength

;; Set periodicity along y

;; USE THIS APPROACH 
;; http://www.mail-archive.com/meep-discuss@ab-initio.mit.edu/msg00697.html
(set! k-point (vector3 0 0 0))
(set! ensure-periodicity true)


(if fields? (set-param! fcen CWfreq))


      (print "Gaussian source \n")
      ;; set sources
       (set! sources (list
              (make source
                (src (make gaussian-src (frequency fcen) (fwidth df)))
                (component Hz)
                (center (+(/ sx -2) 1) 0 0)
                (size 0 sy sz)
                
                ;(amp-func (pw-amp k (vector3 0 (* -0.5 sx)))))
              )
))

;; !!!IMPORTANT!!!:  add-flux should always follow the definition of sources
(define trans ; transmitted flux
     (add-flux fcen dfe nfreq
                (make flux-region
                (center (- (/ sx 2) 1 1)  0) (size 0 sy sz))))
(define refl ; reflected flux
     (add-flux  fcen dfe nfreq
                (make flux-region
                (center (+ (/ sx -2) 1.5) 0 0)
		(size 0 sy sz))))

(if (not ref?) 
    (begin
      (print "load-minus-flux\n")
    (load-minus-flux "refl-flux" refl)
      (print "load-minus-flux done\n" )))

(run-sources+
 (stop-when-fields-decayed 100 Hz 
   (vector3 (- (/ sx 2) 1.5) 0 0) 1e-3) 
 (at-beginning output-epsilon) 
)

(if ref? (save-flux "refl-flux" refl))

(display-fluxes trans refl) 

