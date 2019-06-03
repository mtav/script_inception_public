;----------------------------------------------------------------------------------;
; Control file for simulation of diamond lattice of spherical balls/holes and cylinders.
; Adjust parameters accordingly.
;----------------------------------------------------------------------------------;
; CLI parameter passing example:
;  mpb empty-k-points?=true inner-rod?=false  useRCD2?=false filename-prefix=\"toto-\"  ./iceCrystal.ctl
;----------------------------------------------------------------------------------;

; load lattice and k-points
(load-from-path "all_FCC_BZ_labels.ctl")

(define-param cube-size  1 )
(define-param rod-height (* (/ (sqrt 3) 4) cube-size) )

(define-param rod-radius 0.24 )
(define-param rod-index-RCD 1 )
(define-param backfill-index 2.4 )

(define-param empty-k-points? false) ; if true, use empty k-points list (i.e. output epsilon.h5 only)

;Specifies the computational grid resolution , in pixels per lattice unit
(set-param! resolution 32)

;Number of bands (eigenvectors) to compute at each k point
(set-param! num-bands 10)

;Dielectric constant is averaged over a "mesh" of points
(set! mesh-size 3)

;Number of k-points to interpolate between specified k-points
(define num-k-points 10)

;----------------------------------------------------------------------------------;
;MPB required definitions and calculations
;Defines substrate material
(define rod-material (make dielectric (index rod-index-RCD)))

(set! k-points (interpolate num-k-points RCD_kpoints ))

; point definitions
(define p000 (vector3 0 0 0))
(define p100 (vector3 1 0 0))
(define p010 (vector3 0 1 0))
(define p001 (vector3 0 0 1))
(define pmid1 (vector3 0.25 0.25 0.25))

(define p111 (vector3 1 1 1))
(define p011 (vector3 0 1 1))
(define p101 (vector3 1 0 1))
(define p110 (vector3 1 1 0))
(define pmid2 (vector3 0.75 0.75 0.75))

(define pmid1-p000 (vector3* 0.5 (vector3+ pmid1 p000 ) ) )
(define pmid1-p100 (vector3* 0.5 (vector3+ pmid1 p100 ) ) )
(define pmid1-p010 (vector3* 0.5 (vector3+ pmid1 p010 ) ) )
(define pmid1-p001 (vector3* 0.5 (vector3+ pmid1 p001 ) ) )

(define pmid2-p111 (vector3* 0.5 (vector3+ pmid2 p111 ) ) )
(define pmid2-p011 (vector3* 0.5 (vector3+ pmid2 p011 ) ) )
(define pmid2-p101 (vector3* 0.5 (vector3+ pmid2 p101 ) ) )
(define pmid2-p110 (vector3* 0.5 (vector3+ pmid2 p110 ) ) )

(define pmid1-p000-axis (vector3- pmid1 p000 ) )
(define pmid1-p100-axis (vector3- pmid1 p100 ) )
(define pmid1-p010-axis (vector3- pmid1 p010 ) )
(define pmid1-p001-axis (vector3- pmid1 p001 ) )

(define pmid2-p111-axis (vector3- p111 pmid2 ) )
(define pmid2-p011-axis (vector3- p011 pmid2 ) )
(define pmid2-p101-axis (vector3- p101 pmid2 ) )
(define pmid2-p110-axis (vector3- p110 pmid2 ) )

; TODO: Create function to create cylinder object between two points? -> Extend MPB via ctl/scheme!
(define (cylinder_from_A_to_B A B r h mat)
  (make cylinder
    (material mat)
    (center (vector3* 0.5 (vector3+ A B)) )
    (radius r)
    ;; This part is problematic because the norm can only be calculated correctly in an orthonormal basis, but the input points might be defined in any basis.
    ;; (height (vector3-norm (vector3- B A)) )
    (height h )
    (axis (vector3- B A) )
  )
)

(print "============================\n")
(print "Starting calculation for r/a = " rod-radius  "\n")

;Sets spatial permittivity function
(begin ; why begin? -> To put multiple statement together into a group that can be put into if statements, etc

  (set! default-material (make dielectric (index backfill-index) ) )

  (set! geometry (list
    (cylinder_from_A_to_B pmid1 p000 rod-radius rod-height rod-material)
    (cylinder_from_A_to_B pmid1 p100 rod-radius rod-height rod-material)
    (cylinder_from_A_to_B pmid1 p010 rod-radius rod-height rod-material)
    (cylinder_from_A_to_B pmid1 p001 rod-radius rod-height rod-material)
  ))

)

(if empty-k-points?
  (set! k-points (list))
)

;;   (print "geometry = "geometry "\n")
(print "(length geometry) = " (length geometry) "\n")
;;   (print "k-points = "k-points "\n")
(print "(length k-points) = " (length k-points) "\n")

;Run and calculate modes for each Bloch wavevector
(run)

(print "r/a = " rod-radius " gap from band 2 to band 3 = " (retrieve-gap 2) "\n")
(print "============================\n")

(exit)
