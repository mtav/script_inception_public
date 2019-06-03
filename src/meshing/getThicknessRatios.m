function [direct_ratio, normalized_ratio] = getThicknessRatios(mymesh)
  % returns two ratio vectors:
  %   direct_ratio : t(i+1)/t(i)
  %   normalized_ratio : t(i+1)/t(i) or t(i)/t(i+1), whichever is >1
  % TODO: include left and right ratio?
  
  thickness = diff(mymesh);
  direct_ratio = thickness(2:end)./thickness(1:end-1);
  
  normalized_ratio = [];
  for idx = 2:length(thickness)
    normalized_ratio(end+1) = getRatio(thickness(idx-1), thickness(idx));
  end
end
