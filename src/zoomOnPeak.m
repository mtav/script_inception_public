function [ peakdata_all, peakdata_loc ] = zoomOnPeak( Xin, Yin, delta )

  if exist('delta','var')==0
    disp('delta not given');
    aver = sum(Yin)/length(Yin);
    delta = (max(Yin)-aver)/3;
  end
  
    if (delta<0)
        return;
    end
  
  peakdata_all = [];
  peakdata_loc = [];
  
  peaks = peakdet(Yin, delta);
  index_peaks = peaks(:,1);

    indMin = max(index_peaks(1)-150,1);
    indMax = min(index_peaks(length(index_peaks))+150,length(Xin));
    Xzoom = Xin(indMin:indMax);
  Yzoom = Yin(indMin:indMax);
  peakdata_all.indMin = indMin;
  peakdata_all.indMax = indMax;
  peakdata_all.Xzoom = Xzoom;
  peakdata_all.Yzoom = Yzoom;

  % define structure
  s.indMin = 0;
  s.indMax = 0;
  s.index = 0;
  s.Xzoom = [0];
  s.Yzoom = [0];
  
  s.frequency = 0;
  s.decay_constant = 0;
  s.Q = 0;
  s.amplitude = 0;
  s.phase = 0;
  s.error = 0;

  s.indMin = 0;
  s.indMax = 0;
  s.Xzoom = [0];
  s.Yzoom = [0];
  % s.vStart = vStart;
  % s.vEnd = vEnd;

  peakdata_loc = repmat(s,1,length(index_peaks));

  % s = struct('indMin', {indMin}, 'indMax', {indMax}, 'Xzoom', {Xzoom}, 'Yzoom', {Yzoom});
    % peakdata_all = [ peakdata_all ; s ];

  for peak_idx=1:length(index_peaks)
    indMin = max(index_peaks(peak_idx)-150,1);
    indMax = min(index_peaks(peak_idx)+150,length(Xin));
    Xzoom = Xin(indMin:indMax);
    Yzoom = Yin(indMin:indMax);
    Xzoom = Xzoom(:);
    Yzoom = Yzoom(:);
    
    [x0, y0, A, FWHM] = getLorentzStartValues(Xzoom, Yzoom, 0);
    vStart = [x0, y0, A, FWHM];
    [x0, y0, A, FWHM] = getLorentzEndValues(Xzoom, Yzoom, vStart, 0);
    vEnd = [x0, y0, A, FWHM];

    Q = vEnd(1)/vEnd(4);

    % peakdata_loc(peak_idx).frequency
    % peakdata_loc(peak_idx).decay_constant
    % peakdata_loc(peak_idx).Q
    % peakdata_loc(peak_idx).amplitude
    % peakdata_loc(peak_idx).phase
    % peakdata_loc(peak_idx).error
    
    peakdata_loc(peak_idx).index = index_peaks(peak_idx);
    peakdata_loc(peak_idx).indMin = indMin;
    peakdata_loc(peak_idx).indMax = indMax;
    peakdata_loc(peak_idx).Xzoom = Xzoom;
    peakdata_loc(peak_idx).Yzoom = Yzoom;
    peakdata_loc(peak_idx).vStart = vStart;
    peakdata_loc(peak_idx).vEnd = vEnd;
    peakdata_loc(peak_idx).Q = Q;
  end

end
