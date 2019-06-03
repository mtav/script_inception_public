function B = meepBlock(center, size,epsilon)
  center = center(:)';
  
  sizeStr='size ';
  for m = 1:length(size)
      if size(m)==Inf
          sizeStr = [sizeStr,'infinity '];
      else
          sizeStr = [sizeStr,num2str(size(m),'%4.9g'),' '];
      end
  end

  % B=['\t\t(make block\n
  % \t\t\t(center ',num2str(center,'%4.9g '),')\n
  % \t\t\t(',sizeStr,')\n
  % \t\t\t(material (make dielectric (epsilon ',num2str(epsilon),'))))\r\n'];

  B = ['\t\t(make block\n'];
  B = [B, '\t\t\t(center ',num2str(center,'%4.9g '),')\n'];
  B = [B, '\t\t\t(',sizeStr,')\n'];
  B = [B, '\t\t\t(material (make dielectric (epsilon ',num2str(epsilon),'))))\n'];

  % Center=struct('type',{'center'},'properties',{{center}});
  % Size=struct('type',{'size'},'properties',{{size}});
  % Epsilon=struct('type',{'epsilon'},'properties',{{epsilon}});
  % Make=struct('type',{'make'},'properties',{{'dielectric',Epsilon}});
  % Material=struct('type',{'material'},'properties',{{Make}});
  % 
  % B=struct('type',{'block'},'properties',{{Center,Size,Material}})
end
