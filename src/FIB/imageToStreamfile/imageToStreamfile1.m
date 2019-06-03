function [x,y] = imageToStreamfile1(BW,scanType,scanDir, beamStep)
  switch (scanType)
      case 'oneway'
          switch (scanDir)
              case 'v'
                  [y,x]=find(BW(1:beamStep:end,1:beamStep:end)==1);
                  x=(beamStep*(x-1)+1)';
                  y=(beamStep*(y-1)+1)';
              case 'h'
                  BW=BW';
                  a=BW(1:beamStep:end,1:beamStep:end);
                  [x,y]=find(a==1);
                  x=(beamStep*(x-1)+1)';
                  y=(beamStep*(y-1)+1)';
              otherwise
                  disp('Unknown scan direction.  Use "v" or "h for scan direction"')
                  return;
          end
      case 'twoway'
          [r,c]=size(BW);
          x=[];
          y=[];
          switch (scanDir)
              case 'v'
                  flip=0;
                  for m=1:beamStep:c
                      cc=find(BW(1:beamStep:end,m)==1)';
                      if(mod(m,2)==0)
                          cc=fliplr(cc);
                      end
                      if ~isempty(cc)
                         x=[x,m*ones(1,length(cc))] ;
                         y=[y,beamStep*(cc-1)+1];
                         flip=not(flip);
                      end
                  end
              case 'h'
                  flip=0;
                  for m=1:beamStep:r
                      cc=find(BW(m,1:beamStep:end)==1);
                      if(flip)
                          cc=fliplr(cc);
                          
                      end
                      if ~isempty(cc)
                         y=[y,m*ones(1,length(cc))] ;
                         x=[x,beamStep*(cc-1)+1];
                         flip=not(flip);
                      end
                  end
              otherwise
                  disp('Unknown scan direction.  Use "v" or "h for scan direction"')
                  return;
          end
      otherwise
          disp('Unknown scan method.  Use "oneway" or "twoway for scan method"')
          return;
  end
  
end
