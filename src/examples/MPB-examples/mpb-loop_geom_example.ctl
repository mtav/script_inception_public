(set-param! resolution 21)

(map (lambda (x) 

  (set-param! filename-prefix
    (string-append
      "base"
      "_x-" (number->string x)
      "_"
    )
  )

  (set! geometry (list
    (make sphere
      (center 0 0 0)
      (radius (/ x 2))
      (material (make dielectric (epsilon 2)))
    )
  ))

  (run)

) (list 0.1 0.2 0.3 0.4 0.5))
