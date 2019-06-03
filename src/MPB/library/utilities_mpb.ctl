;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; simulation parameters
(set-param! verbose? true)
(set-param! resolution 32) ; this is problematic, because it is only overridden if passed by CLI... :/ -> workaround: set after loading...
(set-param! num-bands 10)
(define-param k-interp 9)
(define-param output_epsilon_only? false) ; if true, exit after outputting epsilon
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(if verbose?
  (begin
    (print "<----------------------------------------------\n")
    (print "Loading utilities_mpb.ctl with:\n")
    (print "  verbose? = " verbose? "\n")
    (print "  resolution = " resolution "\n")
    (print "  num-bands = " num-bands "\n")
    (print "  k-interp = " k-interp "\n")
    (print "  output_epsilon_only? = " output_epsilon_only? "\n")
  )
)

(load-from-path "utilities.ctl")

;; Return the list (gapratio gapmin midgap gapmax) for the gap from the band lower-band to the band lower-band+1.
;; gapratio is given as a percentage of mid-gap frequency.
;; gapratio may be negative if the maximum of the lower band is higher than the minimum of the upper band.
;; The gap is computed from the band-range-data of the previous run.
;; It basically works like (retrieve-gap lower-band), but also returns the min/mid/max values of the gap.
(define (retrieve-gap-fullinfo lower-band)
  (let
    (
      (gapmax "undefined")
      (gapmin "undefined")
      (midgap "undefined")
      (gapratio "undefined")
    )
    ; min band 3
    (set! gapmax (car (car (list-ref band-range-data lower-band) )))
    ; max band 2
    (set! gapmin (car (cdr (list-ref band-range-data (- lower-band 1)) )))
    ; compute midgap
    (set! midgap (* 0.5 (+ gapmax gapmin)) )
    ; compute gap ratio
    (set! gapratio (* 100 (/ (- gapmax gapmin) midgap )))
    ; return values
    (list gapratio gapmin midgap gapmax)
  )
)
