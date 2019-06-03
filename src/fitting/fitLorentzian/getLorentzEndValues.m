function [x0, y0, A, w] = getLorentzEndValues(x,yOrig, vStart, VERBOSE)
  % function [x0, y0, A, w] = getLorentzEndValues(x,yOrig, vStart)
  % Fits with a function of the form:
  % y=y0+(2*A/pi).*(w./(4*(x-x0).^2+w.^2));
  % gamma = w/2
  % vStart = [x0, y0, A, w]

  % maximum = 2*A/(pi*w)
  % FWHM = w
  % Quality factor:
  % Q = x0/FWHM = v(1)/v(4)

  % function [y]=lorentz2(v,x)
    % x0=v(1);
    % y0=v(2);
    % A=v(3);
    % w=v(4);
    % y=y0+(2*A/pi).*(w./(4*(x-x0).^2+w.^2));
  % end

  if exist('VERBOSE','var')==0
    disp('VERBOSE not given');
      VERBOSE = 1;
  end
  
  % make sure all vectors are column vectors
  x = x(:);
  yOrig = yOrig(:);
  
  %% default arguments
  if nargin<3
    % x0=7;
    % y0=2.5;
    % A=5;
    % w=4;
    [x0,y0,A,w] = getLorentzStartValues(x,yOrig,0);
    vStart = [x0,y0,A,w];
  end
  
  %% define start point
  % vStart=[y0,A,w,x0];
  if VERBOSE==1
    fprintf('Start:  x0=%E y0=%E  A=%E  w=%E \n',vStart(1),vStart(2),vStart(3),vStart(4));
  end

  %% fit using nlinfit
  
  % size(x)
  % size(yOrig)
  % size(vStart)
  
  vEnd = nlinfit(x,yOrig,@lorentz,vStart);
  if VERBOSE==1
    fprintf('End: x0=%E y0=%E  A=%E  w=%E \n',vEnd(1),vEnd(2),vEnd(3),vEnd(4)); 
  end
  
  x0=vEnd(1);
  y0=vEnd(2);
  A=vEnd(3);
  w=vEnd(4);

  % plotting
  % figure;
  % plot(x,yOrig,'ob');
  % hold on;

  % yStart=lorentz(vStart,x);
  % plot(x,yStart,'-r');
  
  % yEnd=lorentz(vEnd,x);
  % plot(x,yEnd,'-g');
  % legend('Orig','Start','End');
  % set(gca,'Color',[0.7,0.7,0.7]);
  % set(gcf,'Color',[1,1,1]);

end
