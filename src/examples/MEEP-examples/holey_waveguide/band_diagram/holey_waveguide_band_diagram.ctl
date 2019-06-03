; Some parameters to describe the geometry:
(define-param eps 13) ; dielectric constant of waveguide
(define-param w 1.2) ; width of waveguide
(define-param r 0.36) ; radius of holes

; The cell dimensions
(define-param sy 12) ; size of cell in y direction (perpendicular to wvg.)
(define-param dpml 1) ; PML thickness (y direction only!)

(set! geometry-lattice (make lattice (size 1 sy no-size)))

(set! geometry
       (list (make block (center 0 0) (size infinity w infinity)
                   (material (make dielectric (epsilon eps))))
              (make cylinder (center 0 0) (radius r) (height infinity) (material air))))

(set-param! resolution 20)

(set! pml-layers (list (make pml (direction Y) (thickness dpml))))

(define-param fcen 0.25) ; pulse center frequency
(define-param df 1.5) ; pulse freq. width: large df = short impulse

(set! sources (list
               (make source
                 (src (make gaussian-src (frequency fcen) (fwidth df)))
                 (component Hz) (center 0.1234 0))))

(set! symmetries (list (make mirror-sym (direction Y) (phase -1))))

(define-param kx false) ; if true, do run at specified kx and get fields
(define-param k-interp 19) ; # k-points to interpolate, otherwise

(if kx
  (begin
    ;;;; run for a single k-point
    (set! k-point (vector3 kx))

    (set-param! filename-prefix
      (string-append
        "holey_waveguide_band_diagram"
        "_kx-" (format #f "~,2f" kx)
        "_fcen-" (format #f "~,4f" fcen)
        "_df-" (format #f "~,4f" df)
      )
    )

    (print "filename-prefix = " filename-prefix "\n")

    ;;;; from wiki:
    ;; (run-sources+ 300
    ;;   (after-sources (harminv Hz (vector3 0.1234) fcen df))
    ;; )
    ;;;; from meep src:
    (run-sources+ 300
      (at-beginning output-epsilon)
      (after-sources (harminv Hz (vector3 0.1234 0) fcen df))
    )
    (run-until (/ 1 fcen)
      (at-every (/ 1 fcen 20)
        ;; fix-hfield-phase ; this only exists in MPB
        output-hfield-z
      )
    )

  )
  (begin
    ;;;; run for a multiple k-points
    (run-k-points 300 (interpolate k-interp (list (vector3 0) (vector3 0.5))))
  )
)
