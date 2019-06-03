(define-param output_epsilon_only? true) ; if true, exit after outputting epsilon

;; (load-from-path "all_FCT_BZ_labels.ctl")
;; (load-from-path "all_FCC_BZ_labels.ctl")
(load-from-path "lattice_orthorhombic_simple.ctl")

(define-param k-interp 0)

(set_kpoints kpoints_all)

(run-mpb run)
(exit)
