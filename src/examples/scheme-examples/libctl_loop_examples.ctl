; set up variables
(define-param a 1)
(define-param b 2)
(define-param dx 0.2)

(print "METHOD 0\n")
;The most frequently asked question seems to be: how do I write a loop in Scheme? We give a few answers to that here, supposing that we want to vary a parameter x from a to b in steps of dx, and do something for each value of x.
;The classic way, in Scheme, is to write a tail-recursive function:

(define (doit x x-max dx)
  (if (<= x x-max)
    (begin
      ;...perform loop body with x...
      (print "x=" x "\n")
      (doit (+ x dx) x-max dx)
    )
  )
)

(doit a b dx) ; execute loop from a to b in steps of dx

(print "METHOD 1\n")
;There is also a do-loop construct in Scheme that you can use
(do ((x a (+ x dx))) ((> x b))
  ;...perform loop body with x...
  (print "x=" x "\n")
)

(print "METHOD 2\n")
;If you have a list of values of x that you want to loop over, then you can use map:
(map
  (lambda (x)
    ;...do stuff with x...
    (print "x=" x "\n")
  )
  ;list-of-x-values
  (list 42 24 1337 3.141592653589793)
)

(print "Using map + interpolate:\n")
(map
  (lambda (x)
    ;...do stuff with x...
    (print "x=" x "\n")
  )
  ;list-of-x-values
  (interpolate 9 (list 0 1))
)

(print "example of a k-point scan:\n")
(define k_points
  (map (lambda (kx)
    (map (lambda (ky)
  ;;     (print "k=(" kx ", " ky ")\n")
      (vector3  kx ky 0)
    ) (interpolate 9 (list 0 0.5)) )
  ) (interpolate 9 (list 0 0.5)) )
)

; Note: GNU scheme seems to offer map-append and map-append!, which should make the following unncessary.
; However, it does not seem to be available in MPB/guile.
(define k_points_flat (apply append! k_points))

(print "k_points_flat = " k_points_flat "\n")

(print "mapping two lists:\n")
; mapping two lists
(map
  (lambda (x y)
    ;...do stuff with x...
    (print "x=" x ", y = " y "\n")
  )
  (list 1 2 3 4 5 6)
  (list 11 22 33 44 55 66)
)

(print "list diff:\n")

(define L (list 1 2 4 7 11 16))
(define Ldiff
  (map
    (lambda (x y)
      ;...do stuff with x...
      (print "x=" x ", y = " y ", y-x = " (- y x) "\n")
      (- y x)
    )
    (list-head L (- (length L) 1))
    (list-tail L 1)
  )
)

(print L "\n")
(print Ldiff "\n")

(exit)
