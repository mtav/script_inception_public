function ret = getUelement(M, p, z, zp, c)
  ret = 0;
  for n = 0:M
    for np = 0:M
      ret += (zp/z)^n*c(n+np+p+1)*zp^(-(n+np));
    end
  end
end

%p=0,1,2

%n+np+p+1
%=M+M+2+1
