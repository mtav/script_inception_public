function GEOmesh(FILE, delta_X_vector, delta_Y_vector, delta_Z_vector)
  % mesh X
  fprintf(FILE,'XMESH **XMESH DEFINITION\n');
  fprintf(FILE,'{\n');
  for i=1:length(delta_X_vector)
    fprintf(FILE,'%E\n', delta_X_vector(i));
  end
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

  % mesh Y
  fprintf(FILE,'YMESH **YMESH DEFINITION\n');
  fprintf(FILE,'{\n');
  for i=1:length(delta_Y_vector)
    fprintf(FILE,'%E\n', delta_Y_vector(i));
  end
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

  % mesh Z
  fprintf(FILE,'ZMESH **ZMESH DEFINITION\n');
  fprintf(FILE,'{\n');
  for i=1:length(delta_Z_vector)
    fprintf(FILE,'%E\n', delta_Z_vector(i));
  end
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');
end
