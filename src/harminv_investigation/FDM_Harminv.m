function harmonics = FDM_Harminv(input, wmin, wmax, dt, Nmodes)

%-t dt  Specify the sampling interval dt; this determines the units of time used throughout the input and output.  Defaults to 1.0.

%-d d   Specify the spectral "density" d to search for modes, where a density of 1 indicates the usual Fourier resolution.
%That is, the number of basis functions (which sets an upper bound on the number of modes) is given by:
%d *  (freq-max  -  freq-min)* dt * the number of samples in your dataset.
%A maximum of 300 is used, however, to prevent the matrices from getting too big (you can force a larger number with -f, below).
%Note  that the frequency resolution of the outputs is not limited by the spectral density, and can generally be much greater than the Fourier resolution.
%The density determines how many modes, at most, to search for, and in some sense is the density with which the bandwidth is initially "searched" for modes.
%The default density is 0.0, which means that the number of basis functions is determined by -f (which defaults to 100).
%This often corresponds to a much larger density than the usual Fourier resolution, but the resulting singularities in the  system matrices are automatically removed by harminv.

%-f nf  Specify a lower bound nf on the number of spectral basis functions (defaults to 100), setting a lower bound on the number of modes to search for.
%This option is often a more convenient way to specify the number of basis functions than the -d option, above, which is why it is the default.
%-f also allows you to employ more than 300 basis functions, but careful:
%the computation time scales as O(N nf) + O(nf^3), where N is the number of samples, and very large matrices can also have degraded accuracy.

% N is the number of "intervals"
N = length(input)-1;

% the size of the basis J (matrices will be of size JxJ, i.e. max number of modes that can be found is J)
%J = ceil(N*dt*(wmax-wmin)/(4*pi));
J = Nmodes;

phi = linspace(wmin*dt , wmax*dt, J);
z = exp(-I*phi);

disp('FDM run 1');
[harmonics, u] = FDM_Harminv_sub(input, wmin, wmax, dt, Nmodes, z);
disp('FDM run 2');
[harmonics, u] = FDM_Harminv_sub(input, wmin, wmax, dt, Nmodes, u);
disp('FDM run 3');
[harmonics, u] = FDM_Harminv_sub(input, wmin, wmax, dt, Nmodes, u);

return
%hjsdhfjkdhsj

%% maximum M to calculate the U matrices
%M = floor((N-2)/2);

%% Alternative notation: S = U0, U = U1
%U0 = zeros(J,J);
%U1 = zeros(J,J);
%U2 = zeros(J,J);

%for i = 1:J
  %for j = 1:J
    %U0(i, j) = getUelement(M, 0, z(i), z(j), input);
    %U1(i, j) = getUelement(M, 1, z(i), z(j), input);
    %U2(i, j) = getUelement(M, 2, z(i), z(j), input);
  %end
%end

%% solve eigenproblem U1*Bk = uk*U0*Bk
%[v, lambda] = eig(U1, U0);

%u = zeros(J,1); % eigenvalues
%w = zeros(J,1); % radial frequencies
%B = zeros(J,J); % eigenvectors
%err = zeros(J,1); % errors

%for k = 1:J

  %% get scalar eigenvalues
  %u(k) = lambda(k,k);
  
  %% normalize eigenvectors
  %B(:,k) = v(:,k) / sqrt(transpose(v(:,k)) * U0 * v(:,k));
  
  %% calculate error
  %err(k,1) = norm((U2 - u(k)^2*U0)*B(:,k));
%end

%% get the radial frequencies wk from the eigenvalues uk
%w = log(u)/(-I*dt);

%% calculate the amplitudes dk from the eigenvectors Bk and the input ck
%d = zeros(J,1);
%for k = 1:J
  %SUMO = 0;
  %for j = 1:J
    %SUMO += B(j,k) * getUelement(M, 0, z(j), u(k), input);
  %end
  %d(k) = ( (1/(M+1)) * (SUMO) )^2;
%end

%d_approx = zeros(J,1);
%for k = 1:J
  %s2 = 0;
  %for j = 1:J
    %s1 = 0;
    %for n = 0:M
      %s1 += input(n+1)*(z(j))^(-n);
    %end
    %s2 += B(j,k)*s1;
  %end
  %d_approx(k) = s2^2;
%end

%z = u;


%harmonics = sortrows([w, d, d_approx, err], 1);

end
