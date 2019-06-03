;minimize-multiple test
(define (Z X Y)
;;   (print "YOLO!!!!!!!!!!!!!!!!!!!!!!!!\n") ; just to show we can print or do all kinds of other weird stuff before returning the result.
  (* X (exp (* -1 (+ (expt X 2) (expt Y 2)) ) ) )
)

(define maxres (maximize-multiple Z 0.1 0 0) )
(define minres (minimize-multiple Z 0.1 0 0) )

(print "minimum: " (list-ref (min-arg minres) 0) " , " (list-ref (min-arg minres) 1) " , " (min-val minres) "\n")
(print "maximum: " (list-ref (max-arg maxres) 0) " , " (list-ref (max-arg maxres) 1) " , " (max-val maxres) "\n")

(exit)
