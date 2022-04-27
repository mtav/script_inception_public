;; example script to collect time domain signal at one point
(define-param fcen 1)
(define-param df 1)
(define-param sampling_time (/ 1 fcen 20))

(print "fcen : " fcen "\n")
(print "df : " df "\n")
(print "sampling_time : " sampling_time "\n")

(set! sources
  (list
    (make source
      (src (make gaussian-src (frequency fcen) (fwidth df)))
      (component Ez) (center 0 0)
    )
  )
)

(run-sources
  (in-volume (volume (center 0 0) (size 0 0))
    (to-appended "ez-source" (at-every sampling_time output-efield-z))
  )
)
