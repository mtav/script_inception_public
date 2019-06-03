;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; simulation parameters
(set-param! verbose? true)
(set-param! resolution 32) ; this is problematic, because it is only overridden if passed by CLI... :/ -> workaround: set after loading...
(define-param k-interp 9)
(define-param output_epsilon_only? false) ; if true, exit after outputting epsilon
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(if verbose?
  (begin
    (print "<----------------------------------------------\n")
    (print "Loading utilities_meep.ctl with:\n")
    (print "  verbose? = " verbose? "\n")
    (print "  resolution = " resolution "\n")
    (print "  k-interp = " k-interp "\n")
    (print "  output_epsilon_only? = " output_epsilon_only? "\n")
  )
)

(load-from-path "utilities.ctl")

(define (init+output-epsilon-meep)
  (init-fields) ; for MEEP
  (output-epsilon)
)
