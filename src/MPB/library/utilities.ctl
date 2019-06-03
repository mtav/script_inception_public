;; To load:
;; (load-from-path "utilities.ctl")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; Useful constants
(define pi (acos -1))
(define c0 299792458)
(define golden_ratio (/ (+ 1 (sqrt 5)) 2) )
(define golden_spiral_radius_growth (/ (log golden_ratio) (/ pi 2)) )

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; functions normally available in MIT/GNU scheme, but missing in MPB/guile for some reason:
;; TODO: finish this
;; (define (append-map procedure . args)
;;   (print "yolo\n")
;;   (print args "\n")
;;   (print "yala\n")
;; ;;   (apply append (map procedure args))
;; ;;   (map )
;; ;;     (lambda (x y)
;; ;;     ;...do stuff with x...
;; ;;     (print "x=" x ", y = " y "\n")
;; ;;   )
;;   (map
;;     (lambda (x y)
;;       ;...do stuff with x...
;;       (print "x=" x ", y = " y "\n")
;;     )
;;     .
;;     args
;;   )
;; 
;; )
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; useful functions
(define (init+output-epsilon-mpb)
  (init-params NO-PARITY true); for MPB
  (output-epsilon)
)

; TODO: maybe pass args to run function, such as output fields, etc
(define (run-mpb run_function)
  (if output_epsilon_only?
    (init+output-epsilon-mpb)
    (run_function)
  )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; Coordinate conversion functions usable to define vectors directly (ex: (l->c 1 2 3))
;; The original functions only work with "vector3" arguments, while these only work with 3 float arguments.
;; Both return a "vector3".
(define (l->c . args) (lattice->cartesian (apply vector3 args)))
(define (c->l . args) (cartesian->lattice (apply vector3 args)))
(define (r->c . args) (reciprocal->cartesian (apply vector3 args)))
(define (c->r . args) (cartesian->reciprocal (apply vector3 args)))
(define (r->l . args) (reciprocal->lattice (apply vector3 args)))
(define (l->r . args) (lattice->reciprocal (apply vector3 args)))

;; cartesian <-> cylindrical
;; TODO
;; (define (cartesian->cylindrical vec3)
;; 
;; )
;; 
;;  inline Double_t TMath::ATan2(Double_t y, Double_t x)
;;   455    { if (x != 0) return  atan2(y, x);
;;   456      if (y == 0) return  0;
;;   457      if (y >  0) return  Pi()/2;
;;   458      else        return -Pi()/2;
;;   459    }
;;   
;;    Double_t TVector3::Theta() const
;;   315 {
;;   316    return fX == 0.0 && fY == 0.0 && fZ == 0.0 ? 0.0 : TMath::ATan2(Perp(),fZ);
;;   317 }
;;   Double_t TVector3::Phi() const
;;   307 {
;;   308    return fX == 0.0 && fY == 0.0 ? 0.0 : TMath::ATan2(fY,fX);
;;   309 }
;;   310 
;;   

;; convert coordinates defined in the (O,e1,e2,e3) referential into its coordinates in the lattice referenctial:
(define (object->lattice
          _center
          _size
          _e1
          _e2
          _e3
          pos_list
        )

  (let*
    (
      (_e1_final (cartesian->lattice (vector3-scale (vector3-x _size) (unit-vector3 (lattice->cartesian _e1)))))
      (_e2_final (cartesian->lattice (vector3-scale (vector3-y _size) (unit-vector3 (lattice->cartesian _e2)))))
      (_e3_final (cartesian->lattice (vector3-scale (vector3-z _size) (unit-vector3 (lattice->cartesian _e3)))))
      (M (matrix3x3 _e1_final _e2_final _e3_final))
    )
    (map
      (lambda (pos)
        (vector3+ _center (matrix3x3* M pos) )
      )
      pos_list
    )
  )
)

;; Returns 3 vectors (in the form of a matrix3x3 so it can directly be used for conversions) forming a direct orthogonal basis, with the last one being equal to the input vector.
;; The 3 vectors are based on the spherical coordinate system with (e_phi, e_theta, e_r) (radial distance r, azimuthal angle θ, and polar angle φ).
;; Both the input and output vectors are defined in lattice coordinates.
;; Note that no normalization is done!
(define (get_axis_referential e_r_lat)

  (define e_r_cart (lattice->cartesian e_r_lat))
  (if (= (vector3-norm e_r_cart) 0)
    (error "e_r_cart is a null vector")
  )
  
  (let*
    (
      (e_theta_cart
        (if
          (and
            (= (vector3-x e_r_cart) 0)
            (= (vector3-y e_r_cart) 0)
          )
          (vector3-cross e_r_cart (vector3 1 0 0) )
          (vector3-cross (vector3 0 0 1) e_r_cart )
        )
      )
      
      (e_phi_cart (vector3-cross e_theta_cart e_r_cart))
      
      (e_phi_lat (cartesian->lattice e_phi_cart))
      (e_theta_lat (cartesian->lattice e_theta_cart))
    )
    (matrix3x3 e_phi_lat e_theta_lat e_r_lat)
  )
    
;;     (matrix3x3 
;;       (vector3 1 0 0)
;;       (vector3 0 1 0)
;;       (vector3 0 0 1)
;;     )
;;     (let*
;;       (
;;         (c_cart (lattice->cartesian e_r))
;;         (b_cart (vector3-cross (vector3 0 0 1) c_cart))
;;         (a_cart (vector3-cross b_cart c_cart))
;;         (a_lat (cartesian->lattice a_cart))
;;         (b_lat (cartesian->lattice b_cart))
;;         (c_lat (cartesian->lattice c_cart))
;;       )
;;       (matrix3x3 a_lat b_lat c_lat)
;;     )
;;   )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; k-point (label . coordinates) system to enable label printing

(define (map-cdr L)
  (map
    (lambda (x)
      (cdr x)
    )
    L
  )
)

(define (map-car L)
  (map
    (lambda (x)
      (car x)
    )
    L
  )
)

(define (print_kpoints_labels kpoint_list)
  (map
    (lambda (x)
      (print (car x) "\n")
    )
    kpoint_list
  )
  (print); just to return nothing
)

(define (print_kpoints_coordinates_reciprocal kpoint_list)
  (map
    (lambda (x)
      (print "in reciprocal basis: " (car x) " : " (cdr x) "\n")
    )
    kpoint_list
  )
  (print); just to return nothing
)

(define (print_kpoints_coordinates_cartesian kpoint_list)
  (map
    (lambda (x)
      (print "in cartesian basis: "(car x) " : " (reciprocal->cartesian (cdr x)) "\n")
    )
    kpoint_list
  )
  (print); just to return nothing
)

(define (print_kpoints_labels_matlab_style kpoint_list)
  (let*
    (
      (S "{")
      (N (length kpoint_list))
    )
    (do ((idx 0 (+ idx 1))) ((>= idx N))
      (if (> idx 0)
        (set! S (string-append S "," ))
      )
      (set! S (string-append S "'" (car (list-ref kpoint_list idx)) "'"))
    )
    (print S "}\n")
  )
)

(define (set_kpoints kpoint_list)
  (set! k-points (interpolate k-interp (map-cdr kpoint_list)))
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; printing utilities
(define (vector3->matlab v)
  (format #f "[ ~f, ~f, ~f ]" (vector3-x v) (vector3-y v) (vector3-z v))
)

(define (printMatrix M)
  (print "[" (vector3->matlab (matrix3x3-row M 0)) ",\n")
  (print     (vector3->matlab (matrix3x3-row M 1)) ",\n")
  (print     (vector3->matlab (matrix3x3-row M 2)) "]\n")
)

(define (printFunctionMatrix func)
  (define M (matrix3x3
    (func (vector3 1 0 0))
    (func (vector3 0 1 0))
    (func (vector3 0 0 1))
  ))
  (printMatrix M)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; geometry utilities
(define (curve_from_coordinates
          _center
          _size
          _e1
          _e2
          _e3
          use_rods?
          voxel_function
          rod_function
          vertex_list
        )

  (define new_vertex_list
    (object->lattice
              _center
              _size
              _e1
              _e2
              _e3
              vertex_list
    )
  )

  (if use_rods?
    
    ; use rods
    (apply append! 
      (map
        rod_function
        (list-head new_vertex_list (- (length new_vertex_list) 1))
        (list-tail new_vertex_list 1)
      )
    )
    
    ; use voxels
    (map voxel_function new_vertex_list)
  )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(if verbose?
  (begin
    (print "---------------------------------------------->\n")
  )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; some old reference code:

; Loop through the k-points and do stuff.
; We do multiple single runs, because otherwise it crashes. MPB apparently does not like a too discontinuous k-point list.
;; (map (lambda (x)
;;   (print (reciprocal->cartesian x ) "\n")
;; ) X_kpoints )
;; 
;; (map (lambda (x)
;;   (print (reciprocal->cartesian x ) "\n")
;; ) L_kpoints )

;; (map (lambda (x)
;;   (print (reciprocal->cartesian x ) "\n")
;; ) (append (list Gamma) reciprocal_lattice_vectors X_kpoints L_kpoints W_kpoints) )

;; (map (lambda (x)
;;   (print (reciprocal->cartesian x ) "\n")
;; ) (append (list Gamma) reciprocal_lattice_vectors X_kpoints L_kpoints W_kpoints K_kpoints U_kpoints) )

;; (map (lambda (x)
;;   (print (reciprocal->cartesian x ) "\n")
;; ) (append reciprocal_lattice_vectors label_list) )

;; (map (lambda (x)
;;   (print (reciprocal->cartesian x ) "\n")
;; ) (append (list Gamma) reciprocal_lattice_vectors ) )

;; (print "number of labels: " (length label_list) "\n")

;; -------------------------------------------------------
;; code for elliptical cylinders for RCD structures.
(define (projected-distance d u v)
  ; d: distance to project
  ; u: vector direction of d
  ; v: vector direction to project on
  ; returns d' = abs( d / cos(angle(u,v)) )
  ; with cos(angle(u,v)) = dot(u,v)/(norm(u)*norm(v))
  (abs (/ d (/ (vector3-dot u v) (* (vector3-norm u) (vector3-norm v)))))
)

(define-class elliptical-cylinder-RCD geometric-object
  ; class specifically meant for elliptical cylinders used in RCD, with the cartesian Z-axis always in the "cutoff-planes".
  (define-post-processed-property axis (vector3 0 0 1) 'vector3 unit-vector3)
  (define-property size-vertical no-default 'number non-negative?)
  (define-property size-horizontal no-default 'number non-negative?)
  (define-property height no-default 'number non-negative?)
)

(define (get_components ell-cyl-RCD)
  (let*
  
    ; local variables
    (
      ; centers
      ( ellipsoid-center (object-property-value ell-cyl-RCD 'center) )
      ( block-center (object-property-value ell-cyl-RCD 'center) )

      ; axes
      ( block-e2 (vector3 0 0 1) )
      ( block-e3 (lattice->cartesian (object-property-value ell-cyl-RCD 'axis)) )
      ( block-e1 (vector3-cross block-e2 block-e3) )

      ( ellipsoid-e3 block-e3 )
      ( ellipsoid-e1 block-e1 )
      ( ellipsoid-e2 (vector3-cross ellipsoid-e3 ellipsoid-e1) )

      ; sizes
      (h (object-property-value ell-cyl-RCD 'size-vertical) )
      (w (object-property-value ell-cyl-RCD 'size-horizontal) )
      (hz (projected-distance h ellipsoid-e2 block-e2) )
      ( ellipsoid-size (vector3 w h infinity ) )
      ( block-size (vector3 w hz (object-property-value ell-cyl-RCD 'height) ) )
    )

    ; return value
    (list
      (make ellipsoid
        (center ellipsoid-center)
        (e1 (cartesian->lattice ellipsoid-e1))
        (e2 (cartesian->lattice ellipsoid-e2))
        (e3 (cartesian->lattice ellipsoid-e3))
        (size ellipsoid-size)
      )
      (make block
        (center block-center)
        (e1 (cartesian->lattice block-e1))
        (e2 (cartesian->lattice block-e2))
        (e3 (cartesian->lattice block-e3))
        (size block-size)
      )
    )
  )
)
;; -------------------------------------------------------
