function test_waitbar()
  
  disp('with text');
  N = 10;
  h = waitbarSmart(0,'0%');
  for idx = 0:N
    waitbarSmart(idx/N, h, sprintf('%f%%', 100*idx/N));
    pause(0.1);
  end
  delete(h);
  
  disp('without text');
  N = 10;
  h = waitbarSmart(0);
  for idx = 0:N
    waitbarSmart(idx/N, h);
    pause(0.1);
  end
  delete(h);
end
