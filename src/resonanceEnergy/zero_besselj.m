function output = zero_besselj(l)
  % fonction zero_besselj.m
  % returns the unique real positive roots of the Bessel function J_l(x) sorted in ascending order

  n_termes = 100;

  l = abs(l);

  coeff = zeros(n_termes-1, 1);

  if l==0,
    s = (2:2:n_termes-1);
    coeff_0 = 1.0;
  else
    s = (l:2:n_termes-1);
    coeff_0 = 0.0; 
  end
   
  % Bessel J 
  coeff(s) = (-1).^((s-l)/2)./(2.^s .* gamma((s-l)/2 +1) .* gamma((s+l)/2 +1));

  polycoeffs = fliplr([coeff_0 coeff']);
  
  %x = [0:0.1:40]
  %plot(x,polyval(polycoeffs,x))
  %hold on; line([0,40],[0,0])
  
  racines = roots(polycoeffs);
  racines_reelles_positives = sort(racines(find(imag(racines)==0 & real(racines)>=0)));
  
  ecart = diff(racines_reelles_positives);
  racines_uniques = racines_reelles_positives(find(ecart~=0));
  
  output = racines_uniques;
end
