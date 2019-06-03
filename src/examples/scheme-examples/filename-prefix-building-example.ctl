; filename-prefix building example
; subdirectories also work if they exist.
; directories can be created using (mkdir DIR)
;; Examples:
;; mpb test.ctl
;; mpb w=78 num-k-points=89  num-bands=90  outside-index=67.4242 mesh-size=9
;; mpb w=78 num-k-points=89  num-bands=90  outside-index=67.4242 mesh-size=9  filename-prefix=\"\"  test.ctl
;; mpb w=78 num-k-points=89  num-bands=90  outside-index=67.4242 mesh-size=9  filename-prefix=\"jijij\"  test.ctl
;; X=999.786
;; mpb w=78 num-k-points=89  num-bands=90  outside-index=67.4242 mesh-size=9  filename-prefix=\"jijij-${X}-\"  test.ctl

(define-param w 0.1)
(define-param h 0.2)
(define-param inside-index 4)
(define-param outside-index 2)
(define-param num-k-points 10)
;; (set-param! mesh-size 3)
(set-param! resolution 32)
;; (set-param! num-bands 10)

(set-param! filename-prefix
  (string-append
    "base"
    "_num-k-points-" (number->string num-k-points)
;;     "_mesh-size-" (number->string mesh-size)
    "_resolution-" (number->string resolution)
;;     "_num-bands-" (number->string num-bands)
    "_w-" (number->string w)
    "_h-" (number->string h)
    "_inside-index-" (number->string inside-index)
    "_outside-index-" (number->string outside-index)
    "_"
  )
)

(print filename-prefix "\n")

(define-param sy 1)
(define-param fcen 1)
(define-param df 1)
(define-param N 1)
(define-param compute-mode? true)

(set-param! filename-prefix
  (string-append
    "holey_waveguide_resonant_modes"
    "_sy-" (format #f "~,3f" sy)
    "_fcen-" (format #f "~,3f" fcen)
    "_df-" (format #f "~,3f" df)
    "_N-" (format #f "~2,'0d" N)
    "_compute-mode-" (if compute-mode? "true" "false")
    "_"
  )
)

(print filename-prefix "\n")

;; (run)
(exit)
