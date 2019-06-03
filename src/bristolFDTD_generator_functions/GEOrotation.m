function GEOrotation(FILE, axis_point, axis_direction, angle_degrees)
  % rotation structure. Actually affects previous geometry object in Prof. Railton's modified BrisFDTD. Not fully implemented yet.
    % Should be integrated into existing structures using a directional vector anyway, like in MEEP. BrisFDTD hacking required... :)

  fprintf(FILE,'ROTATION **Rotation Definition, affects previous geometry object\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **X axis_point\n', axis_point(1));
  fprintf(FILE,'%E **Y axis_point\n', axis_point(2));
  fprintf(FILE,'%E **Z axis_point\n', axis_point(3));
  fprintf(FILE,'%E **X axis_direction\n', axis_direction(1));
  fprintf(FILE,'%E **Y axis_direction\n', axis_direction(2));
  fprintf(FILE,'%E **Z axis_direction\n', axis_direction(3));
  fprintf(FILE,'%E **angle_degrees\n', angle_degrees);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');
end
