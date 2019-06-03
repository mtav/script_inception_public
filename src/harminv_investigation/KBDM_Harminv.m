function harmonics = KBDM_Harminv(input, Nmodes)

dt = 1;

N = length(input);
%M = floor(N/2);
M = Nmodes;

% Alternative notation: S = U0, U = U1
U0 = zeros(M,M);
U1 = zeros(M,M);

for i = 0:M-1
  for j = 0:M-1
    U0(i+1, j+1) = input((0+i+j)+1);
    U1(i+1, j+1) = input((1+i+j)+1);
  end
end

%U0
%U1

% solve eigenproblem U1*Bk = uk*U0*Bk
[v, lambda] = eig(U1, U0);

u = zeros(M,1);
w = zeros(M,1);
B = zeros(M,M);
for k = 1:M
  % get scalar eigenvalues
  u(k) = lambda(k,k);
  % normalize eigenvectors
  B(:,k) = v(:,k) / sqrt(transpose(v(:,k)) * U0 * v(:,k));
end

%lambda
%u

%v
%B

C = (input(:))(1:M);

% calculate the amplitudes dk from the eigenvectors Bk and the input ck
droot = transpose(B)*C;
d = droot.^2;

% get the radial frequencies wk from the eigenvalues uk
%w = -angle(u);
w = log(u)/(-I*dt);

%d
%w

harmonics = sortrows([w, d]);

end
