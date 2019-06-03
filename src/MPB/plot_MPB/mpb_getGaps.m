function ret = mpb_getGaps(mpbdata)
  % TODO: This could easily take just any matrix for more flexibility?
  
  % get min/max values in each column (along dimension 1)
  ret.minima = min(mpbdata.data.normalized_frequency, [], 1);
  ret.maxima = max(mpbdata.data.normalized_frequency, [], 1);
  
  % all gap values, even if negative
  ret.gaps.top = ret.minima(2:end);
  ret.gaps.bottom = ret.maxima(1:end-1);
  ret.gaps.size_absolute = ret.gaps.top - ret.gaps.bottom;
  ret.gaps.midgap = 0.5*(ret.gaps.top + ret.gaps.bottom);
  ret.gaps.size_relative = ret.gaps.size_absolute./ret.gaps.midgap;
  
  % extract positive gaps (i.e. full gaps)
  
  % get indices
  ret.fullgaps.bottom_band_idx = find(ret.gaps.size_absolute > 0);
  
  % extract based on found indices
  ret.fullgaps.top = ret.gaps.top(ret.fullgaps.bottom_band_idx);
  ret.fullgaps.bottom = ret.gaps.bottom(ret.fullgaps.bottom_band_idx);
  ret.fullgaps.size_absolute = ret.gaps.size_absolute(ret.fullgaps.bottom_band_idx);
  ret.fullgaps.midgap = ret.gaps.midgap(ret.fullgaps.bottom_band_idx);
  ret.fullgaps.size_relative = ret.gaps.size_relative(ret.fullgaps.bottom_band_idx);
end
