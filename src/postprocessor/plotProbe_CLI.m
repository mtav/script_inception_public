function [ wavelength_nm, Q_lorentz, Q_harminv_local, Q_harminv_global, handles ] = plotProbe_CLI(ProbeFile, column)
  % create default handles object for convenient CLI usage
  % TODO: Use inputParser...
  
  handles = struct();
  handles.ProbeFile = ProbeFile;
  
  if exist('column','var')==0
    handles.col =  -1;
  else
    handles.col =  column;
  end
  
  handles.autoZoomTime = false;
  handles.DoAnalysis = false;
  handles.useFFTrange = false;
  handles.FFT_f_or_lambda =  1;
  handles.FFT_xlabel = 'f(MHz)';
  handles.FFT_scalingFactor = 1;
  handles.autoZoomFFT = false;
  
  [ wavelength_nm, Q_lorentz, Q_harminv_local, Q_harminv_global, handles ] = plotProbe(handles);
end
