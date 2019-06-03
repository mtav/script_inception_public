function [maxtab, mintab] = peakdet(v, delta, x)
  %PEAKDET Detect peaks in a vector
  %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
  %        maxima and minima ("peaks") in the vector V.
  %        MAXTAB and MINTAB consists of two columns. Column 1
  %        contains indices in V, and column 2 the found values.
  %
  %  i.e.
  %  maxtab =
  %  mxpos1 mx1
  %  mxpos2 mx2
  %  mxpos3 mx3
  %  mintab =
  %  mnpos1 mn1
  %  mnpos2 mn2
  %  mnpos3 mn3
  %      
  %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
  %        in MAXTAB and MINTAB are replaced with the corresponding
  %        X-values.
  %
  %        A point is considered a maximum peak if it has the maximal
  %        value, and was preceded (to the left) by a value lower by
  %        DELTA.
  %
  % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
  % This function is released to the public domain; Any use is allowed.
  %
  % TODO: Merge/compare with findpeak/findpeaks function from Ian in private repo?
  
  maxtab = [];
  mintab = [];
  
  v = v(:); % Just in case this wasn't a proper vector
  
  if nargin < 3
    x = (1:length(v))';
  else 
    x = x(:);
    if length(v)~= length(x)
      error('Input vectors v and x must have same length');
    end
  end
    
  if (length(delta(:)))>1
    error('Input argument DELTA must be a scalar');
  end
  
  if delta <= 0
    error('Input argument DELTA must be positive');
  end
  
  mn = Inf; mx = -Inf;
  mnpos = NaN; mxpos = NaN;
  mx_left = -Inf;
  mx_right = Inf;
  mn_left = -Inf;
  mn_right = Inf;
  mxpos_idx = -1;
  mnpos_idx = -1;
  
  lookformax = 1;
  
  for i=1:length(v)
    this = v(i);
    if this > mx, mx = this; mxpos = x(i); mxpos_idx = i; end
    if this < mn, mn = this; mnpos = x(i); mnpos_idx = i; end
    
    if lookformax
      if this < mx-delta
        [ idx_min_left, idx_min_right ] = getSurroundingMins(v, mxpos_idx);
        mx_left = x(idx_min_left);
        mx_right = x(idx_min_right);
        maxtab = [maxtab ; mxpos mx mx_left mx_right];
        mn = this; mnpos = x(i);
        lookformax = 0;
      end  
    else
      if this > mn+delta
        % TODO: create getSurroundingMaxs
        mn_left = mnpos-1;
        mn_right = mnpos+1;
        mintab = [mintab ; mnpos mn mn_left mn_right];
        mx = this; mxpos = x(i);
        lookformax = 1;
      end
    end
  end
end
