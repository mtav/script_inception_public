; MPB speed hack test
(set! num-bands 8)
(set! k-points (list (vector3 0 0 0)     ; Gamma
                     (vector3 0.5 0 0)   ; X
                     (vector3 0.5 0.5 0) ; M
                     (vector3 0 0 0)))   ; Gamma
(set! k-points (interpolate 4 k-points))
(set! geometry (list (make cylinder
                       (center 0 0 0) (radius 0.2) (height infinity)
                       (material (make dielectric (epsilon 12))))))
(set! geometry-lattice (make lattice (size 1 1 no-size)))
(set! resolution 32)

(print "===================\n")
;(run)

;cond example:
;(cond ((= 2 1)(print "A\n")) ((= 3 1)(print "B\n")) ((= 4 1)(print "C\n")) (else (print "D\n"))  )

(define k_idx 0)

(define (increment_k_idx which-band)
  (cond
    ((= which-band 1)
      (set! k_idx (+ k_idx 1))
      ;(print k_idx "\n")
    )
  )
)

(define (lolify which-band)
;; (if (= which-band 1)
;;            (display "hey, it's true!\n")
;;            (display "dude, it's false\n"))

  (if (= which-band 1)
    (begin
      ;(print band-range-data "\n")
      (print k_idx "\n")
      (print current-k "\n")
      (print freqs "\n")
    )
  )
)

(run increment_k_idx (output-at-kpoint (vector3 0.5 0 0) lolify) )

(print "===================\n")
;Output Variables
;Global variables whose values are set upon completion of the eigensolver.

;A list of the frequencies of each band computed for the last k point. Guaranteed to be sorted in increasing order. The frequency of band b can be retrieved via (list-ref freqs (- b 1)).
(print freqs "\n") ; list of num-bands elements

;The number of iterations required for convergence of the last k point.
(print iterations "\n") ; integer

;A string describing the current required parity/polarization ("te", "zeven", etcetera, or "" for none), useful for prefixing output lines for grepping.
(print parity "\n") ; "te","tm","",etc

;Yet more global variables are set by the run function (and its variants), for use after run completes or by a band function (which is called for each band during the execution of run.

;The k point (from the k-points list) most recently solved.
(print current-k "\n") ;vec3
;This is a list of the gaps found by the eigensolver, and is set by the run functions when two or more k-points are solved. (It is the empty list if no gaps are found.)
(print gap-list "\n") ;[list of (percent freq-min freq-max) lists]
;For each band, this list contains the minimum and maximum frequencies of the band, and the associated k points where the extrema are achieved. Note that the bands are defined by sorting the frequencies in increasing order, so this can be confused if two bands cross.
(print band-range-data "\n") ;[list of ((min . kpoint) . (max . kpoint)) pairs (of pairs)]
(print "===================\n")
(print ( length band-range-data ) "\n")

;(run-tm output-efield-z)
;(run-te (output-at-kpoint (vector3 0.5 0 0) output-hfield-z output-dpwr))
(exit)
