function [ E_meV, lambda_nm, real_neff, radius_vector_mum, E_vector_meV, lambda_vector_nm, real_neff_vector, u, v, b, v_cutoff ] = resonanceEnergy(n_cavity, n_mirror, n_outside, Lcav_nm, radius_mum, L, M)
  %resonanceEnergy(3.521,2.973,1,253,radius_mum)
  %input:
  % n_cavity=3.521;%no unit
  % n_mirror=2.973;%no unit
  % n_outside = 1; % air refractive index
  % Lcav_nm = 253; % (nm)
  % radius_mum (mum) of micropillar microcavity (kn in nm^-1 and v has no unit)
  %output:
  % E_meV (meV)
  % lambda_nm (nm)
  
  % Mode LPlm
  %L = 0;
  %M = 1;

  racines_l = zero_besselj(L);
  racines_l_moins_1 = zero_besselj(L-1);

  switch L
    case {0},
      borne_u_inf = racines_l_moins_1(M);
      borne_u_sup = racines_l(M);
    case {1},
      borne_u_inf = racines_l_moins_1(M);
      borne_u_sup = racines_l(M+1);
    otherwise,
      borne_u_inf = racines_l_moins_1(M+1);
      borne_u_sup = racines_l(M+1);
  end

  v_cutoff = borne_u_inf;
  v_max =100;
  % v_max =12;
  v = (v_cutoff+0.01):0.2:v_max; % normalized waveguide parameter
  n_points = length(v);
  u = zeros(n_points, 1);

  u_min = borne_u_inf + sqrt(eps); % eps = Spacing of floating point numbers

  % calculate the u values corresponding to v, so that eq_transc_bv(u,v,L)=0
  for i = 1:n_points
    u_max = min( v(i)-sqrt(eps), abs(borne_u_sup-sqrt(eps)));
    if sign(eq_transc_bv(u_min, v(i), L)) ~= sign(eq_transc_bv(u_max, v(i), L))
      if isnan(eq_transc_bv(u_min, v(i), L))
        error('NAN type 1')
      end
      if isnan(eq_transc_bv(u_max, v(i), L))
        error('NAN type 2')
      end
      
      if inoctave
        opts = optimset('TolX', 1e-5); % Create/alter optimization OPTIONS structure.
      else
        opts = optimset('Display', 'off', 'TolX', 1e-5); % Create/alter optimization OPTIONS structure.
      end
      u(i) = fzero(@(u) eq_transc_bv(u, v(i), L), [u_min u_max], opts); % Single-variable nonlinear zero finding.
    else
      u(i) = v(i);
    end 
  end

  b = 1 - (u.^2 ./ v'.^2); % normalized propagation constant
  w = sqrt(v'.^2 - u.^2);

  %%%%%%%%%%%%%%%%%%%%%%
  % calculate lambda_nm and E_meV as a function of the obtained u values (and the related v,w,b)
  %%%%%%%%%%%%%%%%%%%%%%
  real_neff_vector = n_mirror + b*(n_cavity-n_mirror);

  approx_neff = get_neff(n_cavity, n_mirror); % average refractive index
  lambda_vector_nm = sqrt(b.*(approx_neff^2-n_outside^2)+n_outside^2)*Lcav_nm*(n_cavity/approx_neff); % (nm)

  k0 = 2*pi./lambda_vector_nm; % free space wave number
  kn = k0.*sqrt(n_cavity^2-n_mirror^2); 
  radius_vector_mum = v./(kn'*1000); % radius_mum (mum) of micropillar microcavity (kn in nm^-1 and v has no unit)

  E_vector_eV = (get_h()*get_c0()/get_e())./(lambda_vector_nm.*10^(-9)); %energy (eV)
  E_vector_meV = E_vector_eV'*1000; % energy (meV)
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Calculate E_meV and lambda_nm for the values of radius_mum (input argument) using simple interpolation
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  E_meV = [];
  lambda_nm = [];
  real_neff = [];
  for i=1:length(radius_mum)
    r = radius_mum(i);
    idx = find(min(abs(radius_vector_mum-r))==abs(radius_vector_mum-r));
    if r<radius_vector_mum(idx)
      if idx-1>0
        E_meV = [E_meV, interpolate(radius_vector_mum, E_vector_meV, idx-1, idx, r)];
        lambda_nm = [lambda_nm, interpolate(radius_vector_mum, lambda_vector_nm, idx-1, idx, r)];
        real_neff = [real_neff, interpolate(radius_vector_mum, real_neff_vector, idx-1, idx, r)];
      else
        E_meV = [E_meV, E_vector_meV(1)];
        lambda_nm = [lambda_nm, lambda_vector_nm(1)];
        real_neff = [real_neff, real_neff_vector(1)];
      end
    else
      if idx+1 <= length(radius_vector_mum)
        E_meV = [E_meV, interpolate(radius_vector_mum, E_vector_meV, idx, idx+1, r)];
        lambda_nm = [lambda_nm, interpolate(radius_vector_mum, lambda_vector_nm, idx, idx+1, r)];
        real_neff = [real_neff, interpolate(radius_vector_mum, real_neff_vector, idx, idx+1, r)];
      else
        E_meV = [E_meV, E_vector_meV(length(radius_vector_mum))];
        lambda_nm = [lambda_nm, lambda_vector_nm(length(radius_vector_mum))];
        real_neff = [real_neff, real_neff_vector(length(radius_vector_mum))];
      end
    end
  end

end
