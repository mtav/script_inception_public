function GEOsphere(FILE, center, outer_radius, inner_radius, permittivity, conductivity)
  % sphere
  % {
  % 1-5 Coordinates of the sphere ( xc yc zc r1 r2 )
  % 6 permittivity
  % 7 conductivity
  % }
  fprintf(FILE,'SPHERE  **SPHERE DEFINITION\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **XC\n', center(1));
  fprintf(FILE,'%E **YC\n', center(2));
  fprintf(FILE,'%E **ZC\n', center(3));
  fprintf(FILE,'%E **outer_radius\n', outer_radius);
  fprintf(FILE,'%E **inner_radius\n', inner_radius);
  fprintf(FILE,'%E **permittivity\n', permittivity);
  fprintf(FILE,'%E **conductivity\n', conductivity);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');
end
