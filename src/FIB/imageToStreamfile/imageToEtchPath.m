function [x, y] = imageToEtchPath(BW, beamStep, direction, etchType, param0)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
  %
  %       ERMAN ENGIN
  %       UNIVERSSITY OF BRISTOL
  %
  % Modified by Mike Taverne
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
  % This code generates a FIB etch paths from a given B&W image matrix.
  %
  % if etchType is 'rough' param0 is the initialShrink
  % else param0 is the number of fine etch contours.
  % direction: Etch direction:
  %              1: Inner to Outer
  %              0: Outer to Inner
  % options: bwboundaries() options argument: 'holes' or 'noholes'
  %
  
  %options = 'noholes';
  options = 'holes';
  
  boundaries={};
  
  if (strcmp(etchType,'fine'))
    BW2 = BW;
  else
    pen = strel('disk', round(param0));
    BW2 = imerode(BW, pen);
  end
  
  pen = strel('disk', round(beamStep));
  
  i = 1;
  while (nnz(BW2))
    [B] = bwboundaries(BW2, options);
    
    %imshow(BW2);
    %hold on;
    %for k = 1:length(B)
      %boundary = B{k};
      %plot(boundary(:,2), boundary(:,1), 'b', 'LineWidth', 2)
    %end
    %pause
    
    lengths = zeros(1, size(B,1));
    for m = 1:size(B)
      lengths(m) = length(B{m});
    end
    boundaries{i} = B{find(lengths==max(lengths))};
    
    if (strcmp(etchType,'fine') && (i>param0))
      break;
    end
    
    %    hold off;
    %    imagesc(BW2')
    %    hold on
    % %    
    %    boundary=boundaries{i};
    %    x=boundary(:,1);
    %    y=boundary(:,2);
    %    plot(x,y);
       
    BW2 = imerode(BW2, pen);
    %    imagesc(BW2)
    %    pause(.5)
    i = i + 1;
    %    
     
  end
  
  x=[];
  y=[];
  boundary=[];
  for i=1:length(boundaries)
      boundary=boundaries{i};
      y=[y,boundary(:,1)'];
      x=[x,boundary(:,2)'];
  end
  
  if (direction)
      x=fliplr(x);
      y=fliplr(y);
  end
end
