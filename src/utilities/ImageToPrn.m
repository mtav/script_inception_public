function ImageToPrn(imagefile, prnfile)
  data = imread(imagefile);
  data = double(data); % in case we get logical values...
  data = flip(data, 1); % flipped vertically because we assume that the "Y axis" points up in the image
  
  % u1 and u2 correspond to the "X" and "Y" axes according to meshgrid standards, i.e. dimensions 2 and 1 respectively.
  u1 = 1:size(data, 2);
  u2 = 1:size(data, 1);
  
  writePrnFile(prnfile, {'u1', 'u2', 'data'}, data, u1, u2);
end
