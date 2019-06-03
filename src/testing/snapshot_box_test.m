out = fopen(strcat('test.inp'),'wt');

% frequency snapshots
first = 1;
repetition = 1;
interpolate = 1;
real_dft = 0;
mod_only = 0;
mod_all = 1;
starting_sample = 0;
E=[1,1,1];
H=[1,1,1];
J=[0,0,0];
power = 0;
FREQUENCY=9001;

plane = 1;
P1 = [0,0,0];
P2 = [1,1,1];

GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, FREQUENCY, starting_sample, E, H, J);
GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);

fclose(out);

out = fopen(strcat('test.geo'),'wt');
GEObox(out, 2*P1, 2*P2);
fclose(out);
