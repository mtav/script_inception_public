function ret = test_memory(a,b)
  % memory-wasting
  %c = a+b;
  %ret = sum(c(:));
  
  %ret = sum(a(:)+b(:));
  
  ret = foo(a+b);
  pause(15);
end

function ret = foo(x)
  ret = sum(x(:));
end
