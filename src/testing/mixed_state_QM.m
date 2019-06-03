% 5th postulate of QM, using mixed states, i.e. density matrices

close all;
clear all;

% 2D

H = [1;0];
V = [0;1];
D = (H + V)/sqrt(2);
A = (H - V)/sqrt(2);
R = (H + I*V)/sqrt(2);
L = (H - I*V)/sqrt(2);

rho0_H = H*H';
rho0_V = V*V';
rho0_D = D*D';
rho0_A = A*A';
rho0_R = R*R';
rho0_L = L*L';

function rho0 = rho0_unpolarized(probability_H)
  H = [1;0];
  V = [0;1];
  rho0 = probability_H * H*H' + (1-probability_H) * V*V';
end

proj_H = H*H';
proj_V = V*V';
proj_D = D*D';
proj_A = A*A';
proj_R = R*R';
proj_L = L*L';

function [state, probability] = result(P, rho0)
  % P must be a projector, i.e. P^n=P and P'=P=P^(-1). rho0 can be anything. (does not have to be normalized)
  probability = trace(rho0*P)/trace(rho0);
  if probability ~= 0
    state = (P*rho0*P')/trace(rho0*P);
  else
    state = (P*rho0*P');
  end
end

disp('======================================================================');
disp('result(proj_H, rho0_H):'); [state, probability] = result(proj_H, rho0_H)
printf('trace(state)=%f\n', trace(state));
disp('result(proj_H, rho0_V):'); [state, probability] = result(proj_H, rho0_V)
printf('trace(state)=%f\n', trace(state));
disp('result(proj_H, rho0_D):'); [state, probability] = result(proj_H, rho0_D)
printf('trace(state)=%f\n', trace(state));
disp('result(proj_H, rho0_A):'); [state, probability] = result(proj_H, rho0_A)
printf('trace(state)=%f\n', trace(state));
disp('result(proj_H, rho0_R):'); [state, probability] = result(proj_H, rho0_R)
printf('trace(state)=%f\n', trace(state));
disp('result(proj_H, rho0_L):'); [state, probability] = result(proj_H, rho0_L)
printf('trace(state)=%f\n', trace(state));

disp('----------------------------------------------------------------------');
for probability_H = 0:0.1:1
  printf('result(proj_H, rho0_unpolarized(%.1f)):\n', probability_H); [state, probability] = result(proj_H, rho0_unpolarized(probability_H))
  printf('trace(state)=%f\n', trace(state));
end
disp('======================================================================');

% 7D, with 3D subspace
b1 = [0,1,0,0,0,0,0]';
b2 = [0,0,0,1,0,0,0]';
b3 = [0,0,0,0,0,1,0]';
P = b1*b1' + b2*b2' + b3*b3'
psi0 = [1,2,3,4,5,6,7]';
rho0 = psi0*psi0'
disp('result(P, rho0):'); [state, probability] = result(P, rho0)
printf('trace(state)=%f\n', trace(state));
disp('======================================================================');

% 7D, with random subspace projector (rho0 could have complex values, but need to make sure it corresponds to diagonal matrix with real values in some basis)
P = diag(randi(2,1,7)-1)
%  rho0 = (2*rand(7,7)-1) + I*(2*rand(7,7)-1)
rho0 = (42*rand(7,7))
disp('result(P, rho0):'); [state, probability] = result(P, rho0)
printf('trace(state)=%f\n', trace(state));

disp('======================================================================');
proba_list = [];
for i = 1:7
  P = zeros(7,7);
  P(i,i) = 1;
  printf('result(P(%d), rho0):\n', i);
  [state, probability] = result(P, rho0)
  printf('trace(state)=%f\n', trace(state));
  proba_list(end+1) = probability;
end

proba_list
sum(proba_list)
% TODO: Could this be used to diagonalize matrices? i.e.:
%  rho0 = some matrix to diagonalize
%  Ndim = size(M,1)
%  proba_list = [];
%  for i in 1:
%    P = zeros(Ndim, Ndim);
%    [state, probability] = result(P, rho0)
%    proba_list(end+1) = probability;
%  end
%  D = trace(rho0)*diag(proba_list)
% Answer: no: Actually, all that does, is take the diagonal of the original matrix... It would have been too easy else. :)
% <P|A|P> would only give eigenvalues of A if P is already a projector transformed using the appropriate eigenbasis change matrix M, i.e. P' = M*P*(M*).
