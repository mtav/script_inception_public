(define (power base exponent)
  (cond
    ( (zero? exponent)
      1
    )
    ( (zero? (remainder exponent 2))
      (* (power base (quotient exponent 2)) (power base (quotient exponent 2)) )
    )
    ( else
      (* base (power base (quotient exponent 2)) (power base (quotient exponent 2)) )
    )
  )
)

; define the function f(x,y)
(define (f x y)
(list (* 2 x) (* -3 y))
;f(x) = a e^{- { \frac{(x-b)^2 }{ 2 c^2} } }
)

(define beam_centre_x -3)
(define beam_centre_y 7)
(define sigma_x 2)
(define sigma_y 7)
(define amplitude 5)

(define X 0)
(define Y 0)
(define R 0)
(define out 0)

(define (gaussian x y)
;X = x-self.beam_centre_x
;Y = y-self.beam_centre_y
;R = abs(numpy.sqrt( pow((X),2) + pow((Y),2) ))
;out = self.amplitude * numpy.exp( -( pow(X,2)/(2*pow(self.sigma_x,2)) + pow(Y,2)/(2*pow(self.sigma_y,2)) ) )
(set! X (- x beam_centre_x) )
(set! Y (- y beam_centre_y) )
(set! R (abs (sqrt ( + (expt X 2) (expt Y 2) ) ) ) )
(set! out (* amplitude (exp ( * -1 ( + (/ (expt X 2) (* 2 (expt sigma_x 2)) ) ( / (expt Y 2) (* 2 (expt sigma_y 2))) ) ))) )
out
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; example loop system
(define L 0)
(define a 0)
(define b 0)

; define the loop function
(define (doit x x-max dx)
  (if (<= x x-max)
    (begin
      ;;...perform loop body with x...

      (set! L (f x x))
      (set! a (list-ref L 0))
      (set! b (list-ref L 1))
      (print x ";" a ";" b "\n")
      (doit (+ x dx) x-max dx)
    )
  )
)

; define the loop parameters
(define-param n_low 1)
(define-param n_ratio_start 0)
(define-param n_ratio_end 10)
(define-param n_ratio_step 1)

; run the loop
;(doit n_ratio_start n_ratio_end n_ratio_step) ; execute loop from a to b in steps of dx

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; write function results to output file
(define (createCSV)
  (define xmin -10)
  (define xmax 10)
  (define dx 0.25)
  (define ymin -10)
  (define ymax 10)
  (define dy 0.25)

  (define result 0)

  (define outfile (open-output-file "test.out"))

  (do ((x xmin (+ x dx))) ((> x xmax))
    (do ((y ymin (+ y dy))) ((> y ymax))
      (set! result (gaussian x y))
      (print "f(" x ", " y ") = " result "\n")
      (display x outfile)
      (display "; " outfile)
      (display y outfile)
      (display "; " outfile)
      (display result outfile)
      (display "\n" outfile)
    )
  )

  (close-output-port outfile)
)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define xfixed 1)
(define yfixed 2)
(define (gaussian_xfixed y) (gaussian xfixed y) )
(define (gaussian_yfixed x) (gaussian x yfixed) )

(define result_xfixed (maximize gaussian_xfixed 0.00001 -10 10) )
(define result_yfixed (maximize gaussian_yfixed 0.00001 -10 10) )

(print "===========\n")
(print "max for xfixed = " xfixed " is " (max-val result_xfixed) " at y = " (max-arg result_xfixed) "\n" )
(print "max for yfixed = " yfixed " is " (max-val result_yfixed) " at x = " (max-arg result_yfixed) "\n" )
(print "===========\n")

(createCSV)
;(gaussian 2 3)

;; functions with local variables:
(print "-------------------------------\n")
(print "functions with local variables:\n")
(define local_x 5)
(define (f1 x)
  (define local_x 4)
  (define local_y (* 4 local_x))
  (print "local_y = " local_y "\n")
  (set! local_x 6)
  (set! local_y 2)
  (+ local_x local_y x)
)
(print "f1(3) = " (f1 3) "\n")
(print "local_x = " local_x "\n")
;; (print "xmin = " xmin "\n")

(define (f2 x)
  (let*
    (
      (local_a 4)
      (local_b 4)
    )
    (set! local_a 6)
    (set! local_b 2)
    (+ local_a local_b x)
  )
)

(print "f2(3) = " (f2 3) "\n")

;; using external variables
(define external_var 42)
(define (f3 x)
  (+ x external_var)
)
(print "f3(3) = " (f3 3) "\n")

;; (print "local_a = " local_a "\n")
;; (print "local_b = " local_b "\n")

;; Note:
;; 2.2 Lexical Binding
;; 
;; The three binding constructs let, let*, and letrec, give Scheme block structure. The syntax of the three constructs is identical, but they differ in the regions they establish for their variable bindings. In a let expression, the initial values are computed before any of the variables become bound. In a let* expression, the evaluations and bindings are sequentially interleaved. And in a letrec expression, all the bindings are in effect while the initial values are being computed (thus allowing mutually recursive definitions). 

(let ((x 2) (y 3))
            (let (
                    (x 7)
                    (foo (lambda (z) (+ x y z)))
                 )
              (foo 4)))                         ;  =>  9

(let ((x 2) (y 3))
            (let* (
                    (x 7)
                    (foo (lambda (z) (+ x y z)))
                 )
              (foo 4)))                         ;  =>  14

(letrec
  (
    (even?
      (lambda (n)
        (if (zero? n)
          #t
          (odd? (- n 1))
        )
      )
    )
    (odd?
      (lambda (n)
        (if (zero? n)
          #f
          (even? (- n 1))
        )
      )
    )
  )
  (even? 88)
)                         ;  =>  #t

;; let statements are useful to avoid this error: "definition in expression context, where definitions are not allowed"

;; this is not ok
;; (define (g x)
;;   (print "doing stuff\n")
;;   (define s 2)
;;   (* s x)
;; )

;; this is ok
(define (g x)
  (define s 2)
  (print "doing stuff\n")
  (* s x)
)

(print "g(3)=" (g 3) "\n")

;; this is ok
(define (g x)
  (print "doing stuff\n")
  (let ((s 2))
    (* s x)
  )
)

(print "g(3)=" (g 3) "\n")

(exit)
