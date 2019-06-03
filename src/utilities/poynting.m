function P = poynting(E1,H1,E2,H2)
  % POYNTING Calculate the poynting vector for a set of data.
  %   POYNTING(E1,H1,E2,H2) calculates the time-averaged Poynting vector
  %   between electric and magnetic field vectors E and H.  This returns one
  %   component of the Poynting vector which can be chosen by choosing
  %   appropriate E1,E2,H1,H2.  To calculate S the determinant of a 3x3
  %   matrix is required.  This is defined by:    |i   j   k  | 
  %                                               |Ex  Ey  Ez |
  %                                               |Hx* Hy* Hz*|.
  %   Therefore the y-component is defined by: Ez.Hx*-Ex.Hz* etc...
  %
  % Created on 27/11/06 by Ian Buss. Version 1.
  %
  % Poynting vector unit: W/m^2

  P = 0.5*real(((E1.re+i.*E1.im).*conj(H2.re+i.*H2.im))-...
      ((E2.re+i.*E2.im).*conj(H1.re+i.*H1.im)));
end
