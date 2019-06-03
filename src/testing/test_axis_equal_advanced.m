close all;
clear all;

function testPlot(alpha, beta)
  
  theta = linspace(0,2*pi);
  xref = cos(theta);
  yref = sin(theta);
  plot(xref, yref, 'b-');
  hold on;
  plot(0.5*xref, 0.5*yref, 'b-');
  
  x = xref;
  y = beta*yref;
  plot(x, y, 'r--');
  
  title(sprintf('alpha=%f beta=%f', alpha, beta));
  
  axes_position = get(gca,'Position');
  
  if alpha < 1
    set(gca, 'Position', [axes_position(1), axes_position(2), axes_position(3), alpha*axes_position(3)]);
  else
    set(gca, 'Position', [axes_position(1), axes_position(2), axes_position(4)/alpha, axes_position(4)]);
  end
  
  axis_equal_advanced(gca, x, y, [0, 0.5], [0, 0.5], 'relative_data_coordinates', false);
  
end

figure;

% alpha < beta
subplot(3,2,1);
testPlot(0.5, 0.75);
subplot(3,2,3);
testPlot(0.5, 1.5);
subplot(3,2,5);
testPlot(1.25, 1.5);

% alpha > beta
subplot(3,2,2);
testPlot(0.75, 0.5);
subplot(3,2,4);
testPlot(1.5, 0.5);
subplot(3,2,6);
testPlot(1.5, 1.25);

%figure;
%subplot(1,2,1)

%plot(x,y);
%hold on;
%plot(x,y);

%alpha = 
%axes_position = get(gca,'Position');

%set(gca, 'Position', [axes_position(1), axes_position(2), 0.5, 0.5]);
%axis_equal_advanced(gca, x, y, [0,0]);

%pause;
%set(gca, 'Position', [axes_position(1), axes_position(2), 0.5, 0.8]);
%axis_equal_advanced(gca, x, y, [0,0]);

%pause;
%set(gca, 'Position', [axes_position(1), axes_position(2), 0.8, 0.5]);
%axis_equal_advanced(gca, x, y, [0,0]);

%pause;
%set(gca, 'Position', [axes_position(1), axes_position(2), 0.5, 0.8]);
%axis_equal_advanced(gca, x, y, [0,0]);

%pause;
%set(gca, 'Position', [axes_position(1), axes_position(2), 0.5, 0.8]);
%axis_equal_advanced(gca, x, y, [0,0]);

%pause;
%set(gca, 'Position', [axes_position(1), axes_position(2), 0.5, 0.8]);
%axis_equal_advanced(gca, x, y, [0,0]);
