clear all
clc
wqd=1378
wc = 1323
Gamma= 74*10^(-3)
Ktot = 182*10^(-3)
g = 81*10^(-3)
x=-0.2:0.01:0.2;
subplot(2,2,1)
plot(x,abs(reflection(x, wc, wqd, Gamma, Ktot, 3, g)))
subplot(2,2,2)
plot(x,angle(reflection(x, wc, wqd, Gamma, Ktot, 3, g)))
subplot(2,2,3)
plot(x,abs(reflection(x, wc, wc, Gamma, Ktot, 3, g)))
subplot(2,2,4)
plot(x,angle(reflection(x, wc, wc, Gamma, Ktot, 3, g)))
reflection(0, wc, wc, 74*10^(-3), Ktot, 1/5, 81*10^(-3))
reflection(0, 1323, 1323, 74*10^(-3), .1820, 1/5, 81*10^(-3))
