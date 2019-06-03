function ret = myfunc2(t, d0, d1, d2, w0, w1, w2)
  ret = d0*exp(-w0*i*t) + d1*exp(-w1*i*t) + d2*exp(-w2*i*t);
end
