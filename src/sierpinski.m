function sierpinski(N,angle,shift,size)
    % sierpinski triangle :)
  if exist('N','var')==0
      N = 1000;
  end
  if exist('angle','var')==0
      angle = 50;
  end
  if exist('shift','var')==0
      shift = 50;
  end
  if exist('size','var')==0
      size = 50;
  end

    height = sqrt(3)/2*size/50;
    corner = [[0,0];[0.5,height];[1,0]];
    P = [0,0];
    plot(corner(:,1),corner(:,2),'r.');
    axis([0,1,0,1]);
    hold on;
  for i=1:N
        triangle = ceil(3*rand());
        xn=P(1);
        yn=P(2);
    if triangle == 1
        P = [0.5 * P(1), 0.5 * P(2)];
  elseif triangle == 2
        P = [0.5 * P(1) + 0.25, 0.5 * P(2) + 0.5*height];
  else
        P = [0.5 * P(1) + 0.5, 0.5 * P(2)];
  end
    plot(P(1),P(2),'b.');
  end
end
