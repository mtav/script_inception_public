function range_string = xlRange(data, nRowStart, nColStart)
  nRowEnd = nRowStart + size(data, 1) - 1;
  nColEnd = nColStart + size(data, 2) - 1;
  
  function ret = div(A,B)
    ret = idivide(int32(A),int32(B));
  end

  function alphaID = num2alpha(numID)
    if numID < 27
      alphaID = char(double('A') + (numID-1) );
    else
      alphaID = strcat(char(double('A') + (div(numID-1, 26) - 1)), char(double('A') + mod(numID-1, 26) ));
    end
  end
  
  range_string = [num2alpha(nColStart), num2str(nRowStart), ':', num2alpha(nColEnd), num2str(nRowEnd)];
  
end
