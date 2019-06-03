function g_Hz = coupling_strength_2(n, lambda_nm, K1, tau_ns)
    % calculations
    a_nm = 1;
    % lambda_nm = a_nm ./ a_over_lambda;
    lambda_m = 10^-9*lambda_nm;
    tau_s = 10^-9*tau_ns;
    V_m3 = K1*(lambda_m/n)^3;
    % V_m3 = (10^-6)^3*V_mum3;
    V_mum3 = V_m3/((10^-6)^3);
    w_Hz = 2*pi*get_c0()./lambda_m;
    % n = (K1 ./ V_m3).^(1/3) .* lambda_m;
    % (2*get_epsilon0() .* n.^2 .* V_m3)
    % (w_Hz)./(2*get_epsilon0() .* n.^2 .* V_m3)
    % sqrt((w_Hz)./(2*get_epsilon0() .* n.^2 .* V_m3))
    E1ph_SI = sqrt((get_hb()*w_Hz)./(2*get_epsilon0() .* n.^2 .* V_m3));
    % (tau_s .* n .* w_Hz.^3)
    % (3*pi*get_epsilon0()*get_c0()^3*get_hb())
    mu_SI = sqrt((3*pi*get_epsilon0()*get_c0()^3*get_hb())./(tau_s .* n .* w_Hz.^3));
    mu_Debye = mu_SI/(10^-18*1/(10*get_c0())*10^-2);
    % mu_SI = (10^-18*1/(10*get_c0())*10^-2)*mu_Debye;
    g_Hz = mu_SI .* E1ph_SI ./ get_hb();
    g_GHz = 10^-9*g_Hz;
    % (mu_SI.^2 .* n .* w_Hz.^3)
    tau_s = (3*pi*get_epsilon0()*get_c0()^3*get_hb())./(mu_SI.^2 .* n .* w_Hz.^3);
    K1 = V_m3./(lambda_m./n).^3;
    K2 = 2^3*K1;

    % output
    disp(['w(Hz)=', num2str(w_Hz,'%E ')]);
    disp(['n(1)=', num2str(n,'%E ')]);
    disp(['tau(ns)=', num2str(tau_ns,'%E ')]);
    disp(['V(mum^3)=', num2str(V_mum3,'%E ')]);
    disp(['K1(1)=V/(lambda/n)^3=', num2str(K1,'%E ')]);
    disp(['K2(1)=V/(lambda/(2n))^3=', num2str(K2,'%E ')]);
    disp(['lambda(nm)=', num2str(lambda_nm,'%E ')]);
    disp(['a(nm)=', num2str(a_nm,'%E ')]);
    disp(['a/lambda(1)=', num2str(a_nm./lambda_nm,'%E ')]);
    disp(['mu(Debye)=', num2str(mu_Debye,'%E ')]);
    disp(['E1ph(N/coul=V/m)=', num2str(E1ph_SI,'%E ')]);
    disp(['g(Hz)=', num2str(g_Hz,'%E ')]);
    disp(['g(GHz)=', num2str(g_GHz,'%E ')]);
    disp(['(g)/(2*pi)(GHz)=', num2str((g_GHz)/(2*pi),'%E ')]);
    disp(['(2*g)/(2*pi)(GHz)=', num2str((2*g_GHz)/(2*pi),'%E ')]);
end
