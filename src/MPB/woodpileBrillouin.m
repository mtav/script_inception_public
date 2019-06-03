close all;

X = [ 1.0;  0.0;  0.0 ];
U = [ 1.0;  0.25;  0.25 ];
L = [ 0.5;  0.5;  0.5 ];
Gamma = [ 0;  0;  0 ];
W = [ 1.0;  0.5;  0.0 ];
K = [ 0.75;  0.75;  0.0 ];
Wpp = [ 1.0;  0.0;  0.5 ];
Xp = [ 0.0;  0.0;  1.0 ];
Kp = [ 0.75;  5.55111512312578e-17;  0.75 ];
Wp = [ 0.5;  -5.55111512312578e-17;  1.0 ];
Up = [ 0.25;  0.25;  1.0 ];

hold on;

text(X(1),X(2),X(3),'X');
text(U(1),U(2),U(3),'U');
text(L(1),L(2),L(3),'L');
text(Gamma(1),Gamma(2),Gamma(3),'Gamma');
text(W(1),W(2),W(3),'W');
text(K(1),K(2),K(3),'K');
text(Wpp(1),Wpp(2),Wpp(3),'Wpp');
text(Xp(1),Xp(2),Xp(3),'Xp');
text(Kp(1),Kp(2),Kp(3),'Kp');
text(Wp(1),Wp(2),Wp(3),'Wp');
text(Up(1),Up(2),Up(3),'Up');

plotVectors([Gamma,X]);
plotVectors([Gamma,U]);
plotVectors([Gamma,L]);
plotVectors([Gamma,W]);
plotVectors([Gamma,K]);

plotVectors([Gamma,Wpp]);
plotVectors([Gamma,Xp]);
plotVectors([Gamma,Kp]);
plotVectors([Gamma,Wp]);
plotVectors([Gamma,Up]);

plotVectors([X,W],[W,K]);
plotVectors([X,U],[U,L]);
plotVectors([K,L]);

plotVectors([X,Wpp],[Wpp,Kp],[Kp,Wp],[Wp,Xp]);
plotVectors([Xp,Up],[Up,L],[L,K]);

plotVectors([Wpp,U],[U,W]);

plotVectors([Wp,Up]);

%Lattice vectors:
a1 = [0; 0.5; 0.5];
a2 = [0.5; 0; 0.5];
a3 = [0.5; 0.5; 0];

%Reciprocal lattice vectors (/ 2 pi):
b1 = [-1; 1; 1];
b2 = [1; -1; 1];
b3 = [1; 1; -1];

basis_matrix = [a1,a2,a3];

basis_matrix = eye(3)

%Geometric objects:
length = 1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% values from (print geometry "\n") output

size = [length;0.2;0.25];
e3 = [0.577350269189626;0.577350269189626;-0.577350269189626];
e2 = [-0.707106781186547;0.707106781186547;0.0];
e1 = [0.0;0.0;1.0];
center = [0;0;0];
projection_matrix = [[0.5; -0.707106781186548; 0.866025403784439], [0.5; 0.707106781186548; 0.866025403784439], [1.0; -0.0; -0.0]];

%plotBlock(size,basis_matrix*center,basis_matrix*e1,basis_matrix*e2,basis_matrix*e3,projection_matrix);

size = [0.2;length;0.25];
e3 = [0.577350269189626;0.577350269189626;-0.577350269189626];
e2 = [-0.707106781186547;0.707106781186547;0.0];
e1 = [0.0;0.0;1.0];
center = [0.25;0.25;0.0];
projection_matrix = [[0.5; -0.707106781186548; 0.866025403784439], [0.5; 0.707106781186548; 0.866025403784439], [1.0; -0.0; -0.0]];

%plotBlock(size,basis_matrix*center,basis_matrix*e1,basis_matrix*e2,basis_matrix*e3,projection_matrix);

e1_geom = e1;
e2_geom = e2;
e3_geom = e3;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% values from (run) output

center = [0;0;0];
size = [length;0.2;0.25];
e1 = [0;0;1.41421];
e2 = [-1.41421;1.41421;0];
e3 = [1;1;-1];

%plotBlock(size,basis_matrix*center,basis_matrix*e1,basis_matrix*e2,basis_matrix*e3,projection_matrix);

center = [0.25;0.25;0];
size = [0.2;length;0.25];
e1 = [0;0;1.41421];
e2 = [-1.41421;1.41421;0];
e3 = [1;1;-1];

%plotBlock(size,basis_matrix*center,basis_matrix*e1,basis_matrix*e2,basis_matrix*e3,projection_matrix);

e1_run = e1;
e2_run = e2;
e3_run = e3;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% direct basis conversion from .ctl input

size = [length;0.2;0.25];
e1 = [0;0;2];
e2 = [-2;2;0];
e3 = [1;1;-1];
center = [0;0;0];
projection_matrix = [[0.5; -0.707106781186548; 0.866025403784439], [0.5; 0.707106781186548; 0.866025403784439], [1.0; -0.0; -0.0]];

plotBlock(size,basis_matrix*center,basis_matrix*e1,basis_matrix*e2,basis_matrix*e3,projection_matrix);

size = [0.2;length;0.25];
e1 = [0;0;2];
e2 = [-2;2;0];
e3 = [1;1;-1];
center = [0.25;0.25;0.0];
projection_matrix = [[0.5; -0.707106781186548; 0.866025403784439], [0.5; 0.707106781186548; 0.866025403784439], [1.0; -0.0; -0.0]];

plotBlock(size,basis_matrix*center,basis_matrix*e1,basis_matrix*e2,basis_matrix*e3,projection_matrix);

e1_input = e1;
e2_input = e2;
e3_input = e3;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
