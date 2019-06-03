function R = getRange(data)
  % function R = getRange(data)
  % Returns R = [min(data(:)), max(data(:))]
  
  if ~isreal(data)
    error('getRange() only supports real data.');
  end
  R = [min(data(:)), max(data(:))];
end
