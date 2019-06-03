function [Mesh_ThicknessVector,Section_FinalDeltaVector] = subGridMultiLayer(Section_MaxDeltaVector,Section_ThicknessVector)
  % Create a list of thicknesses for meshing
    %
  % [Mesh_ThicknessVector,Section_FinalDeltaVector] = subGridMultiLayer(Section_MaxDeltaVector,Section_ThicknessVector)
    % Section_ThicknessVector = list of the thickness of each section
    % Section_MaxDeltaVector = list of maximum allowed deltas in each section
  % Mesh_ThicknessVector = thickness vector of the mesh
  % Section_FinalDeltaVector = list of final deltas used in the mesh
    %
  % ex:
  % Mesh_ThicknessVector = [ 3,2,2,1,1,1 ]
  % Section_FinalDeltaVector = [ 3,2,1 ]
    %
    % Note: If you are switching from the old to the new subGridMultiLayer version, replace:
    %  Section_MaxDeltaVector(new) = lambda(old)/16./indexVector(old)
    %  Section_ThicknessVector(new) = thicknessVector(old)
    

  if (nargin==0)
    Section_MaxDeltaVector = [1.76, 2.1385, 2.3535, 1];
    Section_ThicknessVector = [1, 0.5, 1, 1];
  end
  
  if( size(Section_MaxDeltaVector) ~= size(Section_ThicknessVector) )
    disp('FATAL ERROR: The 2 input vectors do not have the same size.');
    return
  end

  totalHeight = sum(Section_ThicknessVector);

  nLayers = length(Section_ThicknessVector);

  nCellsV = ceil( Section_ThicknessVector ./ Section_MaxDeltaVector );
  Section_FinalDeltaVector = Section_ThicknessVector ./ nCellsV;

  Mesh_ThicknessVector = [];
  for m=1:nLayers
    Mesh_ThicknessVector = [Mesh_ThicknessVector,Section_FinalDeltaVector(m)*ones(1,nCellsV(m))];
  end
end
