function d = findDistance(v1,v2)
  d = sqrt(sum(abs(v2-v1).^2));
end
