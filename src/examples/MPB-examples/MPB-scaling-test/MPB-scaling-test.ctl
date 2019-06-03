; number of primitive unit cells in one lattice cell (i.e. in a length basis-size)
(define-param scaling_factor 3)

(define-param lattice_size 3)
(define-param lattice_basis_size 1)

(define-param n1 1)
(define-param n2 3.5)

; total number of primitive unit cells in the simulation box
(define Ntot (* lattice_size scaling_factor) )

; total size of the simulation box
(define Ltot (* lattice_size lattice_basis_size) )

(define single_double_layer (/ lattice_basis_size scaling_factor) )

(define-param t1 (* single_double_layer (/ n2 (+ n1 n2)) ) )
(define-param t2 (* single_double_layer (/ n1 (+ n1 n2)) ) )

(set! geometry-lattice
  (make lattice
    (basis-size lattice_basis_size lattice_basis_size lattice_basis_size)
    (size lattice_size no-size no-size)
  )
)

(define center1 0)
(define center2 0)

(do ((idx 0 (+ idx 1))) ((>= idx Ntot))
  (set! center1 (+ (- (/ Ltot 2)) (* idx single_double_layer) (/ t1 2) ) )
  (set! center2 (+ center1 (/ t1 2) (/ t2 2)) )
  
  (print idx " -> " center1 "\n")
  (print idx " -> " center2 "\n")

  (set! geometry (append geometry (list
    (make block
      (center center1 0 0)
      (material (make dielectric (index n1)))
      (size t1 infinity infinity)
    )
    (make block
      (center center2 0 0)
      (material (make dielectric (index n2)))
      (size t2 infinity infinity)
    )
  )))
  
)

(map (lambda (b)
  (print (object-property-value b 'center) "\n")
) geometry)

;; (set! num-bands (* 4 scaling_factor))
(define-param scaling_factor_max 4)

(set-param! num-bands (* 4 scaling_factor_max 5))

(set! k-points (list
  (vector3 -0.5 0 0)
  (vector3 0 0 0); Gamma
  (vector3 0.5 0 0)
))

(set! k-points (interpolate 10 k-points))

; resolution of one lattice cell
(set! resolution (* 32 scaling_factor_max))

(set-param! filename-prefix
  (string-append
    "MPB-scaling-test"
    "_lattice_basis_size-" (number->string lattice_basis_size)
    "_lattice_size-" (number->string lattice_size)
    "_scale-" (number->string scaling_factor)
    "_"
  )
)

(optimize-grid-size!)

(run)
