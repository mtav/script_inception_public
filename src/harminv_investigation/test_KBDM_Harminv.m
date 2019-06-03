close all;
clear all;

%  u0 = exp(-3*i);
%  u1 = exp(-4*i);
%  u2 = exp(-5*i);

%  uu-u0*ss
%  uu-u1*ss
%  uu-u2*ss

%  d0 = 6;
%  d1 = 7;
%  d2 = 8;

%  FunkyFunction = @(t) myfunc(t)
%  FunkyFunction = @(t) myfunc2(t,1,2,3,0.4,0.5,0.6)

d0 = rand()
d1 = rand()
d2 = rand()

w0 = rand()
w1 = rand()
w2 = rand()

%d0 = 6;
%d1 = 7;
%d2 = 8;

%w0 = 3;
%w1 = 4;
%w2 = 5;

input_values = [[d0, -angle(exp(-w0*i))];
[d1, -angle(exp(-w1*i))];
[d2, -angle(exp(-w2*i))]];
input_values = sortrows(input_values);

FunkyFunction = @(t) myfunc2(t, d0, d1, d2, w0, w1, w2);

c0 = FunkyFunction(0);
c1 = FunkyFunction(1);
c2 = FunkyFunction(2);
c3 = FunkyFunction(3);
c4 = FunkyFunction(4);
c5 = FunkyFunction(5);

%  bb0 = sqrt(d0)*[conj(c0);conj(c1);conj(c2)]/(c0*conj(c0)+c1*conj(c1)+c2*conj(c2))
%  bb1 = sqrt(d1)*[conj(c0);conj(c1);conj(c2)]/(c0*conj(c0)+c1*conj(c1)+c2*conj(c2))
%  bb2 = sqrt(d2)*[conj(c0);conj(c1);conj(c2)]/(c0*conj(c0)+c1*conj(c1)+c2*conj(c2))


%  [bb0,bb1,bb2]
%  droot = transpose([bb0,bb1,bb2])*[c0;c1;c2]
%  
%  droot.^2
%  droot.^2 - [d0;d1;d2]

%  (uu-u0*ss)*bb0
%  (uu-u1*ss)*bb1
%  (uu-u2*ss)*bb2

% U0
S = [[FunkyFunction(0), FunkyFunction(1), FunkyFunction(2)];...
      [FunkyFunction(1), FunkyFunction(2), FunkyFunction(3)];...
      [FunkyFunction(2), FunkyFunction(3), FunkyFunction(4)]];

% U1
U = [[FunkyFunction(1), FunkyFunction(2), FunkyFunction(3)];...
      [FunkyFunction(2), FunkyFunction(3), FunkyFunction(4)];...
      [FunkyFunction(3), FunkyFunction(4), FunkyFunction(5)]];

% solve eigenproblem
[v, lambda] = eig(U, S);

% eigenvalues
u0 = lambda(1,1);
u1 = lambda(2,2);
u2 = lambda(3,3);

% eigenvectors
bb0 = v(:,1);
bb1 = v(:,2);
bb2 = v(:,3);

% normalize eigenvectors
bb0 = bb0 / sqrt(transpose(bb0) * S * bb0);
bb1 = bb1 / sqrt(transpose(bb1) * S * bb1);
bb2 = bb2 / sqrt(transpose(bb2) * S * bb2);

%disp('normalization check (should all be one)')
%transpose(bb0) * S * bb0
%transpose(bb1) * S * bb1
%transpose(bb2) * S * bb2

%bb0 = bb0/norm(bb0);
%bb1 = bb1/norm(bb1);
%bb2 = bb2/norm(bb2);

%% check that the solutions solve the generalized eigenvalue problem:
%disp('Check that the eigenvalue/vector pairs solve the eigenproblem (should be all zero vectors of size 3)')
%(uu-u0*ss)*bb0
%(uu-u1*ss)*bb1
%(uu-u2*ss)*bb2

%  droot = transpose([bb0,bb1,bb2])*[c0;c1;c2]
%  
%  droot.^2
%  droot.^2 - [d0;d1;d2]

% manual solving:
%c(n) = d0*exp(-i*w0*n*t) + d1*exp(-i*w1*n*t) + d2*exp(-i*w2*n*t)
     %= d0*u0^n           + d1*u1^n           + d2*u2^n

%M * [d0;d1;d2] = [c0;c1;c2]

%%M = [[u0^0, u1^0, u2^0];...
     %%[u0^1, u1^1, u2^1];...
     %%[u0^2, u1^2, u2^2]];

%dvalues = (M^-1)*[c0;c1;c2];

%disp('Calculated sqrt(amplitudes):');

droot0 = bb0(1)*c0 + bb0(2)*c1 + bb0(3)*c2;
droot1 = bb1(1)*c0 + bb1(2)*c1 + bb1(3)*c2;
droot2 = bb2(1)*c0 + bb2(2)*c1 + bb2(3)*c2;

d0_calc = droot0^2;
d1_calc = droot1^2;
d2_calc = droot2^2;

w0_calc = -angle(u0);
w1_calc = -angle(u1);
w2_calc = -angle(u2);

output_values = [[d0_calc, w0_calc];
[d1_calc, w1_calc];
[d2_calc, w2_calc]];
output_values = sortrows(output_values);

disp('Input (d,w) pairs:');
input_values

disp('Output (d,w) pairs:');
output_values

disp('output_values - input_values');
output_values - input_values

%disp('Calculated amplitudes:');

%%dvalues
%%d0_ret = dvalues(1)
%%d1_ret = dvalues(2)
%%d2_ret = dvalues(3)

%%d0_ret_orig = dvalues(1);
%%d1_ret_orig = dvalues(2);
%%d2_ret_orig = dvalues(3);

%%(norm(bb0(1)*c0 + bb0(2)*c1 + bb0(3)*c2)^2)
%%(norm(bb1(1)*c0 + bb1(2)*c1 + bb1(3)*c2)^2)
%%(norm(bb2(1)*c0 + bb2(2)*c1 + bb2(3)*c2)^2)

%%(norm(bb0(1)*c0 + bb0(2)*c1 + bb0(3)*c2)^2)/d0_ret_orig
%%(norm(bb1(1)*c0 + bb1(2)*c1 + bb1(3)*c2)^2)/d1_ret_orig
%%(norm(bb2(1)*c0 + bb2(2)*c1 + bb2(3)*c2)^2)/d2_ret_orig

%disp('Calculated radial frequencies:');
%w0_ret = -angle(u0)
%w1_ret = -angle(u1)
%w2_ret = -angle(u2)

%disp('Input amplitudes:');
%d0
%d1
%d2

%%disp('sqrt(Input amplitudes):');
%%sqrt(d0)
%%sqrt(d1)
%%sqrt(d2)
  
%disp('Input radial frequencies:');
%-angle(exp(-w0*i))
%-angle(exp(-w1*i))
%-angle(exp(-w2*i))

%%for t = 0:5
  %%myfunc2(t, d0_ret, d1_ret, d2_ret, w0_ret, w1_ret, w2_ret) - myfunc2(t, d0, d1, d2, w0, w1, w2)
%%end
%%%%%%%%

%%droot = [bb0,bb1,bb2]*[c0;c1;c2]
%%lol = droot.*droot
%%d0_ret = lol(1)
%%d1_ret = lol(2)
%%d2_ret = lol(3)
%%for t = 0:5
  %%myfunc2(t, d0_ret, d1_ret, d2_ret, w0_ret, w1_ret, w2_ret) - myfunc2(t, d0, d1, d2, w0, w1, w2)
%%end
%%%%%%%%

%%lol = droot.*conj(droot)
%%d0_ret = lol(1)
%%d1_ret = lol(2)
%%d2_ret = lol(3)
%%for t = 0:5
  %%myfunc2(t, d0_ret, d1_ret, d2_ret, w0_ret, w1_ret, w2_ret) - myfunc2(t, d0, d1, d2, w0, w1, w2)
%%end
%%%%%%%%

%%droot = transpose([bb0,bb1,bb2])*[c0;c1;c2]
%%lol = droot.*droot
%%d0_ret = lol(1)
%%d1_ret = lol(2)
%%d2_ret = lol(3)
%%for t = 0:5
  %%myfunc2(t, d0_ret, d1_ret, d2_ret, w0_ret, w1_ret, w2_ret) - myfunc2(t, d0, d1, d2, w0, w1, w2)
%%end
%%%%%%%%

%%lol = droot.*conj(droot)
%%d0_ret = lol(1)
%%d1_ret = lol(2)
%%d2_ret = lol(3)
%%for t = 0:5
  %%myfunc2(t, d0_ret, d1_ret, d2_ret, w0_ret, w1_ret, w2_ret) - myfunc2(t, d0, d1, d2, w0, w1, w2)
%%end
%%%%%%%%

%%droot = ctranspose([bb0,bb1,bb2])*[c0;c1;c2]
%%lol = droot.*droot
%%d0_ret = lol(1)
%%d1_ret = lol(2)
%%d2_ret = lol(3)
%%for t = 0:5
  %%myfunc2(t, d0_ret, d1_ret, d2_ret, w0_ret, w1_ret, w2_ret) - myfunc2(t, d0, d1, d2, w0, w1, w2)
%%end
%%%%%%%%

%%lol = droot.*conj(droot)
%%d0_ret = lol(1)
%%d1_ret = lol(2)
%%d2_ret = lol(3)
%%for t = 0:5
  %%myfunc2(t, d0_ret, d1_ret, d2_ret, w0_ret, w1_ret, w2_ret) - myfunc2(t, d0, d1, d2, w0, w1, w2)
%%end
%%%%%%%%

%%%  droot.^2 - [d0;d1;d2]
