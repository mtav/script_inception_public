function ret = octaveVersionLessThan(version_array)
  current_version_array = versionArray();
  for idx = 1:length(version_array)
    if current_version_array(idx) < version_array(idx)
      ret = true;
      return
    elseif current_version_array(idx) > version_array(idx)
      ret = false;
      return    
    end
  end
  ret = false;
end
