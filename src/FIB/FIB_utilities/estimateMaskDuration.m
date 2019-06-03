function estimateMaskDuration(x, y, dwell, rep)
  numPoints = length(dwell);
  % calculate approximate mask duration
  sec = rep*(sum(dwell)*1e-7+0.008163229517396*numPoints);
  hour   = fix(sec/3600);      % get number of hours
  sec    = sec - 3600*hour;    % remove the hours
  minute = fix(sec/60);        % get number of minutes
  sec    = sec - 60*minute;    % remove the minutes
  second = sec;
  disp(sprintf('Approximate Mask Duration is %2.5f hours %2.5f minutes %2.5f seconds',hour,minute,second));
end
