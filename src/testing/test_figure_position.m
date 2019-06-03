% Script File: ShowPosition
% How to position the current figure window.
%
% Syntax: set(gcf,'position',[a b L W])
%
% (a,b) = is the lower left corner
% L = the horizontal length of the window
% W = the vertical width of the window
%
% Different screens have different dimensions.
% A window that fits on one screen may not fit on another.
% Vary the lower left corner...
close;
figure;
shg; % Show the graph window.
L = 600;
W = 400;
for a = 50:100:350
  for b = 50:50:200
    set(gcf,'position',[a b L W])
    title(sprintf('[ a , b , L , W ] = [%1d , %1d , %1d , %1d]',a,b,L,W),'Fontsize',14)
    text(.3,.5,'Vary Lower Left Corner (a,b)','Fontsize',14)
    pause
  end
end

% Vary the length and width of the figure...
close;
figure;
shg;
a = 100;
b = 100;
for L = 500:100:900
  for W = 100:100:500
    set(gcf,'position',[a b L W])
    title(sprintf('[ a , b , L , W ] = [%1d , %1d , %1d , %1d]',a,b,L,W),'Fontsize',14)
    text(.3,.5,'Vary Length and Width','Fontsize',14)
    pause
  end
end
