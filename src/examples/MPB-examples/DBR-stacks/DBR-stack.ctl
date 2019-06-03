;;;;; DBR index values
(define-param eps1 12)
(define-param eps2 13)

(set-param! filename-prefix
  (string-append
    "DBR-stack_"
    (number->string eps1)
    "-"
    (number->string eps2)
    "-"
  )
)


(set! resolution 64)
(set-param! num-bands 3)

;; IMPORTANT: Do not set no-size values in basis-size!
;; This seems to mess things up a lot! (probably no-size=1/inf=1e-20, so setting both to no-size leads to too small values.)
(set! geometry-lattice
  (make lattice
    (size       1 no-size no-size)
  )
)

; define k-points
(set! k-points (list
  (vector3 -0.5 0 0)
  (vector3  0   0 0); Gamma
  (vector3  0.5 0 0)
))

(set! k-points (interpolate 10 k-points))

(set! geometry (list
  (make block
    (center -0.25 0 0)
    (material (make dielectric (epsilon eps1)))
    (size 0.5 infinity infinity)
  )
  (make block
    (center 0.25 0 0)
    (material (make dielectric (epsilon eps2)))
    (size 0.5 infinity infinity)
  )
))

(optimize-grid-size!)

;; The TE and TM polarizations are defined has having electric and magnetic fields in the xy plane, respectively.
;; Equivalently, the H/E field of TE/TM light has only a z component (making it easier to visualize).
;; (run-te) ; H=Hz
(run-tm (output-at-kpoint (vector3  0.5 0 0)
  fix-hfield-phase output-hfield output-hpwr
  fix-dfield-phase output-dfield output-dpwr
  fix-efield-phase output-efield
  )) ; E=Ez
;; (run)

(define eps_mid (/ (+ eps1 eps2) 2))

(define (energydist N)
  (get-dfield N)
  (compute-field-energy)
  (print "band " N ": energy in eps1=" eps1 " :" (compute-energy-in-dielectric eps1    eps_mid) "\n")
  (print "band " N ": energy in eps2=" eps2 " :" (compute-energy-in-dielectric eps_mid eps2   ) "\n")
)

(energydist 1)
(energydist 2)
(energydist 3)
