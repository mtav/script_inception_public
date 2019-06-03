function [data, n] = density(data, n)
  %[data,n]=density(data, n)
  %-------------------------
  %
  %Computes the empirical density of states either by counting the
  %number of modes per bin or by the free space formula (assuming
  %spherical/circular k-vector surfaces of constant energy).
  %
  % data   band structure completed with
  %     .density    density of states in [f d] rows
  %
  % n      number of bins or zero for extrapolation
  %           if not specified, extrapolation is choosen
  %           whenever the velocity data is present, the
  %           number of bins is set automatically else.
  %
  if nargin < 2 | isempty(n) | ~isnumeric(n)
     if velocity(data)
        n = 0;
     else
        n = ceil(sqrt(prod(size(data.bands))));
     end;
  else
     if n <= 0
        if ~velocity(data)
           n=ceil(sqrt(prod(size(data.bands))));
        else
           n=0;
        end;
     else
        n=ceil(n);
     end;
  end;
  
  n
  
  if n
     disp('Using frequency bins');
     m=max(max(data.bands));    % frequency bins
     i=m/(2*n);
     data.density=[(i:2*i:m)' zeros(n,1)];
     for m=1:n
        data.density(m,2)=sum(sum(abs(data.bands-data.density(m,1)) < i));
     end;
  else
     disp('Using group velocity');
     v=[];                      % group velocity
     if data.grid(1) > 1
        v=data.xvelocity.^2;
     end;
     if data.grid(2) > 1
        if isempty(v)
           v=data.yvelocity.^2;
        else
           v=v+data.yvelocity.^2;
        end;
     end;
     if data.grid(3) > 1
        if isempty(v)
           v=data.zvelocity.^2;
        else
           v=v+data.zvelocity.^2;
        end;
     end;
     v=sqrt(v);
     s=data.lattice(find(data.grid > 1),:);
     d=size(s,1);
     switch d                   % dimension
     case 1
        s=2*sqrt(norm(s))/pi;
     case 2
        s=sqrt(norm(cross(s(1,:),s(2,:))))/pi;
     case 3
        s=sqrt(norm(sum(s(3,:).*cross(s(1,:),s(2,:)))))/pi^2;
     otherwise
        warning('Point density skipped.');
        data.density=zeros(0,2);
        return;
     end;
     data.density=zeros(prod(size(v)),2);
     j=size(v,1);
     for i=1:size(v,2)          % vectorize & sort
        data.density(1+(i-1)*j:i*j,:)=[data.bands(:,i) v(:,i)];
     end;
     [data.density(:,1) i]=sort(data.density(:,1));
     data.density(:,2)=s*data.density(:,1).^(d-1)./max(0.000001,data.density(i,2).^d);
  end;


  %Checks if the extrapolation can be computed
  %
  function flag=velocity(data)
    flag=0;
    if data.grid(1) > 1 & (~isfield(data,'xvelocity') | ~isequal(size(data.bands),size(data.xvelocity)))
       return;
    end;
    if data.grid(2) > 1 & (~isfield(data,'yvelocity') | ~isequal(size(data.bands),size(data.yvelocity)))
       return;
    end;
    if data.grid(3) > 1 & (~isfield(data,'zvelocity') | ~isequal(size(data.bands),size(data.zvelocity)))
       return;
    end;
    flag=1;
  end
end
