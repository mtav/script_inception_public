function GEOfrequency_snapshot(FILE, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency, starting_sample, E, H, J)
  %disp('writing freq snapshot')
  other_args = struct('FILE', FILE,...
            'first', first,...
            'repetition', repetition,...
            'interpolate', interpolate,...
            'real_dft', real_dft,...
            'mod_only', mod_only,...
            'mod_all', mod_all,...
            'starting_sample', starting_sample,...
            'E', E,...
            'H', H,...
            'J', J);
  %disp('STRUCTURE READY')
  %other_args.first
  for i = 1:length(frequency)
    if P1(plane) == P2(plane)
      snapshot(other_args,plane,P1,P2,frequency(i));
    else
      snapshot(other_args,1,[P1(1),P1(2),P1(3)],[P1(1),P2(2),P2(3)],frequency(i));
      snapshot(other_args,1,[P2(1),P1(2),P1(3)],[P2(1),P2(2),P2(3)],frequency(i));
      snapshot(other_args,2,[P1(1),P1(2),P1(3)],[P2(1),P1(2),P2(3)],frequency(i));
      snapshot(other_args,2,[P1(1),P2(2),P1(3)],[P2(1),P2(2),P2(3)],frequency(i));
      snapshot(other_args,3,[P1(1),P1(2),P1(3)],[P2(1),P2(2),P1(3)],frequency(i));
      snapshot(other_args,3,[P1(1),P1(2),P2(3)],[P2(1),P2(2),P2(3)],frequency(i));
    end
  end
  %disp('writing freq snapshot DONE')
  %disp('FREQUENCY SNAPSHOT DONE')
end

function snapshot(other_args,plane,P1,P2, frequency)
  %disp('INSIDE')
  %other_args.first
  
  if plane == 1
    plane_name='X';
  elseif plane == 2
    plane_name='Y';
  else %plane == 3
    plane_name='Z';
  end
  fprintf(other_args.FILE,'FREQUENCY_SNAPSHOT **SNAPSHOT DEFINITION %s\n',plane_name);
  fprintf(other_args.FILE,'{\n');
  fprintf(other_args.FILE,'%d **FIRST\n', other_args.first);
  fprintf(other_args.FILE,'%d **REPETITION\n', other_args.repetition);
  fprintf(other_args.FILE,'%d **interpolate?\n', other_args.interpolate);
  fprintf(other_args.FILE,'%d **REAL DFT\n', other_args.real_dft);
  fprintf(other_args.FILE,'%d **MOD ONLY\n', other_args.mod_only);
  fprintf(other_args.FILE,'%d **MOD ALL\n', other_args.mod_all);
  fprintf(other_args.FILE,'%d **PLANE\n', plane);
  fprintf(other_args.FILE,'%E **X1\n', P1(1));
  fprintf(other_args.FILE,'%E **Y1\n', P1(2));
  fprintf(other_args.FILE,'%E **Z1\n', P1(3));
  fprintf(other_args.FILE,'%E **X2\n', P2(1));
  fprintf(other_args.FILE,'%E **Y2\n', P2(2));
  fprintf(other_args.FILE,'%E **Z2\n', P2(3));
  fprintf(other_args.FILE,'%E **FREQUENCY (MHz)\n', frequency);
  fprintf(other_args.FILE,'%d **STARTING SAMPLE\n', other_args.starting_sample);
  fprintf(other_args.FILE,'%d **EX\n', other_args.E(1));
  fprintf(other_args.FILE,'%d **EY\n', other_args.E(2));
  fprintf(other_args.FILE,'%d **EZ\n', other_args.E(3));
  fprintf(other_args.FILE,'%d **HX\n', other_args.H(1));
  fprintf(other_args.FILE,'%d **HY\n', other_args.H(2));
  fprintf(other_args.FILE,'%d **HZ\n', other_args.H(3));
  fprintf(other_args.FILE,'%d **JX\n', other_args.J(1));
  fprintf(other_args.FILE,'%d **JY\n', other_args.J(2));
  fprintf(other_args.FILE,'%d **JZ\n', other_args.J(3));
  fprintf(other_args.FILE,'}\n');
  fprintf(other_args.FILE,'\n');
end
