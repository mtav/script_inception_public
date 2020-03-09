angle_deg = [0,20,40,60,90];
mid_angles = (angle_deg(2:end)+angle_deg(1:end-1))/2;

% lumerical:
n1=1.5
n2=2.5

d1=2.5
d2=2.5

plot_custom(n1, n2, d1, d2);
for t = mid_angles
  n2 = n1*tan(deg2rad(t));
  plot_custom(n1, n2, d1, d2);
end

% saleh&teich:
n1 = 1.5;
n2 = 3.5;

d1 = 0.5;
d2 = 0.5;

plot_custom(n1, n2, d1, d2);
for t = mid_angles
  n2 = n1*tan(deg2rad(t));
  plot_custom(n1, n2, d1, d2);
end
