; customize parameters
;; (define-param k-interp 9)
(define-param r 0.24)
(define-param inside-index 1)
(define-param outside-index 2.4)
;; (set! resolution 100)

; load MPB utilities
(load-from-path "utilities_mpb.ctl")

; load RCD with round rods geometry, including FCC lattice and labels
(load-from-path "RCD_round_rods.ctl")

;;--------------------------
;; for quick testing
;; (set-param! num-bands 3)
;; (set-param! mesh-size 3)
;; (set-param! resolution 100)
;; (set! resolution 100)
;; 
;; (set_kpoints
;;   (list Gamma
;;     X+z
;;     W+z+x
;;     K+x+z
;;     L+x+y+z
;;     U+z+x+y
;;     X+z
;;   )
;; )
;;--------------------------

;; (set-param! filename-prefix
;;   (string-append
;;     "nrod_" (number->string inside-index)
;;     "_nbg-" (number->string outside-index)
;;     "_r-" (number->string r)
;;     "nrod_" (format #f "~,2f" inside-index)
;;     ".nb_" (format #f "~,2f" outside-index)
;;     ".rn_" (format #f "~,2f" r)
;;     "_"
;;   )
;; )

(define DSTDIR
  (string-append
    "output-"
    "nrod_" (format #f "~,2f" inside-index)
    ".nbg_" (format #f "~,2f" outside-index)
  )
)

(set-param! filename-prefix
  (string-append
    DSTDIR
    "/"
    "nrod_" (format #f "~,2f" inside-index)
    ".nbg_" (format #f "~,2f" outside-index)
    ".rn_" (format #f "~,2f" r)
    "_"
  )
)

(run-mpb run)

;; (run)

;; (define gap (retrieve-gap 2))
;; (define gapinfo (retrieve-gap-fullinfo 2))
;; (print gapinfo "\n")
;; (print gap-list "\n")

;; ;;   (set! gap (retrieve-gap 2))
;; (print " gap = " gap "\n")
;; 
;; band-range-data [ list of ((min .  kpoint) . (max . kpoint)) ]
;; 
;; (list-ref band-range-data 9)
;; $13 = ((0.9864206879251937 . #(0.5 0.5 0.0)) 1.1175885815472653 . #(0.5 0.75 0.25))
;; 
;; gap-list
;; $9 = ((11.426490249914075 0.6204291655199117 0.6956181761075705))
;; 
;; (define (retrieve-gap-fullinfo lower-band)
;;   (let
;;     (
;;       (gapmax "undefined")
;;     )
;;     (set! gapmax 42)
;;     (list gapmax (+ gapmax lower-band))
;;   )
;; )

;; min = (car (car a))
;; max = (car (cdr a))

(exit)
