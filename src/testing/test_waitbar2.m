function [valueofpi step] = test_waitbar2(steps)
  % Converge on pi in steps iterations, displaying waitbar.
  % User can click Cancel or close button to exit the loop.
  % Ten thousand steps yields error of about 0.001 percent.
  
  % TODO: CreateCancelBtn not supported in Octave
  
  h = waitbar(0,'1','Name','Approximating pi...',...
              'CreateCancelBtn',...
              'setappdata(gcbf,''canceling'',1)');
  setappdata(h,'canceling',0)
  % Approximate as pi^2/8 = 1 + 1/9 + 1/25 + 1/49 + ...
  pisqover8 = 1;
  denom = 3;
  valueofpi = sqrt(8 * pisqover8);
  for step = 1:steps 
      % Check for Cancel button press
      if getappdata(h,'canceling')
          break
      end
      % Report current estimate in the waitbar's message field
      waitbar(step/steps,h,sprintf('%12.9f',valueofpi))
      % Update the estimate
      pisqover8 = pisqover8 + 1 / (denom * denom);
      denom = denom + 2;
      valueofpi = sqrt(8 * pisqover8);
  end
  delete(h)       % DELETE the waitbar; don't try to CLOSE it.
end
