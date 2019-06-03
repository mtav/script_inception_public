(set! num-bands 2)

(set! k-points (list (vector3 0 0 0)          ; Gamma
                     (vector3 0 0.5 0)        ; M
                     (vector3 (/ -3) (/ 3) 0) ; K
                     (vector3 0 0 0)))        ; Gamma
(set! k-points (interpolate 4 k-points))

(set! geometry (list (make cylinder
                       (center 0 0 0) (radius 0.2) (height infinity)
                       (material (make dielectric (epsilon 12))))))

(set! geometry-lattice (make lattice (size 1 1 no-size)
                        (basis1 (/ (sqrt 3) 2) 0.5)
                        (basis2 (/ (sqrt 3) 2) -0.5)))

(set! resolution 32)

(define toto 0)

(define (first-tm-gap r)

(print "======================\n")
(print "r = " r "\n")

  (set! geometry (list (make cylinder
                        (center 0 0 0) (radius r) (height infinity)
                        (material (make dielectric (epsilon 12))))))
  (run-tm)
  

  (set! toto (retrieve-gap 1))
(print "r = " r " toto = " toto "\n")
(print "======================\n")

toto
) ; return the gap from TM band 1 to TM band 2

(set! mesh-size 7) ; increase from default value of 3

(define result (maximize first-tm-gap 0.1 0.1 0.5))
(print "radius at maximum: " (max-arg result) "\n")
(print "gap size at maximum: " (max-val result) "\n")
