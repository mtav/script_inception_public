function R = getLocalSurfRange(X, Y, Z)
  % TODO: extend to any-dimensional data?
  
  r = sla(find(lat >=2 & lat <= 3 & lon >=95 & lon <= 97))
  
  if ~isreal(data)
    error('getRange() only supports real data.');
  end
  R = [min(data(:)), max(data(:))];
end
