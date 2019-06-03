function GEOcylinder(FILE, centre, inner_radius, outer_radius, H, permittivity, conductivity, angle_deg)
  % cylinder
  % {
  % 1-7 Coordinates of the material volume ( xc yc zc r1 r2 h )
  % 7 permittivity
  % 8 conductivity
  % 9 angle_deg of inclination
  % }
  % xc, yc and zc are the coordinates of the centre of the cylinder. r1 and r2 are the inner and outer
  % radius respectively, h is the cylinder height, is the angle_deg of inclination. The cylinder is aligned
  % with the y direction if =0 and with the x direction if =90
    %
    % i.e. angle_deg = Angle of rotation in degrees around -Z=(0,0,-1)

  fprintf(FILE,'CYLINDER **Cylinder Definition\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **X CENTRE\n', centre(1));
  fprintf(FILE,'%E **Y CENTRE\n', centre(2));
  fprintf(FILE,'%E **Z CENTRE\n', centre(3));
  fprintf(FILE,'%E **inner_radius\n', inner_radius);
  fprintf(FILE,'%E **outer_radius\n', outer_radius);
  fprintf(FILE,'%E **HEIGHT\n', H);
  fprintf(FILE,'%E **Permittivity\n', permittivity);
  fprintf(FILE,'%E **Conductivity\n', conductivity);
  fprintf(FILE,'%E **Angle of rotation in degrees around -Z=(0,0,-1)\n', angle_deg);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');
end
