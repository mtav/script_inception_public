; ------------------------- BEGIN ----------------------------
; Original by Steven G. Johnson, modified by Ashifi Gogo (Jan 2007)
; with help from Markus Testorf.
; This example creates an approximate TM planewave in vacuum
; propagating at an arbritrary angle between 0 and 90 degrees,
; by using one current source.

(use-output-directory)             ; put all output in a new directory
(define-param source-component Ez) ; field component to use

(define-param theta_deg 13.55)     ; angle in degrees.
; theta_deg goes from 0 (plane wave with k along +Y) to 90
; (plane wave with k along +X)
; possible angles are: 0, 4.48, 8.98, 13.55 etc
; they satisfy theta = asin(m*lambda/d), where m is an integer such
; that asin() can be evaluated. d is the width of the computational cell
; assumed to be bigger than lambda.

(define-param fcen 0.8) ; pulse center frequency
(define-param df 0.02) ; turn-on bandwidth
(define wlength (/ 1 fcen)) ; pulse wavelength

(define-param sx 16) ; the size of the comp cell in X, not including PML
(define-param dpml 5) ; thickness of PML layers

; set periodicity in the X direction. The PML takes care of the
; non-desired Y periodicity that comes for free with the k-point declaration
(set! k-point (vector3 0 0 0))
(set! ensure-periodicity true)

(define sy (+ sx (* 2 dpml))) ; cell size in Y direction, including PML
(set! geometry-lattice (make lattice (size sx sy no-size)))

; we'll only have PML in the Y direction (top and bottom)
(set! pml-layers (list (make pml (thickness dpml) (direction Y))))

(set-param! resolution 10)

; pw-amp is a function that returns the amplitude exp(ik(x+x0)) at a
; given point x.  (We need the x0 because current amplitude functions
; in Meep are defined relative to the center of the current source,
; whereas we want a fixed origin.)  Actually, it is a function of k
; and x0 that returns a function of x ...
(define ((pw-amp k x0) x)
   (exp (* 0+1i (vector3-dot k (vector3+ x x0)))))

(define theta_rad (/ (* pi theta_deg) 180))

; direction of k (length is irrelevant)
(define-param kdir (vector3 (sin theta_rad) (cos theta_rad)))

; k with correct length
(define k (vector3-scale (* 2 pi fcen) (unit-vector3 kdir)))

(set! sources (list
        (make source
         (src (make continuous-src (frequency fcen) (fwidth df)))
         (component source-component) (center 0 (* -0.5 sx)) (size sx 0)
         (amp-func (pw-amp k (vector3 0 (* -0.5 sx)))))
))

(run-until (* 1 40)
        (at-every 1 (output-png source-component "-Zc gray")))
; to run, copy and paste the following at the shell, in the same
; directory as this file (called single-source.ctl):
;rm single-source-out/*
;meep single-source.ctl
;cd single-source-out/
;convert ez-*.png 1.gif
;cd ..

;------------------------- END -------------------------------
