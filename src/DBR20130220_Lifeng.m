% clear all
layers=15



%for cavity of wavelength=994nm
n(1:2:21)=1.85; %high refrective index
n(2:2:20)=1.45; %low refrective index
% n(5)=1.5; %centre
% n(11)=1.5; %substrate

%d=6000./n/4;
d=1470/4./n; 
% d(11)=1000; %substrate
% d(2:2:10)=1000;

%d(12)=262;
%TE
for j=1:71
theta(1)=asin(sin((j-1)*pi/180)*1/n(1));
D0=[1 1;cos((j-1)*pi/180) -(cos((j-1)*pi/180))]; %TE
Ds=[1 1;cos((j-1)*pi/180) -(cos((j-1)*pi/180))]; %TE
for k=1:1400
    lambda(k)=400+k;
for i=1:layers
phi(i)=2*pi*n(i)*d(i)/lambda(k)*cos(theta(i));
Q{i}=[cos(phi(i)) 1i*sin(phi(i))/(n(i)*cos(theta(i)));1i*(n(i)*cos(theta(i)))*sin(phi(i)) cos(phi(i))];
theta(i+1)=asin(sin(theta(i))*n(i)/n(i+1));
end

t=Q{1};
 for i=2:layers
 t=t*Q{i};
 end
 
T=inv(D0)*t*Ds;
% A{lambda}=T*[1;0];
% a=A{lambda};
% TEtrans(lambda,j)=1/abs(a(1));
TEtrans(lambda(k),j)=1/T(1,1);
TET(lambda(k),j)=(abs(1/T(1,1)))^2*cos(theta(i+1))/cos(theta(1));
TER(lambda(k),j)=(abs(T(2,1)/T(1,1)))^2;

end
end

%TM
for j=1:71
theta(1)=asin(sin((j-1)*pi/180)*1/n(1));
D0=[cos((j-1)*pi/180) (cos((j-1)*pi/180));1 -1]; %TM
Ds=[cos((j-1)*pi/180) (cos((j-1)*pi/180));1 -1]; %TM
for k=1:1400
    lambda(k)=400+k;
for i=1:layers
phi(i)=2*pi*n(i)*d(i)/lambda(k)*cos(theta(i));
Q{i}=[cos(phi(i)) 1i*sin(phi(i))/(n(i))*cos(theta(i));1i*(n(i)/cos(theta(i)))*sin(phi(i)) cos(phi(i))];
theta(i+1)=asin(sin(theta(i))*n(i)/n(i+1));
end

t=Q{1};
 for i=2:layers
 t=t*Q{i};
 end
 
T=inv(D0)*t*Ds;
%A{lambda}=T*[1;0];
%a=A{lambda};
%TMtrans(lambda,j)=1/abs(a(1));
TMtrans(lambda(k),j)=1/T(1,1);
TMT(lambda(k),j)=(abs(1/T(1,1)))^2*cos(theta(i+1))/cos(theta(1));
TMR(lambda(k),j)=(abs(T(2,1)/T(1,1)))^2;
end
end

trans=sqrt((TET.^2+TMT.^2)/2);
refl=(TER+TMR)/2;

x=0:60;
y=1:1700;
figure(5)
imagesc(x,y(900:1700),refl(900:1700,:))
colormap bone
% plot(y(900:1700),refl(900:1700,1))
% figure(5)
% imagesc(x,y(400:1700),TER(400:1700,:))
% colormap bone
% figure(6)
% imagesc(x,y(400:1700),TMR(400:1700,:))
% colormap bone