x = 1:10;
y = 2*x;

probe_data = [x(:), y(:)];

writePrnFile('/tmp/probe.prn', {'x','y'}, probe_data); % probe-style save

[X,Y] = meshgrid(1:3,10:14);
Z = X+Y;

surf(X,Y,Z);

%writePrnFile('/tmp/snapshot.prn', header, data, ux, uy); % snapshot-style save
