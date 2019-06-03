;----------------------------------------------------------------------------------;
;Control file for simulation of diamond lattice of spherical balls/holes and cylinders.
;Adjust parameters accordingly.
;Justin L. Stay
;Modified by Mike Taverne
;----------------------------------------------------------------------------------;
(define rod-height 1 )
(define rod-radius (* 0.26 rod-height) )
(define cube-size (* (/ 4 (sqrt 3)) rod-height) )
(define L (* (sqrt 0.5) cube-size) )

;Specify basis vectors and lattice size of computational/primitive unit cell
;Note: basis1 ,basis2 ,basis3 are DIRECTION ONLY , magnitudes are set in basis-size
(set! geometry-lattice (make lattice
                        (basis-size L L L)
                        (basis1 (vector3 0 1 1))
                        (basis2 (vector3 1 0 1))
                        (basis3 (vector3 1 1 0))))
                        
;Specifies the computational grid resolution , in pixels per lattice unit
(set-param! resolution 16)

;Number of bands (eigenvectors) to compute at each k point
(set-param! num-bands 10)

;Dielectric constant is averaged over a "mesh" of points
(set! mesh-size 3)

;Number of k-points to interpolate between specified k-points
(define num-k-points 10)

;Define radius of cylindrical rods/holes
(define sphere-radius 0.10)
;----------------------------------------------------------------------------------;
;MPB required definitions and calculations
;Defines substrate material
(define substrate (make dielectric (index 3)))

;Critical points of irreducible Brillouin Zone



;List of Bloch wavevectors to compute bands ,
;expressed in basis of reciprocal lattice vectors!
(set! k-points
        (interpolate num-k-points (list k1 k2 k3 k4 k5 k6 k7)))

; to have a sphere at the origin
;; (define delta (vector3 0 0 0))

; to have a cylinder at the origin
(define delta (vector3 -0.125 -0.125 -0.125))

(define p000 (vector3 0 0 0))
(define p100 (vector3 1 0 0))
(define p010 (vector3 0 1 0))
(define p001 (vector3 0 0 1))
(define pmid (vector3 0.25 0.25 0.25))

(define pmid-p000 (vector3* 0.5 (vector3+ pmid p000 ) ) )
(define pmid-p100 (vector3* 0.5 (vector3+ pmid p100 ) ) )
(define pmid-p010 (vector3* 0.5 (vector3+ pmid p010 ) ) )
(define pmid-p001 (vector3* 0.5 (vector3+ pmid p001 ) ) )

;Sets spatial permittivity function
(begin
  (set! default-material air)
  (set! geometry
    (list
;;       (make sphere (material substrate) (center (vector3+ p000 delta)) (radius sphere-radius))
;;       (make sphere (material substrate) (center (vector3+ pmid delta)) (radius sphere-radius))
      (make cylinder
        (material substrate)
        (center (vector3+ pmid-p000 delta) )
        (radius rod-radius)
        (height rod-height )
        (axis 0.25 0.25 0.25 )
      )
      (make cylinder
        (material substrate)
        (center (vector3+ pmid-p100 delta) )
        (radius rod-radius)
        (height rod-height )
        (axis 0.75 -0.25 -0.25 )
      )
      (make cylinder
        (material substrate)
        (center (vector3+ pmid-p010 delta) )
        (radius rod-radius)
        (height rod-height )
        (axis -0.25 0.75 -0.25 )
      )
      (make cylinder
        (material substrate)
        (center (vector3+ pmid-p001 delta) )
        (radius rod-radius)
        (height rod-height )
        (axis -0.25 -0.25 0.75 )
      )
    )
  )
)

;; (set! k-points (list))

;Run and calculate modes for each Bloch wavevector
(run)
