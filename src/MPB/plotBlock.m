function plotBlock(size,center,e1,e2,e3,projection_matrix)

%    Appp = projection_matrix*(center + size(1)*e1 + size(2)*e2 + size(3)*e3);
%    Appm = projection_matrix*(center + size(1)*e1 + size(2)*e2 - size(3)*e3);
%    Apmp = projection_matrix*(center + size(1)*e1 - size(2)*e2 + size(3)*e3);
%    Apmm = projection_matrix*(center + size(1)*e1 - size(2)*e2 - size(3)*e3);
%    Ampp = projection_matrix*(center - size(1)*e1 + size(2)*e2 + size(3)*e3);
%    Ampm = projection_matrix*(center - size(1)*e1 + size(2)*e2 - size(3)*e3);
%    Ammp = projection_matrix*(center - size(1)*e1 - size(2)*e2 + size(3)*e3);
%    Ammm = projection_matrix*(center - size(1)*e1 - size(2)*e2 - size(3)*e3);

%    Appp = center + projection_matrix*(+ size(1)*e1 + size(2)*e2 + size(3)*e3);
%    Appm = center + projection_matrix*(+ size(1)*e1 + size(2)*e2 - size(3)*e3);
%    Apmp = center + projection_matrix*(+ size(1)*e1 - size(2)*e2 + size(3)*e3);
%    Apmm = center + projection_matrix*(+ size(1)*e1 - size(2)*e2 - size(3)*e3);
%    Ampp = center + projection_matrix*(- size(1)*e1 + size(2)*e2 + size(3)*e3);
%    Ampm = center + projection_matrix*(- size(1)*e1 + size(2)*e2 - size(3)*e3);
%    Ammp = center + projection_matrix*(- size(1)*e1 - size(2)*e2 + size(3)*e3);
%    Ammm = center + projection_matrix*(- size(1)*e1 - size(2)*e2 - size(3)*e3);

%    e1 = projection_matrix*e1;
%    e2 = projection_matrix*e2;
%    e3 = projection_matrix*e3;

  basis_size = [sqrt(0.5); sqrt(0.5); sqrt(0.5)];
  basis1 = [0; 1; 1];
  basis2 = [1; 0; 1];
  basis3 = [1; 1; 0];

  basis_matrix = [basis1,basis2,basis3]^(-1);

  e1 = basis_matrix*e1;
  e2 = basis_matrix*e2;
  e3 = basis_matrix*e3;
  center = basis_matrix*center;

  Appp = (center + size(1)*e1 + size(2)*e2 + size(3)*e3);
  Appm = (center + size(1)*e1 + size(2)*e2 - size(3)*e3);
  Apmp = (center + size(1)*e1 - size(2)*e2 + size(3)*e3);
  Apmm = (center + size(1)*e1 - size(2)*e2 - size(3)*e3);
  Ampp = (center - size(1)*e1 + size(2)*e2 + size(3)*e3);
  Ampm = (center - size(1)*e1 + size(2)*e2 - size(3)*e3);
  Ammp = (center - size(1)*e1 - size(2)*e2 + size(3)*e3);
  Ammm = (center - size(1)*e1 - size(2)*e2 - size(3)*e3);

  hold on;

  plotVectors([Ampp,Appp]);
  plotVectors([Ampm,Appm]);
  plotVectors([Ammp,Apmp]);
  plotVectors([Ammm,Apmm]);

  plotVectors([Apmp,Appp]);
  plotVectors([Apmm,Appm]);
  plotVectors([Ammp,Ampp]);
  plotVectors([Ammm,Ampm]);

  plotVectors([Appm,Appp]);
  plotVectors([Apmm,Apmp]);
  plotVectors([Ampm,Ampp]);
  plotVectors([Ammm,Ammp]);
end
