function GEOboundary(FILE, Xpos_bc, Xpos_param,...
                            Ypos_bc, Ypos_param,...
                            Zpos_bc, Zpos_param,...
                            Xneg_bc, Xneg_param,...
                            Yneg_bc, Yneg_param,...
                            Zneg_bc, Zneg_param)
  fprintf(FILE,'BOUNDARY  **name=boundaries\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%d %E %E %E **X+\n', Xpos_bc, Xpos_param(1), Xpos_param(2), Xpos_param(3));
  fprintf(FILE,'%d %E %E %E **Y+\n', Ypos_bc, Ypos_param(1), Ypos_param(2), Ypos_param(3));
  fprintf(FILE,'%d %E %E %E **Z+\n', Zpos_bc, Zpos_param(1), Zpos_param(2), Zpos_param(3));
  fprintf(FILE,'%d %E %E %E **X-\n', Xneg_bc, Xneg_param(1), Xneg_param(2), Xneg_param(3));
  fprintf(FILE,'%d %E %E %E **Y-\n', Yneg_bc, Yneg_param(1), Yneg_param(2), Yneg_param(3));
  fprintf(FILE,'%d %E %E %E **Z-\n', Zneg_bc, Zneg_param(1), Zneg_param(2), Zneg_param(3));
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');
end
