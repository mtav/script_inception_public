(define (doit x x-max dx)
  (if (<= x x-max)
    (begin
      ...perform loop body with x...
      (doit (+ x dx) x-max dx)
    )
  )
)

(doit a b dx) ; execute loop from a to b in steps of dx

(do
  (
    (<variable1> <init1> <step1>)
    ...
  )
  (<test> <expression> ...)
  <command> ...
)

(do
  (
    (x a (+ x dx))
  )
  (
    (> x b)
  )
  ...perform loop body with x...
)

(do
  (
    (vec (make-vector 5))
    (i 0 (+ i 1))
  )
  (
    (= i 5) ; test expression
    vec ; return value
  )
  (vector-set! vec i i)
)              ; ==>  #(0 1 2 3 4)

(let
  (
    (x '(1 3 5 7 9))
  )
  (do
    (
      (x x (cdr x))
      (sum 0 (+ sum (car x)))
    )
    (
      (null? x)
      sum
    )
  )
)                ;==>  25

(map
  (lambda (x)
    ...do stuff with x...
  )
  list-of-x-values
)
