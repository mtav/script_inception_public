out = fopen(strcat('test.inp'),'wt');

  ITERATIONS = 261600;%no unit
  % ITERATIONS = 32000;%no unit
%	ITERATIONS=10;%no unit
  TIMESTEP=0.9;%mus
  TIME_CONSTANT=4.000000E-09;%mus
  AMPLITUDE=1.000000E+01;%V/mum???
  TIME_OFFSET=2.700000E-08;%mus

  P1 = [ 0,0,0 ];
  P2 = [ 1,1,1 ];
  E = [ 1, 0,	0];
  H = [ 0, 0,	0];
  type = 10;
  GEOexcitation(out, 7, P1, P2, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, 1234, 0, 0, 0, 0);

  
fclose(out);
