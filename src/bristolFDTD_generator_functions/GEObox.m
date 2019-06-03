function GEObox(FILE, lower, upper)
  fprintf(FILE,'BOX  **BOX DEFINITION\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **XL\n', lower(1));
  fprintf(FILE,'%E **YL\n', lower(2));
  fprintf(FILE,'%E **ZL\n', lower(3));
  fprintf(FILE,'%E **XU\n', upper(1));
  fprintf(FILE,'%E **YU\n', upper(2));
  fprintf(FILE,'%E **ZU\n', upper(3));
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');
end
