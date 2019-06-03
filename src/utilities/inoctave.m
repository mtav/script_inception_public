function ret = inoctave()
  % Returns true if called from GNU Octave, else false.
  %
  % possible alternative code
  %   if size(ver('Octave'),1)
  %     OctaveMode = 1;
  %   else
  %     OctaveMode = 0;
  %   end
  persistent ret_persistent;
  if isempty(ret_persistent)
    ret_persistent = exist('OCTAVE_VERSION','builtin') ~= 0;
  end
  ret = ret_persistent;
end
