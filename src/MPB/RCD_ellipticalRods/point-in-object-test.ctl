(set! geometry-lattice (make lattice
                         (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
                         (basis1 0 1 1)
                         (basis2 1 0 1)
                         (basis3 1 1 0)
                       )
)

(define (c->l . args) (cartesian->lattice (apply vector3 args)))
(define (l->c . args) (lattice->cartesian (apply vector3 args)))

(define obj
  (make block
    (center 0 0 0)
    (size 1 1 1)
  ;;   (e1 1 1 1)
  ;;   (e2 0 1 -1)
  ;;   (e3 -2 1 1)
  )
)

(point-in-object? (vector3 0 0 0) obj)

(point-in-object? (vector3 0.25 0.25 -0.25) obj)

(point-in-object? (c->l 0.25 0.25 -0.25) obj)
