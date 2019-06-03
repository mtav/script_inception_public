function MEEP_time_snapshot(FILE, first, repetition, plane, P1, P2, E, H, J, power, eps)

  % format specification:
  % 1 iteration number for the first snapshot
  % 2 number of iterations between snapshots
  % 3 plane - 1=x 2=y 3=z
  % 4-9 coordinates of the lower left and top right corners of the plane x1 y1 z1 x2 y2 z2
  % 10-18 field components to be sampled ex ey ez hx hy hz Ix Iy Iz
  % 19 print power? =0/1
  % 20 create EPS snapshot? =0/1
  % 21 write an output file in “list” format
  % 22 write an output file in “matrix” format
  %
  % List format ( as used in version 11 ) which has a filename of the form “x1idaa.prn”, where “x” is the plane over
  % which the snapshot has been taken, “1"is the snapshot serial number. ie. the snaps are numbered in the order which
  % they appear in the input file.. “id” in an identifier specified in the “flags” object. “aa" is the time serial number ie.
  % if snapshots are asked for at every 100 iterations then the first one will have “aa, the second one “ab" etc
  % The file consists of a single header line followed by columns of numbers, one for each field component wanted and
  % two for the coordinates of the point which has been sampled. These files can be read into Gema.
  %
  % Matrix format for each snapshot a file is produced for each requested field component with a name of the form
  % “x1idaa_ex” where the “ex” is the field component being sampled. The rest of the filename is tha same as for the list
  % format case. The file consists of a matrix of numbers the first column and first row or which, gives the position of
  % the sample points in each direction. These files can be read into MathCad or to spreadsheet programs. .

  
  function snapshot(plane,P1,P2)
    if plane == 1
      plane_name='X';
    elseif plane == 2
      plane_name='Y';
    else %plane == 3
      plane_name='Z';
    end

    fprintf(FILE,'SNAPSHOT **SNAPSHOT DEFINITION %s\n',plane_name);
    fprintf(FILE,'{\n');
    fprintf(FILE,'%d **FIRST\n', first);
    fprintf(FILE,'%d **REPETITION\n', repetition);
    fprintf(FILE,'%d **PLANE\n', plane);
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
    fprintf(FILE,'%d **JX\n', J(1));
    fprintf(FILE,'%d **JY\n', J(2));
    fprintf(FILE,'%d **JZ\n', J(3));
    fprintf(FILE,'%d **POW\n', power);
    fprintf(FILE,'%d **EPS\n', eps);
    fprintf(FILE,'}\n');
    fprintf(FILE,'\n');
  end
  
  if P1(plane) == P2(plane)
    snapshot(plane,P1,P2);
  else
    snapshot(1,[P1(1),P1(2),P1(3)],[P1(1),P2(2),P2(3)]);
    snapshot(1,[P2(1),P1(2),P1(3)],[P2(1),P2(2),P2(3)]);
    snapshot(2,[P1(1),P1(2),P1(3)],[P2(1),P1(2),P2(3)]);
    snapshot(2,[P1(1),P2(2),P1(3)],[P2(1),P2(2),P2(3)]);
    snapshot(3,[P1(1),P1(2),P1(3)],[P2(1),P2(2),P1(3)]);
    snapshot(3,[P1(1),P1(2),P2(3)],[P2(1),P2(2),P2(3)]);
  end
  
end
