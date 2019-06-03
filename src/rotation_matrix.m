function M = rotation_matrix(rotationAng1, rotationAng2, rotationAng3, rotationSequence)
  % returns a rotation matrix for the rotation sequence XYZ (todo: add others)
  % WARNING: designed for column vectors!!!
  % WARNING 2: XYZ are all absolute, i.e. they don't change with rotations!!!
  % WARNING 3: angles in radians!!!
  
  MX = [1,                 0,                  0;...
        0, cos(rotationAng1), -sin(rotationAng1);...
      0, sin(rotationAng1), cos(rotationAng1)];
      
  MY = [cos(rotationAng2), 0, -sin(rotationAng2);...
      0,                 1,                  0;...
        sin(rotationAng2), 0, cos(rotationAng2)];
      
  MZ = [cos(rotationAng3), -sin(rotationAng3), 0;...
      sin(rotationAng3), cos(rotationAng3),  0;...
      0,                 0,                  1];

  M = MZ*MY*MX;

end
