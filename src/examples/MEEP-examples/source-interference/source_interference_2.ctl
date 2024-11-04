;--------------Simulation box--------------------------------------------------------------------
(define-param scale 1)
(define-param sx (* scale 16))
(define-param sy (* scale 8))

(set! geometry-lattice (make lattice (size sx sy no-size)))

;--------------Simulation resolution--------------------------------------------------------------------
(set! resolution 10); total number of cells: X: 16*10=160, Y: 8*10=80

;--------------absorbing layer specification-----------------------------------------------------
(set! pml-layers (list (make pml (thickness 1.0))))

;--------------Geometry--------------------------------------------------------------------------
; no geometry, only vacuum

;--------------Source----------------------------------------------------------------------------
; a source in the Ez direction of normalized wavelength lambda_n=2, which means normalized frequency f_n=1/lambda_n=1/2
; the corresponding normalized period is then T_n=2.
(set! sources (list
 (make source
   (src (make continuous-src (frequency 0.5))) ; f=0.5*c0/a -> lambda = c0/f = c0/(0.5*c0/a) = 2*a
   (component Ez)
   (center (- (/ sx 4)) 0))
 ; (make source
   ; (src (make continuous-src (frequency 0.5))) ; f=0.5*c0/a -> lambda = c0/f = c0/(0.5*c0/a) = 2*a
   ; (component Ez)
   ; (center (/ sx 4) 0))
))

; (set! sources (list
 ; (make source
   ; (src (make continuous-src (frequency 0.5))) ; f=0.5*c0/a -> lambda = c0/f = c0/(0.5*c0/a) = 2*a
   ; (component Ez)
   ; (center 0 0))
; ))

; (set! sources (geometric-objects-lattice-duplicates sources))
; (set! sources (geometric-objects-duplicates (vector3 1 0 0) 0 2 sources))

;--------------Run simulation---------------------------------------------------------------------
; (run-until 200
           ; (at-beginning output-epsilon)
           ; (at-end output-efield-z))

;;;;; put output in a subdirectory
(use-output-directory) ; put output in a subdirectory
; (use-output-directory "mydir") ; put output in subdirectory "mydir"

  ;(at-beginning output-epsilon)
(run-until 20 ; This is 10*T_n, so 10 periods
  (to-appended "ez" (at-every 0.2 output-efield-z)) ; since T_n=2, this should give us 10 points per period and 100 output files in total.
  ; (at-every 0.2 (output-png Hz "-vZc dkbluered -M 1"))
  ; (at-every 0.2 (output-png Hz "-R -Zc dkbluered"))
)
