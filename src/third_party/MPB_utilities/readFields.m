%item=readFields(file)
%---------------------
%
%Scans a "MIT Photonic-Bands" created HDF5-File for file
%sections and reads them in. Drops zero matrixes and the
%9x9 epsilon tensor and its inverse to limit memory use.
%
% item         structure with datasets in named fields
%     .info       comment or description
%     .lattice    lattice vectors in [x y z] rows
%     .vector     Bloch wavevector in [x y z] row
%     .e          relative dielectric constant
%     .x          field in x rows / y columns
%     .y
%     .z
%
% file         file name of XML formatted HDF5-File
%
function item=readDatasets(file)
if ~nargin | ~ischar(file)
   error('Unknown or undefined argument.');
end;
[fid,msg]=fopen(file);
if fid == -1
   error(msg);
end;
data=strvcat(fread(fid,inf,'uchar'))';
data(find(data < ' '))='';          % drop line breaks ...
fclose(fid);
tags=findtags(data);                % search tags
tags=linktags(data,tags);           % group tags
data=fetch(data,tags);              % fetch data
n=fieldnames(data);                 % compact
i=1:length(n)';
i(strmatch('epsilon',n))=[];
item.info='unknown';
for i=i
   f=getfield(data,n{i});
   if ~isempty(f) & ~isequal(f,zeros(size(f)))
      switch n{i}
      case {'xr';'yr';'zr'}
         n{i}=n{i}(1);
         if isfield(item,n{i})
            f=complex(f,imag(getfield(item,n{i})));
         end;
      case {'xi';'yi';'zi'}
         n{i}=n{i}(1);
         if isfield(item,n{i})
            f=complex(real(getfield(item,n{i})),f);
         else
            if isfield(data,'xr') | isfield(data,'yr') | isfield(data,'zr')
               f=complex(zeros(size(f)),f);
            end;
         end;
      end;
      item=setfield(item,n{i},f);
   end;
end;
