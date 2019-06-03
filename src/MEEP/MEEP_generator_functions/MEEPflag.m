function MEEP_flag(FILE, iteration_method, propagation_constant, flag_1, flag_2, iterations, timestep, id_character)
  fprintf(FILE,'FLAG  **PROGRAM CONTROL OPTIONS\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%d **ITERATION METHOD\n', iteration_method);
  fprintf(FILE,'%d **PROPAGATION CONSTANT (IGNORED IN 3D MODEL)\n', propagation_constant);
  fprintf(FILE,'%d **FLAG ONE\n', flag_1);
  fprintf(FILE,'%d **FLAG TWO\n', flag_2);
  fprintf(FILE,'%d **ITERATIONS\n', iterations);
  fprintf(FILE,'%E **TIMESTEP\n', timestep);
  fprintf(FILE,'"%s" **ID CHARACTER (ALWAYS USE QUOTES)\n', id_character);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');
end
