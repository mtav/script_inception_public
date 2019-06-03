%item=fetch(data, tags)
%----------------------
%
%Scans a HDF5 dataset and puts the values in a structure.
%
% data         file content replaced by structure
% tags         data tag positions (see 'linktags')
%
function data=fetch(data, tags)
if tags(1,1) ~= 1 | tags(2,1) ~= 2
   error('Not a valid HDF5-File.');
end;
root.data=data;
root.tags=tags;
data={};
i=3;
while i < size(tags,1) & tags(i,1) == 3
   item=extract(root,i);
   if item.tags(1,1) == 4
      dims=[];
      switch item.tags(2,1)
      case 5         % ScalarDataspace
         dims=0;
      case 6         % SimpleDataspace
         p=parameters(item,2);
         n=str2double(p.ndims);
         k=3;
         while length(dims) < n & k < item.tags(2,5)
            if item.tags(k,1) == 7
               p=parameters(item,k);
               dims(length(dims)+1)=str2double(p.dimsize);
               k=item.tags(k,5);
            end;
            k=k+1;
         end;
         if length(dims) < n
            error('Corrupt DataSpace.');
         end;
      otherwise
         error('Unknown DataSpace.');
      end;
      k=item.tags(1,5)+1;
      if isequal(item.tags(k:k+1,1),[8;9])
         switch item.tags(k+2,1)
         case 10     % FloatType
            type='float';
         case 11     % StringType
            p=parameters(item,k+2);
            dims=str2double(p.strsize)-1;
            type='string';
         otherwise
            type='';
         end;
      else
         error('Corrupt DataType.');
      end;
      k=item.tags(k,5)+1;
      if isequal(item.tags(k:k+1,1),[12;13])
         item=extract(item,k+1);
         item=item.data;
         switch type
         case 'float'
            [item,k]=sscanf(item,'%f',dims);
            if k ~= prod(dims)
               fprintf('Matrix truncated.\n');
            end;
            item=item';
         case 'string'
            item=characters(item);
            if length(item) ~= dims
               fprintf('String truncated.\n');
            end;
         end;
      else
         error('Corrupt Data.');
      end;
      p=parameters(root,i);
      eval(['data.' variable(p.name) '=item;']);
   end;
   i=root.tags(i,5)+1;
end;


%Extracts a dataset out of its context
%
function data=extract(data, ip)
op=data.tags(ip,5);
id=data.tags(ip,4)-1;
data.data=data.data(id+1:data.tags(op,5));
data.tags=data.tags(ip+1:op-1,:);
i=find(data.tags(:,1) > 0);
o=find(data.tags(:,1) < 0);
data.tags(i,4)=data.tags(i,4)-id;
data.tags(i,5)=data.tags(i,5)-ip;
data.tags(o,4)=data.tags(o,4)-ip;
data.tags(o,5)=data.tags(o,5)-id;
data.tags(:,2:3)=data.tags(:,2:3)-id;


%Forms a valid variable name
%
function s=variable(s);
s=lower(s);
s=s(find(s >= 'a' & s <= 'z'));
switch s
case 'blochwavevector'
   s='vector';
case 'description'
   s='info';
case 'latticevectors'
   s='lattice';
end;


%Scans for the tag parameters and puts them in a structure.
%
function list=parameters(data, ip)
s=data.data(data.tags(ip,2):data.tags(ip,3));
i=find(s > ' ');
while length(i)
   s=s(i(1):length(s));
   i=findstr(s,' ');
   j=findstr(s,'="');
   if ~length(i)
      i=length(s)+1;
   end;
   if length(j) & j(1) < i(1)
      p=s(1:j(1)-1);
      v=characters(s(j(1):length(s)));
      s=s(j(1)+length(v)+3:length(s));
   else
      v=[];
      p=s(1:i(1)-1);
      s=s(i(1)+1:length(s));
   end;
   eval(['list.' variable(p) '=''' v ''';']);
   i=find(s > ' ');
end;


%Scans for the first complete string.
%
function s=characters(s)
j=2;
i=findstr(s,'"');
while j < length(i)-1
   if i(j+1)-i(j) == 1
      i=[i(1:j-1) i(j+1:length(i))];
   else
      j=j+1;
   end;
end;
s=s(i(1)+1:i(2)-1);
