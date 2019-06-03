;preamble - some interesting settings
(set! filename-prefix false)
(set! output-single-precision? true)
(set-param! resolution 56.8513)

;simulation size
(define-param sx 2.97267) ; x size
(define-param sy 4.57883) ; y size
(define-param sz 5.94533) ; z size
(set! geometry-lattice (make lattice (size 2.97267 4.57883 5.94533)))


;huhu
(
;test
define (factorial x)
;;test2
  (if (= x 0) ;;test3
         1 ;test4
         (* x (factorial (- x 1)))
  )
)
