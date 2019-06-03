%data=bandgaps(data)
%-------------------
%
%Computes the band gaps and their relative
%extent to the mean frequency.
%
% data   band structure completed with
%     .gaps    band gaps in [f e] rows
%
function data=bandgaps(data)
i=size(data.ranges,2);
i=find(data.ranges(1,2:i) > data.ranges(2,1:i-1));
f=(data.ranges(1,i+1)+data.ranges(2,i))/2;
e=(data.ranges(1,i+1)-data.ranges(2,i))./f;
i=find(e > 0.01);
data.gaps=[f(i);e(i)];        % store only gaps > 1%
