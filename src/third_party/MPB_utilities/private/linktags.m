%list=linktags(data, tags)
%-------------------------
%
%Links any opening XML tag to its closing part.
%
% data      file content
% tags      data tag positions in [start stop] rows
% list      data tag positions in [tt it ot id|ip od|op] rows
%            tt      tag identificator (negative for closing tag)
%            it/ot   start/stop of tag parameters
%            id/od   start/stop of tag value
%            ip/op   pointer to complementary tag
%
function list=linktags(data, tags)
list=zeros(0,5);
name={'hdf5-file'; ...        %  1
      'rootgroup'; ...        %  2
      'dataset'; ...          %  3
      'dataspace'; ...        %  4
      'scalardataspace'; ...  %  5
      'simpledataspace'; ...  %  6
      'dimension'; ...        %  7
      'datatype'; ...         %  8
      'atomictype'; ...       %  9
      'floattype'; ...        % 10
      'stringtype'; ...       % 12
      'data'; ...             % 13
      'datafromfile'};        % 14
for i=1:size(tags,1)          % identification
   s=data(tags(i,1):tags(i,2));
   p=find(s > ' ');
   s=s(p(1):p(length(p)));
   p=findstr(s,' ');
   if length(p)
      t=lower(s(1:p(1)-1));
   else
      t=lower(s);
   end;
   if t(1) == '/'
      d=-strmatch(t(2:length(t)),name,'exact');
   else
      d=strmatch(t,name,'exact');
   end;
   if length(d) == 1
      list(size(list,1)+1,:)=[d tags(i,1)+length(t) tags(i,1)+length(s)-1 tags(i,2)+2 tags(i,1)-2];
      if s(length(s)) == '/'
         list(size(list,1),3)=list(size(list,1),3)-1;
         list(size(list,1)+1,:)=[-d 0 0 0 tags(i,2)+1];
      end;
   end;
end;
for i=1:length(name)          % grouping
   p=find(abs(list(:,1)) == i);
   while length(p)
      v=list(p,1);
      for o=2:length(v)
         if ~sum(v(1:o))
            list(p(1),5)=p(o);
            list(p(o),4)=p(1);
            p=[p(2:o-1) p(o+1:length(v))];
            break;
         end;
      end;
   end;
end;
