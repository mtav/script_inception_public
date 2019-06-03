function [fig, a1, a2, a3, mymesh] = mesh_smoother(varargin)
    %function [fig, a1, a2, a3, mymesh] = mesh_smoother(xmin, xmax, spacing_left, spacing_max, spacing_right , ratio_max)

    % TODO: check that scaled taper + homo solves all remaining problems (monotonous thickness change => scaling_factor inequalities)
    % TODO: create final mesh checker function
    
    %delta_0 = varargin{1}
    %ratio = varargin{2}
    %N = varargin{3}
    %scaling_factor = varargin{4}
    % mesh_smoother(delta_0, ratio, N, scaling_factor)
    %m = getTaperedMesh_Direct(delta_0, ratio, N)
    
    
    %delta_0 =  1
    %delta_max =  2
    %ratio_max =  1.2000
    %Delta_X =  5

    %% solution_id = 0
    %delta_0 = 1; delta_max = 2; ratio_max = 1.2; Delta_X = 0.2; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id = 1
    %delta_0 = 1; delta_max = 2; ratio_max = 1.2; Delta_X = 1.2; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id = 2
    %delta_0 = 1; delta_max = 2^4; ratio_max = 2; Delta_X = ratio_max + ratio_max^2 + ratio_max^3 + ratio_max^4; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id = 3
    %delta_0 = 1; delta_max = 2; ratio_max = 1.2; Delta_X = 7; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id = 4
    %delta_0 = 1; delta_max = 8; ratio_max = 2; Delta_X = 8; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id =  5
    %delta_0 = 1; delta_max = 2; ratio_max = 1.2; Delta_X = 5; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id =  5
    %delta_0 = 0.1; delta_max = 1.2; ratio_max = 1.01; Delta_X = 2.2; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id =  5
    %delta_0 = 1; delta_max = 2; ratio_max = 1.2; Delta_X = 5; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id =  6
    %delta_0 = 1; delta_max = 1.2; ratio_max = 1.01; Delta_X = 2; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id = 7
    %delta_0 = 1; delta_max = 1.2; ratio_max = 1.01; Delta_X = 2.45; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %% solution_id = 8
    %delta_0 = 1; delta_max = 1.2; ratio_max = 1.01; Delta_X = 2.2; err = 0;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %%% failure debugging
    
    delta_0 = 1; delta_max = 1.2; ratio_max = 1.17; Delta_X = 4; err = 1e-9;
    [mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    %delta_0 = 1; delta_max = 1.2; ratio_max = 1.15; Delta_X = 4.62; err = 1e-9;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)

    fig = ''; a1 = ''; a2 = ''; a3 = '';
    xmin = 0
    xmax = Delta_X
    spacing_left = delta_0
    spacing_max = delta_max
    spacing_right = delta_max
    ratio_used = ratio_max
    [fig, a1, a2, a3] = plotMesh(fig, a1, a2, a3, mymesh, xmin, xmax, spacing_left, spacing_max, spacing_right, ratio_used, ratio_max)
    %[fig, a1, a2, a3] = plotMesh({fig, a1, a2, a3, mymesh, xmin, xmax, spacing_left, spacing_max, spacing_right, ratio_used, ratio_max});


    % should be solution_id=2, but due to precision errors, is = 3
    %delta_0 = 1; delta_max = 1.2^4; ratio_max = 1.2; Delta_X = 1.2 + 1.2^2 + 1.2^3 + 1.2^4; err = 1e-9;
    %% solution_id = 4
    %delta_0 = 1; delta_max = 2; ratio_max = 1.2; Delta_X = 4; err = 1e-9;
    %% solution_id = 4
    %delta_0 = 1; delta_max = 4; ratio_max = 2; Delta_X = 4; err = 1e-9;
    %% solution_id = 4
    %delta_0 = 1; delta_max = 4; ratio_max = 1.2; Delta_X = 8; err = 1e-9;
    %% solution_id = 8 if err=1e-9 and 6 if err=0, but solution 6 is incorrect, because found alpha is too close to 1 and there really is no alpha>1 solution.
    %delta_0 = 1; delta_max = 1.2; ratio_max = 1.01; Delta_X = 2.3; err = 1e-9;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)
    %% solution_id =  8
    %delta_0 = 1; delta_max = 1.2; ratio_max = 1.01; Delta_X = 2.5; err = 1e-9;
    %[mymesh, solution_id] = solveUpUpCase(delta_0, delta_max, ratio_max, Delta_X, err)
    %check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)
    return;

    % mesh_smoother(Delta_X,delta_max,delta_0,ratio_max,err)
    Delta_X = varargin{1}
    delta_max = varargin{2}
    delta_0 = varargin{3}
    ratio_max = varargin{4}
    err = varargin{5}
    custom_mesh = varargin{6}
    [mymesh, solution_id] = solveUpUpCase(varargin)
    check_results = checkMeshUpUp(mymesh, delta_0, delta_max, ratio_max, Delta_X, err)
    check_results = checkMeshUpUp(custom_mesh, delta_0, delta_max, ratio_max, Delta_X, err)
    return;
    
    mmm = getTaperedMesh_Direct(0.1, 2, -2)
    length(mmm)
    mm = getTaperedMesh_Direct(0.1, 2, -1)
    length(mm)
    m0 = getTaperedMesh_Direct(0.1, 2, 0)
    length(m0)
    m1 = getTaperedMesh_Direct(0.1, 2, 1)
    length(m1)
    m2 = getTaperedMesh_Direct(0.1, 2, 2)
    length(m2)
    return
    
    %ms = getTaperedMesh_Direct(scaling_factor*delta_0, ratio, N)
    %ms2 = scaling_factor*m
    
    %delta_max = m(end) - m(end-1);
    %beta = (ratio-1)/ratio;
    %dx1 = (1-scaling_factor)*(delta_max-delta_0)/beta
    %dx2 = m(end)-ms(end)
    %dx3 = m(end)-ms2(end)
    %return
    
    %ratio = test_getAlphaToReachThickness(varargin)
    %N = test_getNToReachThickness(varargin);
    %ratio = test_getAlphaToReachPosition(varargin)
    %N = test_getNToReachPosition(varargin)
    %[fig, a1, a2, a3] = plotMesh(varargin);

    %delta_0 = varargin{1}
    %delta_max = varargin{2}
    %ratio = varargin{3}

    %N = getNToReachThickness(delta_0, delta_max, ratio)
    %ratio = getAlphaToReachThickness(delta_0, delta_max, floor(N))
    %ratio = getAlphaToReachThickness(delta_0, delta_max, ceil(N))
    %return

    %m = getTaperedMesh_Direct(0.2, 1.2, 0)
    %size(m)
    %return
    
    mymesh = solveUpUpCase(varargin)
    diff(mymesh)
    [direct_ratio, normalized_ratio] = getThicknessRatios(mymesh)

    fig = ''; a1 = ''; a2 = ''; a3 = '';

    Delta_X = varargin{1}
    delta_max = varargin{2}
    delta_0 = varargin{3}
    ratio_max = varargin{4}

    xmin = 0
    xmax = Delta_X
    spacing_left = delta_0
    spacing_max = delta_max
    spacing_right = delta_max
    ratio_used = ratio_max
    %ratio_max
    [fig, a1, a2, a3] = plotMesh({fig, a1, a2, a3, mymesh, xmin, xmax, spacing_left, spacing_max, spacing_right, ratio_used, ratio_max});

    return

    Delta_X = varargin{1}
    delta_max = varargin{2}
    delta_0 = varargin{3}
    ratio_max = varargin{4}

    xmin = 0;
    xmax = Delta_X;
    spacing_left = delta_0;
    spacing_max = delta_max;
    spacing_right = delta_max;
    ratio_used = ratio_max;
    ratio_max = ratio_max;

    fig = ''; a1 = ''; a2 = ''; a3 = '';
    [fig, a1, a2, a3] = plotMesh({fig, a1, a2, a3, mymesh, xmin, xmax, spacing_left, spacing_max, spacing_right, ratio_used, ratio_max});

    
    return

    Delta_X = xmax - xmin;
    delta_max = spacing_max;
    delta_0 = spacing_left;

    % mymesh = mesh_smoother(xmin, xmax, spacing_left, spacing_max, spacing_right , ratio_max)

    % default return value
    %mymesh = [xmin, xmax];


    %ratio_used = 1+(ratio_max-1)/2;

    %ratio = ratio_max

    %position = getPositionAtN(delta_0, N, ratio)
    %thickness = getThicknessAtN(delta_0, N, ratio)
    %%delta_0
    %%Delta_X
    %%N
    %%ratio = 1.64244

    %%mymesh = getTaperedMesh_ForLoop(0.1, 2, 5)
    %%return

    %mymesh1 = getTaperedMesh_ForLoop(spacing_max, ratio_max, N)
    %size(mymesh1)
    %mymesh2 = getTaperedMesh_Direct(delta_0, ratio_used, N)
    %size(mymesh2)
    
    %% reaching the target thickness
    %% N
    %N = getNToReachThickness(delta_0, delta_max, ratio)
    
    return

    % reaching the target position
    % N
    N = getNToReachPosition(delta_0, Delta_X, ratio)
    % ratio
    ratio = getAlphaToReachPosition(delta_0, Delta_X, N)
    ratio = selectRatio(ratio, 0, ratio_max)
    fig = ''; a1 = ''; a2 = ''; a3 = '';
    mymesh = getTaperedMesh_ForLoop(spacing_max, ratio_max, N)
    [fig, a1, a2, a3] = plotMesh(fig, a1, a2, a3, mymesh2, spacing_left, spacing_right, spacing_max, ratio_max, ratio_used);
    
    %[fig, a1, a2, a3] = plotMesh(fig, a1, a2, a3, mymesh1, spacing_left, spacing_right, spacing_max, ratio_max, ratio_used);
    %[fig, a1, a2, a3] = plotMesh(fig, a1, a2, a3, mymesh2, spacing_left, spacing_right, spacing_max, ratio_max, ratio_used);

    %fig = ''; a1 = ''; a2 = ''; a3 = '';
    %mymesh1 = getTaperedMesh_ForLoop(spacing_max, ratio_used, 3)
    %[fig, a1, a2, a3] = plotMesh(fig, a1, a2, a3, mymesh1, spacing_left, spacing_right, spacing_max, ratio_max, ratio_used);    
    %%fig = ''; a1 = ''; a2 = ''; a3 = '';
    %mymesh2 = getTaperedMesh_ForLoop(2*spacing_max, 2*ratio_used, 5)
    %[fig, a1, a2, a3] = plotMesh(fig, a1, a2, a3, mymesh2, 2*spacing_left, 2*spacing_right, 2*spacing_max, 2*ratio_max, 2*ratio_used);

    return

    % case 1
    if spacing_max <= spacing_left*ratio_max && spacing_max <= spacing_right*ratio_max
        disp('down-up');
        mymesh = homogeneousMesh(xmin, xmax, spacing_max);
    % case 2
    elseif spacing_max <= spacing_left*ratio_max && spacing_max > spacing_right*ratio_max
      disp('down-down');

      [N, DX, N1, DX1, N2, DX2] = getTaperParameters(spacing_right, spacing_max, ratio_max, xmax-xmin);
      tapered_mesh = getTaperedThenHomogeneousMesh(spacing_right, ratio_max, N, xmax-xmin, spacing_max);
      mymesh = fliplr( xmax - tapered_mesh );
      if ~checkMeshDeltaDecreasesOnly(mymesh)
        warning('bad mymesh smoothing');
      end

    % case 3
    elseif spacing_max > spacing_left*ratio_max && spacing_max <= spacing_right*ratio_max
      disp('up-up');
      
      % TOFIX: mymesh = mesh_smoother(0, 2.8, 0.1, 1, 1, 2); -> bad mymesh smoothing
      %        mymesh = mesh_smoother(0, 2.8, 0.1, 1, 2, 1.5); -> works, proving that alpha can be changed to allow for a better mesh
      
      [N, ratio_used] = getTaperParametersVariableRatio(spacing_left, spacing_max, ratio_max, xmax-xmin)
      tapered_mesh = getTaperedThenHomogeneousMesh(spacing_left, ratio_used, N, xmax-xmin, spacing_max);
      
%        [N, DX, N1, DX1, N2, DX2] = getTaperParameters(spacing_left, spacing_max, ratio_max, xmax-xmin);
%        tapered_mesh = getTaperedThenHomogeneousMesh(spacing_left, ratio_max, N, xmax-xmin, spacing_max);

      mymesh = xmin + tapered_mesh;
      if ~checkMeshDeltaIncreasesOnly(mymesh)
        warning('bad mymesh smoothing');
      end
    
    % case 4
    elseif spacing_max > spacing_left*ratio_max && spacing_max > spacing_right*ratio_max
      disp('up-down');
      [N_left, DX_left, N1_left, DX1_left, N2_left, DX2_left] = getTaperParameters(spacing_left, spacing_max, ratio_max, xmax-xmin);
      [N_right, DX_right, N1_right, DX1_right, N2_right, DX2_right] = getTaperParameters(spacing_right, spacing_max, ratio_max, xmax-xmin);
      x_left = xmin + DX_left
      x_right = xmax - DX_right
      
      if x_left == x_right
        tapered_mesh_left = getTaperedThenHomogeneousMesh(spacing_left, ratio_max, N_left, xmax-xmin, spacing_max)
        tapered_mesh_right = getTaperedThenHomogeneousMesh(spacing_right, ratio_max, N_right, xmax-xmin, spacing_max)
        mesh_left = xmin + tapered_mesh_left
        mesh_right = fliplr( xmax - tapered_mesh_right )
        mymesh = [mesh_left, mesh_right(2:end)]
        
      elseif x_left < x_right
        error('not yet handled');
      else
        error('not yet handled');
      end
      
      
    else
      error('should not happen');
    end

    plotMesh(mymesh, spacing_left, spacing_right, spacing_max, ratio_max, ratio_used);

    mymesh
    diff(mymesh)
end

%%%%%
%% test functions

function ratio = test_getAlphaToReachThickness(varargin)
  delta_0 = varargin{1}{1}
  delta_max = varargin{1}{2}
  N = varargin{1}{3}

  ratio = getAlphaToReachThickness(delta_0, delta_max, N)
  fig = ''; a1 = ''; a2 = ''; a3 = '';
  mymesh = getTaperedMesh_ForLoop(delta_0, ratio, N);

  xmin = 0;
  xmax = 10;
  spacing_left = delta_0;
  spacing_max = delta_max;
  spacing_right = delta_max;
  ratio_used = ratio;
  ratio_max = ratio;

  [fig, a1, a2, a3] = plotMesh({fig, a1, a2, a3, mymesh, xmin, xmax, spacing_left, spacing_max, spacing_right, ratio_used, ratio_max})

  mymesh
  diff(mymesh)
end

function N = test_getNToReachThickness(varargin)
  delta_0 = varargin{1}{1}
  delta_max = varargin{1}{2}
  ratio = varargin{1}{3}

  N = getNToReachThickness(delta_0, delta_max, ratio)
  fig = ''; a1 = ''; a2 = ''; a3 = '';
  mymesh = getTaperedMesh_ForLoop(delta_0, ratio, N);

  xmin = 0;
  xmax = 10;
  spacing_left = delta_0;
  spacing_max = delta_max;
  spacing_right = delta_max;
  ratio_used = ratio;
  ratio_max = ratio;

  [fig, a1, a2, a3] = plotMesh({fig, a1, a2, a3, mymesh, xmin, xmax, spacing_left, spacing_max, spacing_right, ratio_used, ratio_max})

  mymesh
  diff(mymesh)
end

function ratio = test_getAlphaToReachPosition(varargin)
  delta_0 = varargin{1}{1}
  Delta_X = varargin{1}{2}
  N = varargin{1}{3}
  err = varargin{1}{4}
  ratio_max = varargin{1}{5}

  ratio_list = getAlphaToReachPosition(delta_0, Delta_X, N)
  ratio = selectRatio(ratio_list, err, ratio_max)
  
  fig = ''; a1 = ''; a2 = ''; a3 = '';
  mymesh = getTaperedMesh_ForLoop(delta_0, ratio, N);

  spacing_left = delta_0;
  spacing_right = Delta_X;
  spacing_max = Delta_X;
  ratio_max = ratio;
  ratio_used = ratio;

  [fig, a1, a2, a3] = plotMesh({fig, a1, a2, a3, mymesh, xmin, xmax, spacing_left, spacing_max, spacing_right, ratio_used, ratio_max})

  mymesh
  diff(mymesh)
end

function N = test_getNToReachPosition(varargin)
  delta_0 = varargin{1}{1}
  Delta_X = varargin{1}{2}
  ratio = varargin{1}{3}

  N = getNToReachPosition(delta_0, Delta_X, ratio)
  
  fig = ''; a1 = ''; a2 = ''; a3 = '';
  mymesh = getTaperedMesh_ForLoop(delta_0, ratio, N);
  
  xmin = 0
  xmax = Delta_X
  spacing_left = delta_0;
  spacing_max = Delta_X;
  spacing_right = Delta_X;
  ratio_used = ratio;
  ratio_max = ratio;

  [fig, a1, a2, a3] = plotMesh({fig, a1, a2, a3, mymesh, xmin, xmax, spacing_left, spacing_max, spacing_right, ratio_used, ratio_max})

  mymesh
  diff(mymesh)
end
