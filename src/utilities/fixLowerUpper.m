function [real_L, real_U] = fixLowerUpper(L,U)
  real_L = [0,0,0];
  real_U = [0,0,0];
  for i=[1:3]
    real_L(i) = min(L(i),U(i));
    real_U(i) = max(L(i),U(i));
  end
end
