function [x,y,dwell]=ScanIm(IMG,scanType,scanDir, beamStep)

IMG=double(IMG);

switch (scanType)
    case 'oneway'
        switch (scanDir)
            case 'v'
                img=IMG(1:beamStep:end,1:beamStep:end);
                [y,x]=find(img);
                x=(beamStep*(x-1)+1)';
                y=(beamStep*(y-1)+1)';
                c=size(img,1);
                dwell=img(c*(x-1)+y);
            case 'h'
                IMG=IMG';
                img=IMG(1:beamStep:end,1:beamStep:end);
                [y,x]=find(img);
                x=(beamStep*(x-1)+1)';
                y=(beamStep*(y-1)+1)';
                c=size(img,1);
                dwell=img(c*(x-1)+y);
            otherwise
                disp('Unknown scan direction.  Use "v" or "h for scan direction"')
                return;
        end
    case 'twoway'
        x=[];
        y=[];
        dwell=[];
        switch (scanDir)
            case 'v'
                IMG=IMG';
                [r,c]=size(IMG);
                flip=0;
                for m=1:beamStep:c
                    strip=IMG(1:beamStep:end,m);
                    cc=find(strip)';
                    if(mod(m,2)==0)
                        cc=fliplr(cc);
                    end
                    if ~isempty(cc)
                       y=[y,m*ones(1,length(cc))];
                       if (flip)
                           x=[x,fliplr(beamStep*(cc-1)+1)];
                           dwell=[dwell,fliplr(strip(cc)')];
                       else
                           x=[x,beamStep*(cc-1)+1];
                           dwell=[dwell,strip(cc)'];
                       end
                       flip=not(flip);
                    end
                end
            case 'h'
                [r,c]=size(IMG);
                flip=0;
                for m=1:beamStep:r
                    strip=IMG(m,1:beamStep:end);
                    plot(strip);
                    cc=find(strip);
                    if(flip)
                        cc=fliplr(cc);
                    end
                    if ~isempty(cc)
                       x=[x,m*ones(1,length(cc))] ;
                       y=[y,beamStep*(cc-1)+1];
                       dwell=[dwell,strip(cc)];
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
% plot(x,y)