(display "Welcome!")(newline)
(print "Hello world!\n")

(define list1 (list 1 2 3))
(define list2 (list 4 5 6))
(define list3 (append list1 list2))

(print list1 "\n")
(print list2 "\n")
(print list3 "\n")

;; (exit)

(define (celsius->fahrenheit celsius)
(display "HOHO")(newline)
(+ (* 1.8 celsius) 32))

;y = -6*x^5+5*x^4+3x^3+2x^2+1x+9
(define (y1 x)
(+ (* -6 (expt x 5)) (* 5 (expt x 4)) (* 3 (expt x 3)) (* 2 (expt x 2)) (* 1 (expt x 1)) (* 9 (expt x 0)) )
)

(define (y2 x)
;; (print "===== \n")
;; (print "===== \n")
(* (- x 1) (- x 2) (- x 3) (- x 4) (- x 5))
)

(define result (maximize y2 0.000001 0 2.5))
(print "x at maximum1: " (max-arg result) "\n")
(print "y at maximum1: " (max-val result) "\n")

(define result (maximize y2 0.000001 2.5 5))
(print "x at maximum2: " (max-arg result) "\n")
(print "y at maximum2: " (max-val result) "\n")
(exit)

(exit)
