% [Q, vStart, vEnd] = fitLorentzian(X, Y, xmin, xmax, isInverted)
%
% This function tries to fit Y using the following function:
%  y = y0 + (2*A/pi).*(w./(4*(x-x0).^2+w.^2))
%
% xmin,xmax : range on which to fit
% isInverted = 0 : standard lorentzian ("positive peak")
% isInverted = 1 : inverted lorentzian ("negative peak")
%
% return values:
% vStart = [x0, y0, A, FWHM] from a simple look at data properties like min, max, etc
% vEnd = [x0, y0, A, FWHM] from the real fitting function
% Q = vEnd(1)/vEnd(4) -> the Q factor
% 
% NOTE: Used to be named getQfactor() before.
%
% Example usage:
% >> x=linspace(500,700,200);
% >> y=lorentz([600,0,10,50],x);
% >> [Q, vStart, vEnd] = fitLorentzian(x, y, min(x), max(x), 0);
% >> figure;hold on;plot(x,y,'ro');plot(x,lorentz(vStart,x),'g-');plot(x,lorentz(vEnd,x),'b-');
% >> y=lorentz([600,0,-10,50],x);
% >> [Q, vStart, vEnd] = fitLorentzian(x, y, min(x), max(x), 1);
% >> figure;hold on;plot(x,y,'ro');plot(x,lorentz(vStart,x),'g-');plot(x,lorentz(vEnd,x),'b-');

function [Q, vStart, vEnd] = fitLorentzian(X, Y, xmin, xmax, isInverted)

  if exist('xmin','var')==0; xmin = min(X(:)); end;
  if exist('xmax','var')==0; xmax = max(X(:)); end;
  if exist('isInverted','var')==0; isInverted = 0; end;

  % limit the data to an [xmin,xmax] fitting range based on the previous plot
  [Xzoom,Yzoom] = zoomPlot(X,Y,xmin,xmax);
  
  % calculate some fit start values from the peak
  [x0, y0, A, FWHM] = getLorentzStartValues(Xzoom, Yzoom, isInverted);
  vStart = [x0, y0, A, FWHM];
  
  % fit the peak with a lorentz function
  [x0, y0, A, FWHM] = getLorentzEndValues(Xzoom, Yzoom, vStart, 0);
  vEnd = [x0, y0, A, FWHM];
  
  % calculate the Q factor
  Q = vEnd(1)/vEnd(4);
end
