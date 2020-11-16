function handleAxis(activeAxis,...
                    XactiveFullScaleMin, XactiveFullScaleMax, YactiveFullScaleMin, YactiveFullScaleMax,...
                    passiveAxis,...
                    XpassiveFullScaleMin, XpassiveFullScaleMax, YpassiveFullScaleMin, YpassiveFullScaleMax)
                    
    % update passiveAxis limits based on activeAxis limits
    % source: https://uk.mathworks.com/matlabcentral/answers/178247-linkaxes-with-different-x-scales

    activeXLimits   = get( activeAxis, 'XLim' );
    activeXMin      = activeXLimits(1);    
    activeXMax      = activeXLimits(2);    
    
    activeYLimits   = get( activeAxis, 'YLim' );
    activeYMin      = activeYLimits(1);    
    activeYMax      = activeYLimits(2);     
    
    activeXminRatio = (activeXMin - XactiveFullScaleMin) / (XactiveFullScaleMax - XactiveFullScaleMin);
    activeXmaxRatio = (activeXMax - XactiveFullScaleMin) / (XactiveFullScaleMax - XactiveFullScaleMin);   
                            
    activeYminRatio = (activeYMin - YactiveFullScaleMin)/ (YactiveFullScaleMax - YactiveFullScaleMin);
    activeYmaxRatio = (activeYMax - YactiveFullScaleMin)/ (YactiveFullScaleMax - YactiveFullScaleMin);  
    
    passiveXmin =  XpassiveFullScaleMin + activeXminRatio * (XpassiveFullScaleMax - XpassiveFullScaleMin);
    passiveXmax =  XpassiveFullScaleMin + activeXmaxRatio * (XpassiveFullScaleMax - XpassiveFullScaleMin);
    
    passiveYmin =  YpassiveFullScaleMin + activeYminRatio * (YpassiveFullScaleMax - YpassiveFullScaleMin);
    passiveYmax =  YpassiveFullScaleMin + activeYmaxRatio * (YpassiveFullScaleMax - YpassiveFullScaleMin); 
      
    set( passiveAxis, 'XLim', [passiveXmin, passiveXmax]);
    set( passiveAxis, 'YLim', [passiveYmin, passiveYmax]);    
    
end
