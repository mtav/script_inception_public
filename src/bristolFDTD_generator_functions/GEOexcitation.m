function GEOexcitation(FILE, current_source, P1, P2, E, H, source_type, time_constant, amplitude, time_offset, frequency, param1, param2, template_filename, template_source_plane, template_target_plane, template_direction, template_rotation)

  if exist('param1','var')==0; param1 = 0; end;
  if exist('param2','var')==0; param2 = 0; end;
  if exist('template_filename','var')==0; template_filename = 'template.dat'; end;
  if exist('template_source_plane','var')==0; template_source_plane = 'x'; end;
  if exist('template_target_plane','var')==0; template_target_plane = 'x'; end;
  if exist('template_direction','var')==0; template_direction = 0; end;
  if exist('template_rotation','var')==0; template_rotation = 0; end;

  if current_source ~= 11
    [P1, P2] = fixLowerUpper(P1, P2);
    fprintf(FILE,'EXCITATION **name=excitation\n');
    fprintf(FILE,'{\n');
    fprintf(FILE,'%d ** CURRENT SOURCE\n', current_source);
    fprintf(FILE,'%E **X1\n', P1(1));
    fprintf(FILE,'%E **Y1\n', P1(2));
    fprintf(FILE,'%E **Z1\n', P1(3));
    fprintf(FILE,'%E **X2\n', P2(1));
    fprintf(FILE,'%E **Y2\n', P2(2));
    fprintf(FILE,'%E **Z2\n', P2(3));
    fprintf(FILE,'%d **EX\n', E(1));
    fprintf(FILE,'%d **EY\n', E(2));
    fprintf(FILE,'%d **EZ\n', E(3));
    fprintf(FILE,'%d **HX\n', H(1));
    fprintf(FILE,'%d **HY\n', H(2));
    fprintf(FILE,'%d **HZ\n', H(3));
    fprintf(FILE,'%d **GAUSSIAN MODULATED SINUSOID\n', source_type);
    fprintf(FILE,'%E **TIME CONSTANT\n', time_constant);
    fprintf(FILE,'%E **AMPLITUDE\n', amplitude);
    fprintf(FILE,'%E **TIME OFFSET\n', time_offset);
    fprintf(FILE,'%E **FREQUENCY (MHz if dimensions in mum) (c0/f = %E)\n', frequency, get_c0()/frequency);
    fprintf(FILE,'%d **UNUSED PARAMETER\n', param1);
    fprintf(FILE,'%d **UNUSED PARAMETER\n', param2);
    fprintf(FILE,['"',template_filename,'" ** TEMPLATE FILENAME\n']);
    fprintf(FILE,['"',template_source_plane,'" ** TEMPLATE SOURCE PLANE\n']);
    fprintf(FILE,'}\n');
    fprintf(FILE,'\n');
  else
    E = [1,1,1];
    H = [1,1,1];
    [P1, P2] = fixLowerUpper(P1, P2);
    fprintf(FILE,'EXCITATION **name=excitation\n');
    fprintf(FILE,'{\n');
    fprintf(FILE,'%d ** CURRENT SOURCE\n', current_source);
    fprintf(FILE,'%E **X1\n', P1(1));
    fprintf(FILE,'%E **Y1\n', P1(2));
    fprintf(FILE,'%E **Z1\n', P1(3));
    fprintf(FILE,'%E **X2\n', P2(1));
    fprintf(FILE,'%E **Y2\n', P2(2));
    fprintf(FILE,'%E **Z2\n', P2(3));
    fprintf(FILE,'%d **EX\n', E(1));
    fprintf(FILE,'%d **EY\n', E(2));
    fprintf(FILE,'%d **EZ\n', E(3));
    fprintf(FILE,'%d **HX\n', H(1));
    fprintf(FILE,'%d **HY\n', H(2));
    fprintf(FILE,'%d **HZ\n', H(3));
    fprintf(FILE,'%d **GAUSSIAN MODULATED SINUSOID\n', source_type);
    fprintf(FILE,'%E **TIME CONSTANT\n', time_constant);
    fprintf(FILE,'%E **AMPLITUDE\n', amplitude);
    fprintf(FILE,'%E **TIME OFFSET\n', time_offset);
    fprintf(FILE,'%E **FREQUENCY (MHz if dimensions in mum) (c0/f = %E)\n', frequency, get_c0()/frequency);
    fprintf(FILE,'%d **UNUSED PARAMETER\n', param1);
    fprintf(FILE,'%d **UNUSED PARAMETER\n', param2);
    % template specific;
    fprintf(FILE,['"',template_filename,'" ** TEMPLATE FILENAME\n']);
    fprintf(FILE,['"',template_source_plane,'" ** TEMPLATE SOURCE PLANE\n']);
    fprintf(FILE,['"',template_target_plane,'" ** TEMPLATE TARGET PLANE\n']);
    fprintf(FILE,'%d ** DIRECTION 0=-ve 1=+ve\n', template_direction);
    fprintf(FILE,'%d ** ROTATE 0=no, 1=yes\n', template_rotation);
    fprintf(FILE,'}\n');
    fprintf(FILE,'\n');
  end

end
