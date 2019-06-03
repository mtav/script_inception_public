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

length = 1;

size = [length;0.2;0.25];
e3 = [0.577350269189626;0.577350269189626;-0.577350269189626];
e2 = [-0.707106781186547;0.707106781186547;0.0];
e1 = [0.0;0.0;1.0];
center = [0;0;0];
projection_matrix = [[0.5; -0.707106781186548; 0.866025403784439], [0.5; 0.707106781186548; 0.866025403784439], [1.0; -0.0; -0.0]];

plotBlock(size,center,e1,e2,e3,projection_matrix);

size = [0.2;length;0.25];
e3 = [0.577350269189626;0.577350269189626;-0.577350269189626];
e2 = [-0.707106781186547;0.707106781186547;0.0];
e1 = [0.0;0.0;1.0];
center = [0.25;0.25;0.0];
projection_matrix = [[0.5; -0.707106781186548; 0.866025403784439], [0.5; 0.707106781186548; 0.866025403784439], [1.0; -0.0; -0.0]];

plotBlock(size,center,e1,e2,e3,projection_matrix);
