;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; This file demonstrates three different ways to return multiple values from a function in Scheme, since Scheme functions normally return just one value.
;;;;;;;;;;;;;;;;;;;;;;;;

;;;;; 1. values + let-values (the "proper" R6RS way)
;; (values 1 2 3) packages up three separate return values (not a list — a genuine multiple-value return).
;; let-values is the special form that knows how to unpack those values into a, b, c.
;; Output: (1 2 3)
;;
;; This is the standard/idiomatic mechanism defined in R6RS/R7RS for multiple returns.

;; This implementation requires importing the rnrs library.
;; In the Scheme programming language, rnrs refers to the standard library and modular system introduced in the R6RS (Revised⁶ Report on the Algorithmic Language Scheme) standard.
;; Key Details About rnrs
;; • Standardization: It stands for Revised [n] Report on the Algorithmic Language Scheme, where rnrs libraries provide the official modular framework for R6RS-compliant Scheme programs.
;; https://doc.guix.gnu.org/guile/2.0.14/en/html_node/rnrs-base.html
;; (import (rnrs))
;; (import (rnrs base))
(import (rnrs base (6)))

(define (foo1)
  (values 1 2 3))

(let-values (((a b c) (foo1)))
  (display (list a b c))
  (newline))

;;;;; 2. Continuation-passing style (CPS)
;; Instead of returning anything, foo2 takes a callback function k (the "continuation") as its argument.
;; foo2 calls k with the three values as arguments — control is passed forward into the callback rather than a value being passed back.
;; Output: (1 2 3)
;;
;; This is a classic functional-programming pattern (common in Scheme, JS callbacks, etc.) that sidesteps the need for a "return multiple values" feature entirely — you just push the values into a function that consumes them immediately.
(define (foo2 k)
  (k 1 2 3))

(foo2 (lambda (a b c) 
        (display (list a b c))
        (newline)))

;;;;; 3. Bundle into a list (the "cheat" method)
;; Simplest approach: just wrap the values in a single list, which is one value.
;; Caller gets result = (1 2 3) and can pull it apart with car/cadr/caddr etc. if needed.
;; Output: (1 2 3)
(define (foo3)
  (list 1 2 3))

(let ((result (foo3)))
  (display result)
  (newline))

(exit)
