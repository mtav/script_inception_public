Xini = 3.0;
Xend = 9.0;
Xres = 0.1;
Xposition = Xini:Xres:Xend;

Xangle0a = ( ((Xposition -(Xend+Xini)/2)/Xres) / (length(Xposition)/2) ) * 1.88*10*3;
Xangle0b = ( (Xposition -(Xend+Xini)/2) / ((Xend-Xini)/2) ) * 1.88*10*3;

centro = 6;

Xangle1 = FIS_PositionToAngle(Xposition, centro, 1.88*10, false);
Xangle2 = FIS_PositionToAngle(Xposition, centro, tan(deg2rad(1.88*10*3))/3, true);

Xposition1 = FIS_AngleToPosition(Xangle1, centro, 1.88*10, false);
Xposition2 = FIS_AngleToPosition(Xangle2, centro, tan(deg2rad(1.88*10*3))/3, true);

figure();
xlabel('position (mm)');
ylabel('angle (degrees)');
hold on;

plot(Xposition, Xangle0a, 'o');
plot(Xposition, Xangle0b, 's');

plot(Xposition, Xangle1, 'r--');
plot(Xposition, Xangle2, 'b-');

legend({'basic a', 'basic b', 'linear', 'trigonometric'});

figure();
xlabel('position (mm)');
ylabel('angle (degrees)');
hold on;

plot(Xposition, Xangle1, 'r--');
plot(Xposition, Xangle2, 'b-');

plot(Xposition1, Xangle1, 'ro');
plot(Xposition2, Xangle2, 'bs');

legend({'linear: pos->angle', 'trigonometric: pos->angle', 'linear: angle->pos', 'trigonometric: angle->pos'});
