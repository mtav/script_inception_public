%flag=isbands(data)
%------------------
%
%Validates a frequency band structure.
%
%data    band structure
%flag    sum of all diagnostic flags
%     0  valid structure
%     1  file/geometry/polarity/time member invalid
%     2  velocity/parity member invalid
%     4  grid/size/lattice/reciprocal member invalid
%     8  vectors/bands/ranges member invalid
%
function flag = isbands(data)
  flag=15;
  if ~nargin | isempty(data) | ~isstruct(data)
      disp('FATAL ERROR');
     return;
  end;
  if isfield(data,'file') & isstr(data.file) ...
        & isfield(data,'geometry') & iscellstr(data.geometry) ...
        & isfield(data,'polarity') & isstr(data.polarity) ...
        & isfield(data,'time') & isnumeric(data.time)
     flag=flag-1;
     disp('0: OK');
  else
     disp('0: FAIL');
  end;
  if (~isfield(data,'xvelocity') || isnumeric(data.xvelocity)) ...
        & (~isfield(data,'yvelocity') || isnumeric(data.yvelocity)) ...
        & (~isfield(data,'zvelocity') || isnumeric(data.zvelocity)) ...
        & (~isfield(data,'yparity') || isnumeric(data.yparity)) ...
        & (~isfield(data,'zparity') || isnumeric(data.zparity))
     flag=flag-2;
     disp('1: OK');
  else
     disp('1: FAIL');
  end;
  if isfield(data,'grid') & isnumeric(data.grid) ...
        & isfield(data,'size') & isnumeric(data.size) ...
        & isequal(size(data.size),size(data.grid),[3 1]) ...
        & isfield(data,'lattice') & isnumeric(data.lattice) ...
        & isfield(data,'reciprocal') & isnumeric(data.reciprocal) ...
        & isequal(size(data.lattice),size(data.reciprocal),[3 3])
     flag=flag-4;
     disp('2: OK');
  else
     disp('2: FAIL');
  end;
  if isfield(data,'vectors') & isnumeric(data.vectors) & size(data.vectors,2) == 4 ...
        & isfield(data,'bands') & isnumeric(data.bands) & size(data.vectors,1) == size(data.bands,1) ...
        & isfield(data,'ranges') & isnumeric(data.ranges) & isequal(size(data.ranges),[2 size(data.bands,2)])
     flag=flag-8;
     disp('3: OK');
  else
     disp('3: FAIL');
  end;
end
