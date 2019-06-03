function [harmonics, u] = FDM_Harminv_sub(input, wmin, wmax, dt, Nmodes, z)

J = length(z);

% N is the number of "intervals"
N = length(input)-1;

% maximum M to calculate the U matrices
M = floor((N-2)/2);

% Alternative notation: S = U0, U = U1
U0 = zeros(J,J);
U1 = zeros(J,J);
U2 = zeros(J,J);

for i = 1:J
  for j = 1:J
    U0(i, j) = getUelement(M, 0, z(i), z(j), input);
    U1(i, j) = getUelement(M, 1, z(i), z(j), input);
    U2(i, j) = getUelement(M, 2, z(i), z(j), input);
  end
end

%disp('U matrices ready');

%U0
%U1

% solve eigenproblem U1*Bk = uk*U0*Bk
[v, lambda] = eig(U1, U0);


u = zeros(J,1); % eigenvalues
w = zeros(J,1); % radial frequencies
B = zeros(J,J); % eigenvectors
err = zeros(J,1); % errors

%disp('sizes')
%size(U0)
%size(U1)
%size(U2)
%size(v)
%size(lambda)

%disp('new sizes')
%size(u)
%size(w)
%size(B)


for k = 1:J

  % get scalar eigenvalues
  u(k) = lambda(k,k);
  
  % normalize eigenvectors
  %size(v(:,k))
  %sqrt(transpose(v(:,k)) * U0 * v(:,k))
  %v(:,k) / sqrt(transpose(v(:,k)) * U0 * v(:,k))
  %size(B(:,k))
  B(:,k) = v(:,k) / sqrt(transpose(v(:,k)) * U0 * v(:,k));
  
  % calculate error
  err(k,1) = norm((U2 - u(k)^2*U0)*B(:,k));
end

%disp('u and B calculated');

%for k = 1:M
  %%size((U2 - u(k)^2*U0)*B(:,k))
  %%size(err)
  %%(U2 - u(k)^2*U0)*B(:,k)
%end

% get the radial frequencies wk from the eigenvalues uk
%w = -angle(u);
w = log(u)/(-I*dt);

%B

% calculate the amplitudes dk from the eigenvectors Bk and the input ck
d = zeros(J,1);
for k = 1:J
  SUMO = 0;
  for j = 1:J
    SUMO += B(j,k) * getUelement(M, 0, z(j), u(k), input);
  end
  d(k) = ( (1/(M+1)) * (SUMO) )^2;
end

d_approx = zeros(J,1);
for k = 1:J
  s2 = 0;
  for j = 1:J
    s1 = 0;
    for n = 0:M
      s1 += input(n+1)*(z(j))^(-n);
    end
    s2 += B(j,k)*s1;
  end
  d_approx(k) = s2^2;
end

%w
%err
%d
%d_approx

harmonics = sortrows([w, d, d_approx, err], 1);

end
