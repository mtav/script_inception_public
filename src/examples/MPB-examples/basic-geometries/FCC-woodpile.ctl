; basic FCC-woodpile geometry

; example usage:
;mpb rod-index=1.285 FCC-woodpile.ctl | tee FCC-woodpile-rod-index-1.285.out
;mpb rod-index=1.332 FCC-woodpile.ctl | tee FCC-woodpile-rod-index-1.332.out

; sets geometry-lattice and canonical FCC-BZ labels
(load-from-path "all_FCC_BZ_labels.ctl")

; based on example from:
; http://www.mail-archive.com/mpb-discuss@ab-initio.mit.edu/msg00512.html
; Steven G. Johnson
; Tue, 17 Feb 2009 12:27:20 -0800
; Woodpile structure.  Note that a general woodpile is an fct lattice,
; but with the correct log height it is fcc, and that is what is used here.
; (It turns out that the optimal structure is pretty close to fcc
; anyway, so we don't gain much by going to fct.) -> KIT begs to differ.

(define-param k-interp 9)

(set! k-points (interpolate k-interp FCC_standard_kpoints))
;; (set! k-points (list))

(define-param backfill-index 1 )
(define-param rod-index 1.285 )

(define-param elliptical-rod-shape? true); elliptical rods
;(define-param elliptical-rod-shape? false); rectangular rods

(set! default-material (make dielectric (index backfill-index) ) )
(define rod-material (make dielectric (index rod-index)))

(define au_microns (* 4 0.900 (- 1 0.5)) )

(define-param dw (sqrt 0.5)) ; distance between rods in one layer (horizontal period)
(define-param dh 0.25 ) ; distance between layers (vertical period)

(define-param w (/ 0.500 au_microns) ) ; width of the logs
(define-param h (/ 0.900 au_microns) ) ; height of logs (should be 1/4 for fcc to not overlap)

(define overlap (- 1 (/ dh h)) )

; print summary of essential parameters
(print "backfill-index = " backfill-index "\n")
(print "rod-index = " rod-index "\n")
(print "w = " w "\n")
(print "h = " h "\n")
(print "dw = " dw "\n")
(print "dh = " dh "\n")
(print "overlap = " overlap "\n")
(print "elliptical-rod-shape? = " elliptical-rod-shape? "\n")

; shortcut for cartesian->lattice function:
(define (c->l . args) (cartesian->lattice (apply vector3 args)))

(set! geometry

;;   (make ellipsoid (material rod-material)
;;     (center (c->l 0 0 0))
;;     (e1 (c->l 1 1 0))
;;     (e2 (c->l 1 -1 0))
;;     (e3 (c->l 0 0 1))
;;     (size infinity w h))
;;   (make ellipsoid (material rod-material)
;;     (center (c->l 0.125 0.125 dh))
;;     (e1 (c->l 1 1 0))
;;     (e2 (c->l 1 -1 0))
;;     (e3 (c->l 0 0 1))
;;     (size w infinity h))
;; 
;;    (make block (material (make dielectric (epsilon 10)))
;;     (center 0 0 0)
;;     (e1 (c->l 1 0 0))
;;     (e2 (c->l 0 1 0))
;;     (e3 (c->l 0 0 1))
;;     (size 1 0.1 0.1))
;; 
;;    (make block (material (make dielectric (epsilon 20)))
;;     (center 0 0 0)
;;     (e1 (c->l 1 0 0))
;;     (e2 (c->l 0 1 0))
;;     (e3 (c->l 0 0 1))
;;     (size 0.1 1 0.1))
;; 
;;    (make block (material (make dielectric (epsilon 30)))
;;     (center 0 0 0)
;;     (e1 (c->l 1 0 0))
;;     (e2 (c->l 0 1 0))
;;     (e3 (c->l 0 0 1))
;;     (size 0.1 0.1 1))
;; 
;;    (make block (material (make dielectric (epsilon 40)))
;;     (center 0 0 0)
;;     (size 1 0.1 0.1))
;; 
;;    (make block (material (make dielectric (epsilon 50)))
;;     (center 0 0 0)
;;     (size 0.1 1 0.1))
;; 
;;    (make block (material (make dielectric (epsilon 60)))
;;     (center 0 0 0)
;;     (size 0.1 0.1 1))

  (if elliptical-rod-shape?
    (begin
      (list
        (make ellipsoid (material rod-material)
          (center (c->l 0 0 0))
          (e1 (c->l 1 1 0))
          (e2 (c->l 1 -1 0))
          (e3 (c->l 0 0 1))
          (size infinity w h))
        (make ellipsoid (material rod-material)
          (center (c->l 0.125 0.125 dh))
          (e1 (c->l 1 1 0))
          (e2 (c->l 1 -1 0))
          (e3 (c->l 0 0 1))
          (size w infinity h))
      )
    )
    (begin
      (list
        (make block (material rod-material)
          (center (c->l 0 0 0))
          (e1 (c->l 1 1 0))
          (e2 (c->l 1 -1 0))
          (e3 (c->l 0 0 1))
          (size infinity w h))
        (make block (material rod-material)
          (center (c->l 0.125 0.125 dh))
          (e1 (c->l 1 1 0))
          (e2 (c->l 1 -1 0))
          (e3 (c->l 0 0 1))
          (size w infinity h))
      )
    )
  )
)

(set-param! resolution 32)
(set-param! num-bands 10)
(run)
