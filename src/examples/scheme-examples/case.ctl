(define-param x 0)
(case x
  ((0)(begin
    (print "0\n")
  ))
  ((1)(begin
    (print "1\n")
  ))
  ((2)(begin
    (print "2\n")
  ))
  (else
    (print "else\n")
  )
)
(exit)
