%%%%%
%% up-up case
function [mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
  % We should always try to reach delta_max first, since at the end, we will always reach Delta_X anyway.
  % Scaling the taper will keep the slope and ratio constant, but will shift the line along the Y axis (thickness).

  % TODO: final mesh sort? In fact, mesh sorting could be used for all cases instead of inverting an "up-up" to get a "down-down" or glueing together two "up-up" for an up-down.
  % TODO: up-down could be made by sorting in decreasing order, while appending left and right alternatively (just compare to outer limits to add to appropriate side to avoid going below them)
  
  % TODO: Add numeric example for each case.
  % problem:
  % close all; [fig, a1, a2, a3, mymesh] = mesh_smoother(2.2, 1.2, 1, 1.01);
  % -> 0   1   2   3
  
  % general settings:
  %err = 1e-9;
  
  % mini-cases:
  if Delta_X <= delta_0
    disp('Delta_X <= delta_0');
    mymesh = [0, Delta_X];
    solution_id = 0;
    return;
  elseif Delta_X <= delta_max && Delta_X <= ratio_max*delta_0
    disp('Delta_X <= delta_max && Delta_X <= ratio_max*delta_0');
    mymesh = [0, Delta_X];
    solution_id = 1;
    return;
  end
  
  Nt_float = getNToReachThickness(delta_0, delta_max, ratio_max)

  %%% get x_final, t_final for various solutions
  % solution 0: direct taper
  N_0 = floor(Nt_float);
  ratio_0 = ratio_max;
  x_final_0 = getPositionAtN(delta_0, N_0, ratio_0)
  t_final_0 = getThicknessAtN(delta_0, N_0, ratio_0)
  delta_start_0 = delta_0;
  % solution 1: scaled direct taper
  % TODO: check that ratio_1*delta_start_1 > delta_0
  N_1 = ceil(Nt_float);
  ratio_1 = ratio_max;
  x_final_1 = getPositionAtN(delta_0, N_1, ratio_1);
  t_final_1 = getThicknessAtN(delta_0, N_1, ratio_1);
  scaling_factor = delta_max/t_final_1;
  x_final_1 = scaling_factor*x_final_1
  t_final_1 = delta_max
  delta_start_1 = scaling_factor*delta_0;
  % solution 2: solve for alpha
  N_2 = ceil(Nt_float);
  ratio_2 = getAlphaToReachThickness(delta_0, delta_max, N_2);
  x_final_2 = getPositionAtN(delta_0, N_2, ratio_2)
  t_final_2 = getThicknessAtN(delta_0, N_2, ratio_2)
  delta_start_2 = delta_0;

  % choose the fastest rising taper (shortest taper)
  x_final_min = min([x_final_0, x_final_1, x_final_2]);
  
  % set the other properties based on the chosen taper
  if x_final_min == x_final_0 && t_final_0 == delta_max
    disp('use solution 0');
    chosen_taper = 0;
    x_final = x_final_0;
    t_final = t_final_0;
    delta_start = delta_start_0;
    ratio = ratio_0;
    N = N_0;
  elseif x_final_min == x_final_1
    disp('use solution 1');
    chosen_taper = 1;
    x_final = x_final_1;
    t_final = t_final_1;
    delta_start = delta_start_1;
    ratio = ratio_1;
    N = N_1;
  else
    disp('use solution 2');
    chosen_taper = 2;
    x_final = x_final_2;
    t_final = t_final_2;
    delta_start = delta_start_2;
    ratio = ratio_2;
    N = N_2;
  end
  
  if x_final <= Delta_X
    disp('TARGET: thickness');
    % calculate the homogeneous mesh parameters for the rest of the section
    N_homo = floor((Delta_X - x_final)/delta_max)
    homo_start = Delta_X - N_homo*delta_max
    homo = linspace(homo_start, Delta_X, N_homo+1)
    
    % epsilon is the unmeshed part between the current taper and the homogeneous mesh
    epsilon = homo_start - x_final
    
    if epsilon == 0
      disp('epsilon == 0');
      taper = getTaperedMesh_Direct(delta_start, ratio, N);
      %homo = homogeneousMesh(homo_start, Delta_X, delta_max);
      mymesh = [taper, homo(2:end)];
      solution_id = 2;
      return;
    else
      disp('epsilon != 0');
      
      if epsilon >= delta_0
        taper = getTaperedMesh_Direct(delta_start, ratio, N)
        diff(taper)
        %homo = homogeneousMesh(homo_start, Delta_X, delta_max) % TODO: another problem if this leads to a homogeenous delta < delta_0...
        diff(homo)
        mymesh = [taper, homo(1:end)]
        diff(mymesh)
        thickness_list = sort(diff(mymesh))
        mymesh = [0, cumsum(thickness_list)]
        mymesh(end) = Delta_X; % hack for precision
        solution_id = 9;
        return;
      end
      % TODO: if epsilon > delta_0, simply re-order thicknesses
      
      % example for testing:
      % close all; [fig, a1, a2, a3, mymesh] = mesh_smoother(16, 1, 0.1, 2);
      
      % problem if taper only has 1 step (i.e. = [0,A]):
      % close all; [fig, a1, a2, a3, mymesh] = mesh_smoother(30, 1.2, 1, 2);
      
      % Remove last part of taper which should be delta_max (because we are in the case where the taper could reach the target thickness, before the end of the Delta_X section)
      fulltaper = getTaperedMesh_Direct(delta_start, ratio, N)
      diff_fulltaper = diff(fulltaper)
      taper = getTaperedMesh_Direct(delta_start, ratio, N-1)
      diff_taper = diff(taper)
      
      % calculate new "rest" (unmeshed section) (=epsilon+delta_max)
      rest = homo_start - taper(end)
      
      % split the whole thing so that both parts are in the [delta0, delta_max] range.
      % We want:
      %   delta_0 <= splitting_ratio*rest <= delta_max
      %   delta_0 <= (1-splitting_ratio)*rest <= delta_max
      
      disp('ratio must be bigger than:')
      delta_0/rest
      1-(delta_max/rest)
      
      disp('ratio must be smaller than:')
      delta_max/rest
      1-(delta_0/rest)
      
      splitting_ratio_min = max(delta_0/rest, 1-(delta_max/rest))
      splitting_ratio_max = min(delta_max/rest, 1-(delta_0/rest))

      % TODO: handle it. Possible solutions: accept delta < delta_0 and/or try the other possible initial tapers.
      %if splitting_ratio_min > splitting_ratio_max
        %error('unhandled case :(');
      %end
      
      splitting_ratio = (splitting_ratio_min + splitting_ratio_max)/2
      
      thickness_list = [diff(taper), splitting_ratio*rest, (1-splitting_ratio)*rest];

      % Then simply reorder the whole set of thicknesses to have monotonous increase.
      thickness_list = sort(thickness_list)
      
      newtaper = [0, cumsum(thickness_list)]

      %homo = homogeneousMesh(homo_start, Delta_X, delta_max);
      mymesh = [newtaper, homo(2:end)]

      solution_id = 3;
      return;
    end
    
  else
    disp('TARGET: position');
    disp('reach x_max first');
    Nx_sup = ceil(getNToReachPosition(delta_0, Delta_X, ratio_max))
    %Nx_inf = floor(getNToReachPosition(delta_0, Delta_X, ratio_max))
    scaling_factor = Delta_X/getPositionAtN(delta_0, Nx_sup, ratio_max)
    if scaling_factor > 1
      error('This should never happen.');
    elseif scaling_factor >= 1/ratio_max
      disp('scaling time');
      mymesh = getTaperedMesh_Direct(scaling_factor*delta_0, ratio_max, Nx_sup);
      solution_id = 4;
      return;
    else
      disp('need to solve alpha polynomial');
      
      % new problem: close all; [fig, a1, a2, a3, mymesh] = mesh_smoother(2.2, 1.2, 1, 1.01)=(Delta_X, delta_max, delta_0, ratio_max)
      Xinf = getPositionAtN(delta_0, Nx_sup-1, ratio_max) % Nx_inf = Nx_sup-1, because else Delta_X = Xsup, i.e. scaling_factor = 1 >= 1/ratio_max, already handled previously
      if Xinf > Nx_sup*delta_0
        % solve for ratio directly
        % example: [fig, a1, a2, a3, mymesh] = mesh_smoother(2.2, 1.2, 0.1, 1.01)=(Delta_X, delta_max, delta_0, ratio_max)
        [mymesh, ratio_list, ratio, ok] = getAlphaToReachPositionFull(delta_0, Delta_X, Nx_sup, err, ratio_max);
        if ~ok
          error('failed to find ratio in given range');
        end
        mymesh(end) = Delta_X; % hack for precision
        solution_id = 5;
        return;
      else
        % solve for ratio using smaller delta_0 (=delta_0/ratio_max) (TODO: find optimal smaller delta_0)
        [mymesh, ratio_list, ratio, ok] = getAlphaToReachPositionFull(delta_0/ratio_max, Delta_X, Nx_sup, err, ratio_max);
        if ok
          % use found ratio and smaller delta_0
          mymesh(end) = Delta_X; % hack for precision
          solution_id = 6;
          return;
        else
          % use homogeneous mesh
          % calculate delta_sup and delta_inf
          % definition: (delta_inf  = Delta_X/Nh_inf) <= delta_0 <= (delta_sup = Delta_X/Nh_sup)
          Nh_inf = ceil(Delta_X/delta_0)
          Nh_sup = floor(Delta_X/delta_0)
          delta_inf  = Delta_X/Nh_inf
          delta_sup = Delta_X/Nh_sup
          if delta_sup/delta_0 <= ratio_max
            % if delta_sup/delta_0 <= ratio_max, use delta_sup, Nh_sup
            mymesh = linspace(0, Delta_X, Nh_sup+1);
            mymesh(end) = Delta_X; % hack for precision
            solution_id = 7;
            return;
          else
            % else, use delta_inf, Nh_inf
            mymesh = linspace(0, Delta_X, Nh_inf+1);
            mymesh(end) = Delta_X; % hack for precision
            solution_id = 8;
            return;
          end
        end
      end
    end
  end

  error('no solution found');

end

%%%%%

function mymesh = homogeneousMesh(xmin, xmax, spacing_max)
  Ncells = ceil((xmax - xmin)/spacing_max);
  mymesh = linspace(xmin, xmax, Ncells+1);
end

function homo_spacing = homogeneousMeshSpacing()
  Ncells = ceil((xmax - xmin)/spacing_max);
  homo_spacing = (xmax - xmin)/Ncells;
end

function [N, DX, N1, DX1, N2, DX2] = getTaperParameters(spacing_start, spacing_max, ratio_max, DXmax)
  % spacing_max limit
  N1_float = (log(spacing_max/spacing_start))/log(ratio_max);
  N1 = floor(N1_float);

  % DXmax limit
  A = (DXmax/spacing_start)*(ratio_max-1);
  N2_float = log(A+ratio_max)/log(ratio_max) - 1;
  N2 = floor(N2_float);

  N = min(N1, N2);
  
  DX1 = getTaperSize(spacing_start, ratio_max, N1);
  DX2 = getTaperSize(spacing_start, ratio_max, N2);
  DX = getTaperSize(spacing_start, ratio_max, N);
end

function [N, ratio] = getTaperParametersVariableRatio(spacing_start, spacing_max, ratio_max, DXmax)
  N_float = (log(spacing_max/spacing_start))/log(ratio_max);
  N = ceil(N_float);
  ratio = (spacing_max/spacing_start)^(1/N);
end

function DX = getTaperSize(spacing_start, ratio_max, N)
  DX = ( (ratio_max - ratio_max^(N+1))/(1-ratio_max) )*spacing_start;
end

function [mymesh, final_thickness_taper, final_thickness_homo] = getTaperedThenHomogeneousMesh(spacing_start, ratio_max, N, DXmax, spacing_max)
  %mymesh = getTaperedMesh_ForLoop(spacing_start, ratio_max, N);
  mymesh = getTaperedMesh_Direct(spacing_start, ratio_max, N);
  final_thickness_taper = mymesh(end) - mymesh(end-1);
  %    mymesh = getTaperedMesh_LogSpace(spacing_start, ratio_max, N)
  if mymesh(end) < DXmax
    homo = homogeneousMesh(mymesh(end), DXmax, spacing_max);
    final_thickness_homo = homo(end) - homo(end-1);
    mymesh = [mymesh, homo(2:end)];
    %      if length(mymesh)>=2 && DXmax - mymesh(end) < mymesh(end) - mymesh(end-1)
    %        mymesh(end) = (mymesh(end-1) + DXmax)/2;
    %        mymesh(end+1) = DXmax;
    %      else
    %        homo = homogeneousMesh(mymesh(end), DXmax, spacing_max);
    %        mymesh = [mymesh, homo(2:end)];
    %      end
  end
end

function mymesh = getTaperedMesh_LogSpace(spacing_start, ratio_max, N)
  L = logspace(log10(ratio_max*spacing_start), log10(ratio_max^N*spacing_start), N);
  mymesh = [0, cumsum(L)];
end

%%%%%
% utility functions
function ratio = selectRatio(ratio_list, err, ratio_max)
  % Return the biggest real ratio in the ]1 + err, ratio_max] range.
  r = [];
  for i = 1:length(ratio_list)
    %sprintf('%.42f', real(ratio(i)))
    if isreal(ratio_list(i)) && 1+err < real(ratio_list(i))  && real(ratio_list(i)) <= ratio_max
      r(end+1) = real(ratio_list(i));
    end
  end
  ratio = max(r(:));
end

function L = logspace_start_ratio_N(spacing_start, ratio, N)
  % Return a row vector with N elements logarithmically spaced from *spacing_start* to *ratio^(N-1)*spacing_start*.
  L = logspace(log10(spacing_start), log10(ratio^(N-1)*spacing_start), N);
end

function L = logspace_start_end_ratio(delta_min, delta_max, ratio)
  % similar to logspace, but you can specify a maximum ratio instead
  A = log10(delta_min);
  B = log10(delta_max);
  N = ceil( ((B-A)/(log10(ratio))) + 1 );
  L = logspace(A, B, N);
end

%%%%%
% poly solving+selection function
function [mymesh, ratio_list, ratio, ok] = getAlphaToReachPositionFull(delta_0, Delta_X, Nx_sup, err, ratio_max)
  ratio_list = getAlphaToReachPosition(delta_0, Delta_X, Nx_sup)
  ratio = selectRatio(ratio_list, err, ratio_max)
  if length(ratio) ~= 1
    ok = false
    mymesh = []
  else
    ok = true
    mymesh = getTaperedMesh_Direct(delta_0, ratio, Nx_sup)
  end
end

%%%%%
% basic functions solving the set of equations:
%   delta(N) = (ratio^N) * delta_0 <= delta_max
%   x(N) = ( (ratio^(N+1)-ratio)/(ratio-1) ) * delta_0 <= Delta_X
%
% general rule:
%   getPositionAtN(delta_0, N, ratio_max) - getPositionAtN(delta_0, N-1, ratio_max) = getThicknessAtN(delta_0, N, ratio_max)
