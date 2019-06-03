; lists
(define koko (list 11 22 33))
(list-ref koko 0)
;; 11
(list-ref koko 1)
;; 22
(list-ref koko 2)
;; 33

; vectors

; arrays
(define a1 #1(11 42 33))

(define a2 #2(
(45 67 89)
(11 22 42)
))

(define a3 #3(
((45 67)
(5 6)
(5 6))

((11 22)
(33 66)
(5 6))

((56 5)
(42 8)
(5 6)) 

((56 5)
(7 8)
(5 6)) 

))

; single line definitions
; arrays
(define a1 #1(11 42 33))
(define a2 #2( (45 67 89) (11 22 42) ))
(define a3 #3( ((45 67)(5 6)(5 6)) ((11 22)(33 66)(5 6)) ((56 5)(42 8)(5 6)) ((56 5)(7 8)(5 6)) ))

; get array dimensions
(array-dimensions a1)
(array-dimensions a2)
(array-dimensions a3)

; get array shape
(array-shape a1)
(array-shape a2)
(array-shape a3)

; get array elements
(array-ref a1 1)
(array-ref a2 1 2)
(array-ref a3 2 1 0)

; print for convenience
(print (array-ref a1 1) "\n")
(print (array-ref a2 1 2) "\n")
(print (array-ref a3 2 1 0) "\n")

(exit)
