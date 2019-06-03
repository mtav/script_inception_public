function neff = get_neff(n_cavity,n_mirror)
  % based on formula 3.12, page 63 in Daniel Ho's PhD:
  % reference 241: 
  % Spontaneous emission factor of a microcavity DBR surface-emitting laser
  % Spontaneous_Emission_Factor_of_a_Microcavity_DBR_Surface-Emitting_Laser.pdf
  
  %Baba, T.;   Hamano, T.;   Koyama, F.;   Iga, K.;  
  %Precision & Intelligence Lab., Tokyo Inst. of Technol., Yokohama 
  
  %This paper appears in: Quantum Electronics, IEEE Journal of
  %Issue Date: Jun 1991
  %Volume: 27 Issue:6
  %On page(s): 1347 - 1358
  %ISSN: 0018-9197
  %References Cited: 33
  %INSPEC Accession Number: 4026539
  %Digital Object Identifier: 10.1109/3.89951 
  %Date of Current Version: 06 August 2002
  %Sponsored by: IEEE Photonics Society  

  % TODO: Calculate n_eff based on real definition, i.e. n_eff^2 = int(n(z)^2*U*dz,z,-inf,+inf)/int(U*dz,z,-inf,+inf)
  % U = power distribution
  
  neff = sqrt(2*n_cavity^4/(3*n_cavity^2-n_mirror^2)); % average refractive index
end
