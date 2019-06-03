function [res, HFW] = getResolution(mag)
  % function [res, HFW] = getResolution(mag)
  HFW = 304000/mag; % Width of the horizontal scan (mum).
  res = HFW/4096; % size of each pixel (mum/pxl).
end
