function [dx,dy,dz] = autoMeshGeometry(geoFilePath,lambda)

  [ entries, structured_entries ] = GEO_INP_reader({geoFilePath});

  xvec=[];
  yvec=[];
  zvec=[];
  epsx=[];
  epsy=[];
  epsz=[];
  
  simMinX=structured_entries.box.lower(1);
  simMinY=structured_entries.box.lower(2);
  simMinZ=structured_entries.box.lower(3);
  simMaxX=structured_entries.box.upper(1);
  simMaxY=structured_entries.box.upper(2);
  simMaxZ=structured_entries.box.upper(3);
  objx=sort([structured_entries.box.lower(1),structured_entries.box.upper(1)]);
  objy=sort([structured_entries.box.lower(2),structured_entries.box.upper(2)]);
  objz=sort([structured_entries.box.lower(3),structured_entries.box.upper(3)]);

  eps=1;
  xvec
  objx
  xvec=[xvec;objx]
  yvec=[yvec;objy]
  zvec=[zvec;objz]
  epsx=[epsx;eps]
  epsy=[epsy;eps]
  epsz=[epsz;eps]

  for m=1:length(entries)

    entry=entries{m};

    switch upper(entry.type)
      case 'BOX'
        data=entries{m}.data;
        objx=sort([data(1),data(4)]);
        objy=sort([data(2),data(5)]);
        objz=sort([data(3),data(6)]);
        eps=1;
        xvec=[xvec;objx];
        yvec=[yvec;objy];
        zvec=[zvec;objz];
        epsx=[epsx;eps];
        epsy=[epsy;eps];
        epsz=[epsz;eps];
      case 'BLOCK'
        data=entries{m}.data;
        objx=sort([data(1),data(4)]);
        objy=sort([data(2),data(5)]);
        objz=sort([data(3),data(6)]);
        eps=data(7);
        cond=data(8);
        xvec=[xvec;objx];
        yvec=[yvec;objy];
        zvec=[zvec;objz];
        epsx=[epsx;eps];
        epsy=[epsy;eps];
        epsz=[epsz;eps];
      case 'SPHERE'
        data=entries{m}.data;
        r=max(data(5),data(4));
        eps=data(6);
        cond=data(7);
        objx=[data(1)-r,data(1)+r];
        objy=[data(2)-r,data(2)+r];
        objz=[data(3)-r,data(3)+r];
        xvec=[xvec;objx];
        yvec=[yvec;objy];
        zvec=[zvec;objz];
        epsx=[epsx;eps];
        epsy=[epsy;eps];
        epsz=[epsz;eps];
      case 'CYLINDER'
        data=entries{m}.data;
        xyz=data(1:3);
        r=max(data(5),data(4));
        h=data(6);
        eps=data(7);
        cond=data(8);
        objx=[data(1)-r,data(1)+r];
        objy=[data(2)-r,data(2)+r];
        objz=[data(3)-h/2,data(3)+h/2];
        xvec=[xvec;objx];
        yvec=[yvec;objy];
        zvec=[zvec;objz];
        epsx=[epsx;eps];
        epsy=[epsy;eps];
        epsz=[epsz;eps];
      otherwise
        disp('Unknown case');
    end
  end


  xvec(find(xvec<simMinX))=simMinX;
  xvec(find(xvec>simMaxX))=simMaxX;
  yvec(find(yvec<simMinY))=simMinY;
  yvec(find(yvec>simMaxY))=simMaxY;
  zvec(find(zvec<simMinZ))=simMinZ;
  zvec(find(zvec>simMaxZ))=simMaxZ;

  %%
  VX=unique(sort([xvec(:,1);xvec(:,2)]));
  MX=zeros(size(xvec,1),length(VX));

  for m=1:size(xvec,1)
    indmin=find(VX==xvec(m,1));
    indmax=find(VX==xvec(m,2));
    eps=epsx(m);
    vv=zeros(1,length(VX));
    vv(indmin:indmax-1)=eps;
    MX(m,:)=vv;
  end


  thicknessVX=diff(VX)';
  epsVX=max(MX(:,1:end-1));

  %%
  VY=unique(sort([yvec(:,1);yvec(:,2)]));
  MY=zeros(size(yvec,1),length(VY));

  for m=1:size(yvec,1)
    indmin=find(VY==yvec(m,1));
    indmax=find(VY==yvec(m,2));
    eps=epsy(m);
    vv=zeros(1,length(VY));
    vv(indmin:indmax-1)=eps;
    MY(m,:)=vv;
  end

  thicknessVY=diff(VY)';
  epsVY=max(MY(:,1:end-1));

  %%
  VZ=unique(sort([zvec(:,1);zvec(:,2)]));
  MZ=zeros(size(zvec,1),length(VZ));

  for m=1:size(zvec,1)
    indmin=find(VZ==zvec(m,1));
    indmax=find(VZ==zvec(m,2));
    eps=epsz(m);
    vv=zeros(1,length(VZ));
    vv(indmin:indmax-1)=eps;
    MZ(m,:)=vv;
  end

  thicknessVZ=diff(VZ)';
  epsVZ=max(MZ(:,1:end-1));

  % dx = subGridMultiLayer(sqrt(epsVX), thicknessVX, lambda,offset);
  % dy = subGridMultiLayer(sqrt(epsVY), thicknessVY, lambda,offset);
  % dz = subGridMultiLayer(sqrt(epsVZ), thicknessVZ, lambda,offset);

  dx = subGridMultiLayer(lambda/16./sqrt(epsVX), thicknessVX);
  dy = subGridMultiLayer(lambda/16./sqrt(epsVY), thicknessVY);
  dz = subGridMultiLayer(lambda/16./sqrt(epsVZ), thicknessVZ);

end
