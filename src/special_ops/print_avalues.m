function print_avalues(gapmin,gapmax)
  midgap = 0.5*(gapmin+gapmax);
  lambda = 1.55;
  a = midgap*lambda;
  disp(["gapmin(a/lambda) = ",num2str(gapmin)]);
  disp(["gapmax(a/lambda) = ",num2str(gapmax)]);
  disp(["midgap(a/lambda) = ",num2str(midgap)]);
  disp(["lambda (mum) = ",num2str(lambda)]);
  disp(["a (mum) = midgap*lambda = ",num2str(a)]);
end
