[xa_new_header, xa_new_data, xa_outfile, xa_total] = createPoyntingSnapshot('xa_id_00.prn', true);
[xb_new_header, xb_new_data, xb_outfile, xb_total] = createPoyntingSnapshot('xb_id_00.prn', true);
[yc_new_header, yc_new_data, yc_outfile, yc_total] = createPoyntingSnapshot('yc_id_00.prn', true);
[yd_new_header, yd_new_data, yd_outfile, yd_total] = createPoyntingSnapshot('yd_id_00.prn', true);
[ze_new_header, ze_new_data, ze_outfile, ze_total] = createPoyntingSnapshot('ze_id_00.prn', true);
[zf_new_header, zf_new_data, zf_outfile, zf_total] = createPoyntingSnapshot('zf_id_00.prn', true);

xa_total.Sx
xb_total.Sx
yc_total.Sy
yd_total.Sy
ze_total.Sz
zf_total.Sz

xa_total.Smod
xb_total.Smod
yc_total.Smod
yd_total.Smod
ze_total.Smod
zf_total.Smod

xm=0.02;
ym=0.02;
zm=0.02;

xp=0.98;
yp=0.98;
zp=0.98;

x=[];
y=[];
z=[];
u=[];
v=[];
w=[];

[h, d]=readPrnFile('xa_id_00_poynting.prn');
x = cat(1, x, xm*ones(size(d(:,1))));
y = cat(1, y, d(:,1));
z = cat(1, z, d(:,2));
u = cat(1, u, d(:,3));
v = cat(1, v, d(:,4));
w = cat(1, w, d(:,5));

[h, d]=readPrnFile('xb_id_00_poynting.prn');
x = cat(1, x, xp*ones(size(d(:,1))));
y = cat(1, y, d(:,1));
z = cat(1, z, d(:,2));
u = cat(1, u, d(:,3));
v = cat(1, v, d(:,4));
w = cat(1, w, d(:,5));

[h,d]=readPrnFile('yc_id_00_poynting.prn');
x = cat(1, x, d(:,1));
y = cat(1, y, ym*ones(size(d(:,1))));
z = cat(1, z, d(:,2));
u = cat(1, u, d(:,3));
v = cat(1, v, d(:,4));
w = cat(1, w, d(:,5));

[h,d]=readPrnFile('yd_id_00_poynting.prn');
x = cat(1, x, d(:,1));
y = cat(1, y, yp*ones(size(d(:,1))));
z = cat(1, z, d(:,2));
u = cat(1, u, d(:,3));
v = cat(1, v, d(:,4));
w = cat(1, w, d(:,5));

[h,d]=readPrnFile('ze_id_00_poynting.prn');
x = cat(1, x, d(:,1));
y = cat(1, y, d(:,2));
z = cat(1, z, zm*ones(size(d(:,1))));
u = cat(1, u, d(:,3));
v = cat(1, v, d(:,4));
w = cat(1, w, d(:,5));

[h,d]=readPrnFile('zf_id_00_poynting.prn');
x = cat(1, x, d(:,1));
y = cat(1, y, d(:,2));
z = cat(1, z, zp*ones(size(d(:,1))));
u = cat(1, u, d(:,3));
v = cat(1, v, d(:,4));
w = cat(1, w, d(:,5));

quiver3(x, y, z, u, v, w, 20);
xlabel('X');
ylabel('Y');
zlabel('Z');

%  x=u1;
%  z=u2;
%  [X,Z] = meshgrid(x, z);
%  Sx=d(:,:,1);
%  Sy=d(:,:,2);
%  Sz=d(:,:,3);
%  Y=zeros(size(Z))
%  Y=zeros(size(Z));
%  quiver3(X,Y,Z,Sx,Sy,Sz)
