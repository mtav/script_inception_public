function selected_k = getKpointIndicesByValue(mpbdata, field_name, val_list, tol)

  if ~exist('tol', 'var'); tol=1e-10; end;

  selected_k = [];
  
  for val = val_list
    L = mpbdata.data.(field_name);
    matching_k = find( abs(L - val) <= tol );
    selected_k = [selected_k; matching_k(:)];
  end
  
  selected_k = unique(selected_k);
  
end
