function [all_diff, header_diff, data_diff, h1, d1, h2, d2] = diffPrn(file1, file2)
  % compares 2 .prn files, header and data.
  % 1 means no difference
  % 0 means different
  
  [h1, d1] = readPrnFile(file1);
  [h2, d2] = readPrnFile(file2);
  header_diff = isequal(h1,h2);
  data_diff = isequal(d1,d2);
  all_diff = header_diff && data_diff;
end
