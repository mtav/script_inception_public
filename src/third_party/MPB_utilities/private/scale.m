%data=scale(data)
%----------------
%
%Scales the k axis of a frequency bands structure
%and sorts band frequencies in ascending order.
%
% data          band structure completed with
%     .edges         corner indexes
%     .scale         k-axis scaling centered on first Gamma point
%     .ticks         corner labels
%
function data=scale(data)
data.bands=sort(data.bands,2);
t=sum(data.lattice(1,:).*data.lattice(2,:))/prod(data.size(1:2));
if abs(t) < 0.000001        % rectangular lattice
   t={'G','X','X','Y','Y','M','M','M','M'};
   v=[ 0.0  0.0  0; ...     % Gamma point
       1/2  0.0  0; ...     % X point
      -1/2  0.0  0; ...
       0.0  1/2  0; ...     % Y point
       0.0 -1/2  0; ...
       1/2  1/2  0; ...     % M point
      -1/2  1/2  0; ...
       1/2 -1/2  0; ...
      -1/2 -1/2  0];
else
   if abs(t-0.5) < 0.000001 % triangular lattice
   t={'G','M','M','M','M','M','M','K','K','K','K','K','K'};
   v=[ 0.0  0.0  0; ...     % Gamma point
       1/2  0.0  0; ...     % M point
      -1/2  0.0  0; ...
       0.0  1/2  0; ...
       0.0 -1/2  0; ...
       1/2  1/2  0; ...
      -1/2 -1/2  0; ...
       1/3 -1/3  0; ...     % K point
      -1/3  1/3  0; ...
       2/3  1/3  0; ...
      -2/3 -1/3  0; ...
       1/3  2/3  0; ...
      -1/3 -2/3  0];
   else
      t={'G'};
      v=zeros(1,3);
   end;
end;
n=size(data.vectors,1);
e=data.vectors(2:n,1:3)-data.vectors(1:n-1,1:3);   % delta-k-vectors
d=sqrt(sum(e.*e,2));                               % delta-k-lengths
e=sum(e(2:n-1,:).*e(1:n-2,:),2)./(d(2:n-1).*d(1:n-2));
data.edges=[1;find(abs(e-1) > 0.000001)+1;n];
data.scale=zeros(n,1);
for i=1:n-1
   data.scale(i+1)=data.scale(i)+d(i);
end;
e=data.vectors(data.edges,1:3);                    % k-points
l={};
for i=1:length(data.edges)
   n=find(sum(abs(v-repmat(e(i,:),size(v,1),1)),2) < 0.000001);
   if isempty(n)
      l{i}='?';
   else
      l{i}=t{n};
      if t{n} == 'G' & ~data.scale(1)
         data.scale=data.scale-data.scale(data.edges(i));
      end;
   end;
end;
data.ticks=l;
