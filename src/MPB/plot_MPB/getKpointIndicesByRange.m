function selected_k = getKpointIndicesByRange(mpbdata, field_name, mini, maxi, strict)

  if ~exist('strict', 'var'); strict=true; end;
  
  L = mpbdata.data.(field_name);
  if strict
    selected_k = find( and(mini < L, L < maxi) );
  else
    selected_k = find( and(mini <= L, L <= maxi) );
  end
end
