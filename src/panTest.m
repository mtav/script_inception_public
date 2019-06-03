function panTest
  % Allow a line to have its own 'ButtonDownFcn' callback.
  hLine = plot(rand(1,10));
  set(hLine,'ButtonDownFcn','disp(''This executes'')');
  set(hLine,'Tag','DoNotIgnore');
  h = pan;
  set(h,'ButtonDownFilter',@mycallback);
  set(h,'Enable','on');
end

% mouse click on the line
%
function [flag] = mycallback(obj,event_obj)
  % If the tag of the object is 'DoNotIgnore', then return true.
  % Indicate what the target is
  disp(['Clicked ' get(obj,'Type') ' object'])
  objTag = get(obj,'Tag');
  if strcmpi(objTag,'DoNotIgnore')
     flag = true;
  else
     flag = false;
  end
end
