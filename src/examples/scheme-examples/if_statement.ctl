(define-param x true)

(if x
  (begin
    (print "true\n")
;;     (print "F-RD + NOT inner-rod\n")
;;     (set! geometry (append outer-rod-PCD-list outer-rod-FRD-list) )
  )
  (begin
    (print "false\n")
;;     (print "PCD + NOT inner-rod\n")
;;     (set! geometry (append outer-rod-PCD-list ) )
  )
)

(exit)
