function [ real_neff_1,real_neff_2,real_neff_1_vector,real_neff_2_vector,radius_vector_mum, u, v, b, v_cutoff ] = get_neff_2(radius_mum,n_inside,n_outside,L,M,lambda_nm)
  % cf optical electronics in modern communications, fifth edition, by Amnon Yariv, chapter 3, p 88-95 notably

  if exist('n_inside','var') == 0; n_inside = 2.4; end
  if exist('n_outside','var') == 0; n_outside = 1; end
  if exist('lambda_nm','var') == 0; lambda_nm = 637; end
  
  % Mode LPlm
  if exist('L','var') == 0; L = 0; end
  if exist('M','var') == 0; M = 1; end

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
  v_max = 100;
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
  real_neff_1_vector = n_outside + b*(n_inside-n_outside);
  real_neff_2_vector = sqrt(n_outside^2 + b*(n_inside^2-n_outside^2));

  k0 = 2*pi./lambda_nm; % free space wave number in nm^-1
  kn = k0.*sqrt(n_inside^2-n_outside^2); % nm ^-1
  radius_vector_mum = v./(kn'*1000); % radius_mum (mum) of micropillar microcavity (kn in nm^-1 and v has no unit)
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % Calculate E_meV and lambda_nm for the values of radius_mum (input argument) using simple interpolation
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  %real_neff_1 = interp2(radius_vector_mum,,real_neff_1_vector,XI,YI);
  %yi = interp1(x,Y,xi,method)
  
  real_neff_1 = radius_mum;
  real_neff_2 = radius_mum;
  for i=1:size(radius_mum,1)
    for j=1:size(radius_mum,2)
      r = radius_mum(i,j);
      idx = find(min(abs(radius_vector_mum-r))==abs(radius_vector_mum-r));
      if r<radius_vector_mum(idx)
        if idx-1>0
          real_neff_1(i,j) = interpolate(radius_vector_mum, real_neff_1_vector, idx-1, idx, r);
          real_neff_2(i,j) = interpolate(radius_vector_mum, real_neff_2_vector, idx-1, idx, r);
        else
          real_neff_1(i,j) = real_neff_1_vector(1);
          real_neff_2(i,j) = real_neff_2_vector(1);
        end
      else
        if idx+1 <= length(radius_vector_mum)
          real_neff_1(i,j) = interpolate(radius_vector_mum, real_neff_1_vector, idx, idx+1, r);
          real_neff_2(i,j) = interpolate(radius_vector_mum, real_neff_2_vector, idx, idx+1, r);
        else
          real_neff_1(i,j) = real_neff_1_vector(length(radius_vector_mum));
          real_neff_2(i,j) = real_neff_2_vector(length(radius_vector_mum));
        end
      end
    end
  end

end
