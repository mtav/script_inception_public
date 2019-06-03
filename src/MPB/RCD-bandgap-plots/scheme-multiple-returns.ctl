(import (rnrs))

; let-values + values
(define (foo1)
  (values 1 2 3))

(let-values (((a b c) (foo1)))
  (display (list a b c))
  (newline))

; cps
(define (foo2 k)
  (k 1 2 3))

(foo2 (lambda (a b c) 
        (display (list a b c))
        (newline)))

; list
(define (foo3)
  (list 1 2 3))
(let ((result (foo3)))
  (display result)
  (newline))

(exit)
