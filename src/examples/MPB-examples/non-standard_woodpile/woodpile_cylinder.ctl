;----------------------------------------------------------------------------------------------------------------
; File found on http://www.mail-archive.com/mpb-discuss@ab-initio.mit.edu/msg00511.html

; It does not actually give a "correct" woodpile!!! It's a woodpile where one layer is shifted relative to the other layer by more than a/2 (shifted by 5/6*a), as is usual with a = distance between rods in one layer.
; Also the distance between rods in a layer is not the same in the "X" and "Y" directions!

; For viewing:
; mpb ./woodpile_cylinder.ctl && mpb-data -r -n32 ./epsilon.h5 && h5tovtk -d data-new epsilon.h5 && paraview
; see also "-e" flag for mpb-data

; cartesian here means the original orthonormal x,y,z reference frame

; in cartesian:
; b1 = 0.5*[0,1,1]
; b2 = 0.5*[1,0,1]
; b3 = 0.5*[1,1,0]

; rod centres in cartesian:
; x1 = [0, 0, 0]
; x2 = [1/8, 1/8, 0]
; x3 = [1/2, 1/4, 1/4]
; x4 = [5/8, 3/8, 1/4]

; rod directions in cartesian are:
; xdir ~ [ 1, 1, 2] ~ b1 + b2 = u1 = u3
; ydir ~ [-1, 1, 0] ~ b1 - b2 = u2 = u4
; stacking direction in cartesian is zdir ~ [-1, -1, 1]
; vertical period = c = 1/sqrt(3)

; normalized directions in cartesian:
; xdir = [1/2, 1/2, 1]*sqrt(2/3)
; ydir = [-1/2, 1/2, 0]*sqrt(2)
; zdir = xdir^ydir = [-1, -1, 1]*1/sqrt(3)

; distance between rods in a layer periodic in xdir (layers 2 and 4): ax = Px = dot(b1,xdir) = sqrt(3/2)*1/2
; distance between rods in a layer periodic in ydir (layers 1 and 3): ay = Py = dot(b1,ydir) = sqrt(2)/4
; shift between rods in layers 2 and 4 along xdir: deltaX = dot(x4-x2,xdir) = sqrt(3/2)*5/12 = 5/6*Px
; shift between rods in layers 1 and 3 along ydir: deltaY = -dot(x3-x1,ydir) = sqrt(2)/8 = 1/2*Py
;----------------------------------------------------------------------------------------------------------------

; woodpile lattice ; using diamond lattice from the example files:
; Dielectric spheres in a diamond (fcc) lattice.  This file is used in
; the "Data Analysis Tutorial" section of the MPB manual.

; NOTE: basis1, basis2 and basis3 are normalized to be as long as specified in "basis-size"
(set! geometry-lattice (make lattice
 			 (basis-size (sqrt 0.5) (sqrt 0.5) (sqrt 0.5))
 			 (basis1 0 1 1)
 			 (basis2 1 0 1)
 			 (basis3 1 1 0)))

; NOTE: k-points are specified in the reciprocal lattice!!! (the reciprocal of the specified geometry-lattice)
; Corners of the irreducible Brillouin zone for the fcc lattice,
; in a canonical order:
(set! k-points (interpolate 4 (list
 			       (vector3 0 0.5 0.5)            ; X
 			       (vector3 0 0.625 0.375)        ; U
 			       (vector3 0 0.5 0)              ; L
 			       (vector3 0 0 0)                ; Gamma
 			       (vector3 0 0.5 0.5)            ; X
 			       (vector3 0.25 0.75 0.5)        ; W
 			       (vector3 0.375 0.75 0.375))))  ; K

; define a couple of parameters (which we can set from the command-line)
(define-param eps 13) ; the dielectric constant of the cylinders

;(define-param r 0.1)    ; the radius of the cylinders
(define-param r (/ 1 (sqrt 3) 4 2) )    ; the radius of the cylinders, so that they just touch each other

(define si (make dielectric (epsilon eps)))

; NOTE: The geometrical objects are specified in the "geometry-lattice" using basis1/2/3. Scalar values like radius, width, etc are specified in the original orthonormal x,y,z (cartesian) basis, i.e. in units of "a" (not the interRodDistance here)(cf MEEP units).
(set! geometry (list
 		(make cylinder ; layer 1
 		  (center 0 0 0) (radius r) (axis (vector3 1 1 0))
 		  (height infinity) (material si))
 		(make cylinder ; layer 2
 		  (center 0 0 (/ 1 4)) (radius r) (axis (vector3 1 -1 0))
 		  (height infinity) (material si))
 		(make cylinder ; layer 3
 		  (center 0 (/ 1 2) (/ 2 4)) (radius r) (axis (vector3 1 1 0))
 		  (height infinity) (material si))
 		(make cylinder ; layer 4
 		  (center 0 (/ 1 2) (/ 3 4)) (radius r) (axis (vector3 1 -1 0))
 		  (height infinity) (material si))
 		))

(set-param! resolution 24)
(set-param! num-bands 10)

(set! k-points (list ))

(run)
