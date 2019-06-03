function createSymmetricSnapshot(snapshot, outfile)
  % function createSymmetricSnapshot(snapshot, outfile)
  % at the moment "symmetrifies" XZ snapshot along X axis
  % TODO: Validate with simpler snapshots + add arguments to specify symmetry plane?
  % TODO: Make symmetric or anti-symmetric depending on field type... Validate with theory and half/full simulations...
  
  % read in data
  [header, data, ui, uj] = readPrnFile(snapshot);
  
  ui2 = [ui;2*ui(end)-flipud(ui(1:end-1))];
  data2 = cat(2,data,flipdim(data(:,1:end-1,:),2));
  data3 = reshape(data2,size(data2,1)*size(data2,2),size(data2,3));

  new_data = [ kron(ui2,ones(length(uj),1)), repmat(uj,length(ui2),1), data3 ];
  
  new_header = [];
  for i = 1:length(header)
    if i == 1
      new_header = [new_header, header{i}];
    else
      new_header = [new_header, ' ', header{i}];
    end
  end
  
  % write energy snapshot to outfile
  writePrnFile(outfile, new_header, new_data);
end
