%tags=findtags(data)
%-------------------
%
%Looks for XML tags.
%
% data      file content
% tags      data tag positions in [start stop] rows
%
function tags=findtags(data)
i=findstr(data,'<')+1;     % tag starts
o=findstr(data,'>')-1;     % tag stops
tags=zeros(0,2);           % tags
p=1;
while length(i)
   while mod(length(findstr(data(i(1):o(p)),'"')),2)
      p=p+1;               % strings
   end;
   tags(size(tags,1)+1,:)=[i(1) o(p)];
   i=i(find(i > o(p)));
   p=p+1;
end;
