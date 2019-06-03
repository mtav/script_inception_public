function data = harminv_plotSignal(infile)
  data = dlmread(infile);
  i = 2;
  j = 2;
  k = 1;
  k = plotRealImag(data, 'data', i, j, k);
  k = plotRealImag(fft(data), 'fft(data)', i, j, k);
end
