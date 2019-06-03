(define L1 (list 1 2 3))
(define L2 (list 4 5 6))

(define (foo x y)
  (print "x = " x ", y = " y "\n")
  (list x y)
)

(define out
  (apply append 
    (map
      foo
      L1
      L2
    )
  )
)

(print out "\n")

     
(define compose
  (lambda (f g)
    (lambda args
      (f (apply g args))
    )
  )
)

((compose sqrt *) 12 75)
; =>  (sqrt (* 12 75)) = 30
          
(define (append-map procedure . args)
  (define (fifi . args)
    (lambda (. _args)(map
      procedure
      . _args
    )
  )
  (print "yolo\n")
  (print args "\n")
  (print "yala\n")
;;   (apply append (map procedure args))
;;   (map )
;;     (lambda (x y)
;;     ;...do stuff with x...
;;     (print "x=" x ", y = " y "\n")
;;   )
  (map
    (lambda (x y)
      ;...do stuff with x...
      (print "x=" x ", y = " y "\n")
    )
    .
    args
  )

  
  (apply append 
    (apply args
      (map
        procedure
        args
      )
    )
  )
)

(define out
  (append-map
    foo
    L1
    L2
  )
)

(print out "\n")

(exit)
