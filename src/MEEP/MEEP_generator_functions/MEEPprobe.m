function MEEP_probe(FILE, position, step, E, H, J, power )
  fprintf(FILE,'PROBE **PROBE DEFINITION\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **X\n', position(1));
  fprintf(FILE,'%E **Y\n', position(2));
  fprintf(FILE,'%E **Z\n', position(3));
  fprintf(FILE,'%d **STEP\n', step);
  fprintf(FILE,'%d **EX\n', E(1));
  fprintf(FILE,'%d **EY\n', E(2));
  fprintf(FILE,'%d **EZ\n', E(3));
  fprintf(FILE,'%d **HX\n', H(1));
  fprintf(FILE,'%d **HY\n', H(2));
  fprintf(FILE,'%d **HZ\n', H(3));
  fprintf(FILE,'%d **JX\n', J(1));
  fprintf(FILE,'%d **JY\n', J(2));
  fprintf(FILE,'%d **JZ\n', J(3));
  fprintf(FILE,'%d **POW\n', power);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');
end
