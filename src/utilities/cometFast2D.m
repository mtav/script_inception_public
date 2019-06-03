function cometFast2D(x, y, delay, step)

  if ~exist('delay','var')
    delay = 0.001;
  end

  if ~exist('step','var')
    step = 1;
  end

  newFigure = false;
  if newFigure
    figure;
    axis([min(x), max(x), min(y), max(y)]);
  end

  N = length(x);

  % plot the first point to get started
  h = plot(x(1), y(1), "b");

  % refresh the plot in a loop through the rest of the data
  for k = 1:step:N;
    set(h, 'XData', x(1:k));
    set(h, 'YData', y(1:k));
    pause (delay); % delay in seconds
    % alternatively could provide a velocity function
    % pause(sqrt(vx(k)^2+vy(k)^2+vz(k)^2));  
  end

  % if N was not reached with the given step
  set(h, 'XData', x);
  set(h, 'YData', y);  
end
