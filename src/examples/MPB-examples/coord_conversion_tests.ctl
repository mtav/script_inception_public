(load-from-path "utilities.ctl")

(define (test pos_list _center _size _e1 _e2 _e3)
  (define newpos_list
    (object->lattice
              _center
              _size
              _e1
              _e2
              _e3
              pos_list
    )
  )

  (print "----------------------------------------\n")
  (print "_center = " (vector3->matlab _center) ";\n")
  (print "_size = " (vector3->matlab _size) ";\n")
  (print "_e1 = " (vector3->matlab _e1) ";\n")
  (print "_e2 = " (vector3->matlab _e2) ";\n")
  (print "_e3 = " (vector3->matlab _e3) ";\n")
  (print "M = [_size(1)*_e1(:)/norm(_e1), _size(2)*_e2(:)/norm(_e2), _size(3)*_e3(:)/norm(_e3)];\n")
  
  (map
    (lambda (pos newpos)
      (print "pos = " (vector3->matlab pos) ";\n")
      (print "newpos = _center(:) + M*pos(:);\n")
      (print "newpos(:)'\n")
      (print "newpos = " (vector3->matlab newpos) ";\n")
    )
    pos_list
    newpos_list
  )
)

; test 1
(define _center (vector3 11 22 33))
(define _size (vector3 2 3 4))
(define _e1 (vector3 1 0 0))
(define _e2 (vector3 0 1 0))
(define _e3 (vector3 0 0 1))

(define pos_list
  (list
    (vector3 2 4 5)
    (vector3 (random:uniform ) (random:uniform ) (random:uniform ))
    (vector3 (random:uniform ) (random:uniform ) (random:uniform ))
    (vector3 (random:uniform ) (random:uniform ) (random:uniform ))
  )
)

(test pos_list _center _size _e1 _e2 _e3)

; test 2
(define _center (vector3 (random:uniform ) (random:uniform ) (random:uniform )))
(define _size (vector3 (random:uniform ) (random:uniform ) (random:uniform )))
(define _e1 (vector3 (random:uniform ) (random:uniform ) (random:uniform )))
(define _e2 (vector3 (random:uniform ) (random:uniform ) (random:uniform )))
(define _e3 (vector3 (random:uniform ) (random:uniform ) (random:uniform )))

(define pos_list
  (list
    (vector3 2 4 5)
    (vector3 (random:uniform ) (random:uniform ) (random:uniform ))
    (vector3 (random:uniform ) (random:uniform ) (random:uniform ))
    (vector3 (random:uniform ) (random:uniform ) (random:uniform ))
  )
)

(test pos_list _center _size _e1 _e2 _e3)

; test 3
(define _center (vector3 (random:uniform ) (random:uniform ) (random:uniform )))
(define _size (vector3 (random:uniform ) (random:uniform ) (random:uniform )))
(define _e1 (vector3 (random:uniform ) (random:uniform ) (random:uniform )))
(define _e2 (vector3 (random:uniform ) (random:uniform ) (random:uniform )))
(define _e3 (vector3 (random:uniform ) (random:uniform ) (random:uniform )))

(define pos_list
  (list
    (vector3 2 4 5)
    (vector3 (random:uniform ) (random:uniform ) (random:uniform ))
    (vector3 (random:uniform ) (random:uniform ) (random:uniform ))
    (vector3 (random:uniform ) (random:uniform ) (random:uniform ))
  )
)

(test pos_list _center _size _e1 _e2 _e3)

(exit)
