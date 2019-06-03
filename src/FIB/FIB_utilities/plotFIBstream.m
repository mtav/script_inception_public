function plotFIBstream(x, y, dwell, magnitude)
  % visualize expected results of a FIB stream
  % TODO: Incorporate dwell time, spot size, magnification, etc
  %plot(x, y, '-r.', 'MarkerEdgeColor', 'b', 'MarkerFaceColor', 'b');
  
  if exist('magnitude','var') == 1
    [res, HFW] = getResolution(magnitude);
    subplot(1,2,1);
    plotFIBstream_single(x, y, dwell, 'pixels', 'pixels', 1);
    subplot(1,2,2);
    plotFIBstream_single(x, y, dwell, 'mum', 'mum', res);
  else
    plotFIBstream_single(x, y, dwell, 'pixels', 'pixels', 1);
  end
  

end

function plotFIBstream_single(x, y, dwell, xlabel_text, ylabel_text, res)
  set(gca,'Ydir','reverse');
  
  dotsize = 6;  %adjust as needed
  scatter3(res*x, res*y, -dwell, dotsize, -dwell, 'filled');  hold on;
  colorbar();
  
  view(2);
  xlabel(xlabel_text);
  ylabel(ylabel_text);
  zlabel('-1 * dwell time');
  axis(res*[0 4095 280 3816]);
  %pbaspect([1,1,1]);
  daspect([1024, 1024, max(dwell(:))]);
  
  % different visualization techniques:
  %figure;
  %%animate = true
  %animate = false;
    
  %if exist('magnitude','var')==1
    %subplot(1, 2, 1);
    %plot(x, y, '-r.', 'MarkerEdgeColor', 'b', 'MarkerFaceColor', 'b'); hold on;
    %subplot(1, 2, 2);
    %plot(res*x, res*y, '-r.', 'MarkerEdgeColor', 'b', 'MarkerFaceColor', 'b'); hold on;
  %else
    %if animate
      %delay = 0.00001  % seconds
      %step = 1000;
      %%delay = 0  % seconds
      %%comet(x, y, delay); hold on;
      
      %axis([0 4096 0 4096]);
      %hold on;
      
      %cometFast2D(x, y, delay, step);
      
      %%figure;
      %%axis([min(x(:)), max(x(:)), min(y(:)), max(y(:))]);
      %%hold on;
      
      %%disp('START');
      %%for ii = 1:length(x)
        %%plot(x(ii), y(ii), '-r.', 'MarkerEdgeColor', 'b', 'MarkerFaceColor', 'b'); hold on;
        %%pause(.00001);
      %%end
      %%disp('DONE');
    %else
      %plot(x, y, '-r.', 'MarkerEdgeColor', 'b', 'MarkerFaceColor', 'b'); hold on;
    %end
  %end
    
  %%if (nargin==0)
  %%%     scatter(x,y)
  %%% plot(x,y)
      %%set(gca,'YDir','reverse');
      %%title([num2str(length(x)),' Points']);
  %%%     
  %%%     spotR=1;
  %%%     for m=1:min(55500,length(x))
  %%%     % for m=1:length(x)
  %%%     rectangle('Position',[x(m)-spotR,y(m)-spotR,2*spotR,2*spotR],'Curvature',[1,1])
  %%%     end
  %%%     axis equal
  %%end
    
  %% A=zeros(4094,4096);
  
  %% for m=1:length(x)
  %%   A(x(m),y(m))=dwell(m);
  %% end
  %% B=autoCrop(A);
  %% surf(B);
  %% imagesc(A)
  %% imagesc(B)
  
  %% pbaspect temporarily disabled for quick octave (3.2.4) compatibility
  %% (although the function seems to be available on later octave versions)
  %if exist('magnitude','var') == 1
    %subplot(1,2,1);
    %xlabel('pixels');
    %ylabel('pixels');
    %axis([0 4096 0 4096]);
    %if ~inoctave()
      %pbaspect([1,1,1]);
    %end
    %subplot(1,2,2);
    %xlabel('mum');
    %ylabel('mum');
    %axis([0 res*4096 0 res*4096]);
    %if ~inoctave()
      %pbaspect([1,1,1]);
    %end
  %else
    %xlabel('pixels');
    %ylabel('pixels');
    %axis([0 4096 0 4096]);
    %if ~inoctave()
      %pbaspect([1,1,1]);
    %end  
  %end
end
