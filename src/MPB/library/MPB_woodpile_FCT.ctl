;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; This script defines the MPB_woodpile_FCT function which can be used to easily create woodpiles.
;;; It also defines the lattice based on the given _interRodDistance parameter.
;;; _lattice_mode can also be used to force an FCC or BCC lattice in which case _interRodDistance is ignored. (but it is modified accordingly to avoid confusion and accidental errors!)
;;; TODO: supercell support
;;; TODO: position support (to create two non-overlapping woodpiles for example...)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; Example usage:
;; (set-param! verbose? true)
;; (load-from-path "MPB_woodpile_FCT.ctl")
;; 
;; (set-param! resolution 32)
;; (set-param! num-bands 10)
;; (define-param k-interp 5)
;; (define-param elliptical-rod-shape? true)
;; 
;; (set! geometry
;;   (MPB_woodpile_FCT elliptical-rod-shape? (make dielectric (index 3)) 0.2 0.25)
;; )
;; 
;; (set! k-points (interpolate k-interp FCC_standard_kpoints))
;; 
;; (run)
;; 
;; (exit)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; reference values based on JOSA-B paper:
;; rod_height=0.25
;; rod_width=0.2145
;; rod-index=3.3
;; gap = 16%
;; gap range: 0.4853 - 0.5689
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; parameters that can be defined by the user before loading this script
(define-param _interRodDistance (sqrt 0.5)) ; distance between rods in one layer (horizontal period)
(define-param _lattice_mode 0) ; 0=FCT, 1=FCC, 2=BCC (FCC and BCC will override any interRodDistance setting)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(if verbose?
  (begin
    (print "<----------------------------------------------\n")
    (print "Loading MPB_woodpile_FCT.ctl with:\n")
    (print "  _interRodDistance = " _interRodDistance "\n")
    (print "  _lattice_mode = " _lattice_mode "\n")
  )
)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; lattice setup
; dimensions of the cubic unit-cell: _a,_b,_c
; FCC if _c = _a = _b to BCC if _c = _a/sqrt(2) = _b/sqrt(2)
(define _a 1)
(define _b 1)
(define _c 1)
(case _lattice_mode
  ; FCT
  ((0)(begin
    (if verbose?
      (print "  setting up FCT lattice\n")
    )
    (if (or (< _interRodDistance (sqrt 0.5)) (< 1 _interRodDistance))
      (error "Invalid _interRodDistance value. It must be in [(sqrt 0.5), 1].")
    )
    (set! _a (* (sqrt 2) _interRodDistance) )
    (set! _b (* (sqrt 2) _interRodDistance) )
    (set! _c 1)
  ))
  ; FCC
  ((1)(begin
    (if verbose?
      (print "  setting up FCC lattice\n")
    )
    (set! _a 1)
    (set! _b 1)
    (set! _c 1)
    (set! _interRodDistance (sqrt 0.5))
  ))
  ; BCC
  ((2)(begin
    (if verbose?
      (print "  setting up BCC lattice\n")
    )
    (set! _a (sqrt 2))
    (set! _b (sqrt 2))
    (set! _c 1)
    (set! _interRodDistance 1)
  ))
)

; sets geometry-lattice and canonical FCT-BZ labels based on given _a,_b,_c parameters
(load-from-path "all_FCT_BZ_labels.ctl")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define (MPB_woodpile_FCT elliptical-rod-shape? rod-material rod_width rod_height)
  (let*
    (
      (geometry_list (list))
      (rod1_center (c->l (*  0     _a) (*  0     _b) (*  0     _c)))
      (rod1_e1     (c->l (*  1     _a) (*  1     _b) (*  0     _c)))
      (rod1_e2     (c->l (*  1     _a) (* -1     _b) (*  0     _c)))
      (rod1_e3     (c->l (*  0     _a) (*  0     _b) (*  1     _c)))

      (rod2_center (c->l (*  0.125 _a) (*  0.125 _b) (*  0.250 _c)))
      (rod2_e1     (c->l (*  1     _a) (*  1     _b) (*  0     _c)))
      (rod2_e2     (c->l (*  1     _a) (* -1     _b) (*  0     _c)))
      (rod2_e3     (c->l (*  0     _a) (*  0     _b) (*  1     _c)))
    )
    (if elliptical-rod-shape?
      (begin
        (set! geometry_list
          (list
            (make ellipsoid (material rod-material)
              (center rod1_center)
              (e1 rod1_e1)
              (e2 rod1_e2)
              (e3 rod1_e3)
              (size infinity rod_width rod_height)
            )
            (make ellipsoid (material rod-material)
              (center rod2_center)
              (e1 rod2_e1)
              (e2 rod2_e2)
              (e3 rod2_e3)
              (size rod_width infinity rod_height)
            )
          )
        )
      )
      (begin
        (set! geometry_list
          (list
            (make block (material rod-material)
              (center rod1_center)
              (e1 rod1_e1)
              (e2 rod1_e2)
              (e3 rod1_e3)
              (size infinity rod_width rod_height)
            )
            (make block (material rod-material)
              (center rod2_center)
              (e1 rod2_e1)
              (e2 rod2_e2)
              (e3 rod2_e3)
              (size rod_width infinity rod_height)
            )
          )
        )
      )
    )
    geometry_list
  )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(if verbose?
  (begin
    (print "---------------------------------------------->\n")
  )
)
