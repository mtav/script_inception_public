function res_rd=ringdown(res,noiseLevel,plots,verbose)
% RINGDOWN analyzes a data trace representing the ringdown of a resonator
%  and returns the frequency and Q values.
% RES_RD=RINGDOWN(RES,NOISELEVEL,PLOTS,VERBOSE)
%
% RES is a structure with the following fields:
%     res.trace1.x
%     res.trace1.y
%  res.trace1 contains the time (in seconds) and amplitude data for a ringdown
%   measurement of a resonator. The data is analyzed using:
%   1) FFT
%   2) Exponential fit to signal envelope
%   3) Minimum Search fit to the ringdown form.
%
% The results are returned in RES_RD in the following fields:
%   res_rd.f0          % the f of the largest peak in the fft (power)
%   res_rd.Q           % the Q determined by exponential fit to the ringdown envelope.
%   res_rd.fit_f0      % the f determined by the best fit to the data.
%   res_rd.fit_Q       % the Q determined by the best fit to the data.
%   res_rd.env_upper   % the upper and lower envelopes for the data set.
%   res_rd.env_lower   %
%
% NOISELEVEL sets a threshold level for the data analysis. Only data for
%   which the amplitude is greater than NOISELEVEL*MAX(data) will be used.
%   Default is 0.1 (i.e., 10%).
% 
% Use PLOTS (0|1|2) and VERBOSE (0|1|2) to set the number of plots and the
%  number of messages.
%
% Example:
%
% >> x = .001:.001:10;
% >> y = 10*sin(20*x).*exp(-1*x);
% >> plot(x,y)
% >> res.trace1.x = x;
% >> res.trace1.y = y;
% >> r = ringdown(res)
% ringdown: Analyzing trace1 as ringdown.
% ringdown: Data sampling interval: 0.001 sec
% ringdown: Raw signal maximum is 9.25621
% ringdown: Discarding first 3 oscillations (start at point 315)
% ringdown: 0/0 outliers removed from envelope
% ringdown: Data after t=2.275 ignored (signal < 0.9)
% ringdown: Min. search function value: 0.001
%
% r = 
% 
%        trace1: [1x1 struct]
%            f0: 3.3241
%             Q: 10.4441
%     env_upper: [1x1 struct]
%     env_lower: [1x1 struct]
%        fit_f0: 3.1832
%         fit_Q: 9.9996
%
%
% Matthew Hopcroft
% mhopeng@ml1.net
%
% Nov2011
% v2.1  fix envelope outlier removal
%       add user constants
% v2.0  bugfixes & code cleanup
%       Thanks to John H. for user feedback
%
% MH May2010
% v1.4  bugfixes; prepare for publication
% v1.3  included minsearch fit
% v1.2  sorted out the isolation of relevant data
% v1.1  integration with res_meas

%% User constants
%  adjust as necessary
skipFirst = 3; % ignore this many initial rings. Must be >= 0
MaxFunEvals = 10000; % max iterations for fitting function
offsetThreshold = 0.01; % subtract offset if greater than this * signal max
envMaxD = 0.3; % remove envelope points with diff > than this * signal max

if nargin < 4, verbose = 2; end
if nargin < 3, plots = 2; end
if nargin < 2 || isempty(noiseLevel), noiseLevel = 0.1; end % ignore data lower than max(signal) * noiseLevel

if plots >= 1, datafig=figure; end

%% Format data
% which trace? Ensure column-wise data
    if isfield(res,'trace1')
        t=res.trace1.x(:); V=res.trace1.y(:);
        if verbose >= 1, fprintf(1,'ringdown: Analyzing trace1 as ringdown.\n'); end
    elseif isfield(res,'trace2')
        t=res.trace2.x(:); V=res.trace2.y(:);
        if verbose >= 1, fprintf(1,'ringdown: Analyzing trace2 as ringdown.\n'); end
    elseif isfield(res,'trace3')
        t=res.trace3.x(:); V=res.trace3.y(:);
        if verbose >= 1, fprintf(1,'ringdown: Analyzing trace3 as ringdown.\n'); end
    elseif isfield(res,'trace4')
        t=res.trace4.x(:); V=res.trace4.y(:);
        if verbose >= 1, fprintf(1,'ringdown: Analyzing trace4 as ringdown.\n'); end
    else
        fprintf(1,'ringdown: Error: no data trace from oscilloscope.\n');
    end
    
% determine sample interval
time_length=t(end)-t(1);
sample_int=time_length/(length(t)-1);
if abs(sample_int-mean(diff(t)))>1e-6
    fprintf(1,'ringdown: Warning: sampling interval calculations do not match: %f %f\n',sample_int,mean(diff(t)));
else
    fprintf(1,'ringdown: Data sampling interval: %g sec\n',sample_int);
end

% check for negative time, discard pre-trigger data
%  (this works if the oscilloscope trigger is set correctly)
if any(sign(t)==-1)
    V=V(sign(t)>=0);
    t=t(sign(t)>=0);
    if verbose >= 2, fprintf(1,'ringdown: Pre-trigger data (t < 0) detected and discarded.\n'); end
end

% signal maximum
Vmax=max(abs(V));
if verbose >= 2, fprintf(1,'ringdown: Raw signal maximum is %g\n',Vmax); end

% remove any offset
Vmean=mean(V);
if Vmean > offsetThreshold*Vmax
    V=V-Vmean; % center data at 0
    if verbose >= 2, fprintf(1,'ringdown: Offset of %+g subtracted.\n',Vmean); end
else
    Vmean=0;
end


% plot data set
if plots >= 2
    figure(datafig);
    hold on;
    h_all=plot(t,V,'.-c'); % plot all data
    title('Ringdown Data'); xlabel('time [sec]'); ylabel('Amplitude');
end


%% Find zero crossings
%  code based on "crossing.m" by Steffen Brueckner
ind0 = find(V==0);
ind1 = find(sign(V(1:end-1).*sign(V(2:end)))<0);
size(ind0);
size(ind1);
indZ = unique([ind0; ind1]);

% skip the first few oscillations
%  (they are sometimes tainted by the release mechanism)
if skipFirst > 0
    if length(indZ)>skipFirst*5
        t=t(indZ(skipFirst):end);
        V=V(indZ(skipFirst):end);
        indZ=indZ(skipFirst:end);
        indZ=indZ-indZ(1)+1;
        if verbose >=2, fprintf(1,'ringdown: Discarding first %d oscillations (start at point %d)\n',skipFirst,indZ(skipFirst)); end
    else
        fprintf(1,'ringdown: WARNING: Number of zero crossings is suspiciously low (<%d)\n',skipFirst*5);
    end
end

% show zero crossings
if plots >= 2
    figure(datafig);
    ha = axis;
    plot(t(indZ),0,'ok'); % show zero crossings
    plot([ha(1) ha(2)],[0 0], '-k'); % plot zero line
end


%% Find envelope
% the envelope is where the signal turns over
% ue and le are index values into V for envelope points
ue = find(diff(sign(diff(V))) < 0) + 1;
le = find(diff(sign(diff(V))) > 0) + 1;
% remove outliers from envelope
if envMaxD > 0
    lengthUE=length(ue); lengthLE=length(le);
    ue(abs(diff(V(ue)))>envMaxD*Vmax)=[];
    le(abs(diff(V(le)))>envMaxD*Vmax)=[];
    if verbose >=2, fprintf(1,'ringdown: %d/%d outliers removed from envelope\n',lengthUE-length(ue),lengthLE-length(le)); end
end

% Use the first portion of the ringdown based on the upper envelope
rexdown = noiseLevel*Vmax; % end of the ringdown slope at 10% of max
if rexdown > 0
    % select envelope points above the threshold
    Vrex=find(V(ue)>rexdown);
    VrexInd=Vrex(end);
    Vfit=V(1:ue(VrexInd));
    tfit=t(1:ue(VrexInd));
    
    %VrexInd
    %size(ue)
    %size(le)
    uelim = min(VrexInd,length(ue))
    lelim = min(VrexInd,length(le))
    
    Vuefit = V(ue(1:uelim)); Vlefit=V(le(1:lelim));
    tuefit = t(ue(1:uelim)); tlefit=t(le(1:lelim));
    if verbose >=2, fprintf(1,'ringdown: Data after t=%g ignored (signal < %.1f)\n',t(ue(VrexInd)),rexdown); end
end

% plot data that will be analyzed
if plots >= 1
    figure(datafig);
    hold on;
    h_select = plot(tfit,Vfit,'.-b'); % plot selected data
    plot(xlim,[rexdown rexdown],'--b')
    plot(xlim,[-rexdown -rexdown],'--b')
    plot(xlim,[0 0], '-k'); % plot zero line
    % plot the envelopes
    if plots >= 2,
        h_envelope=plot(t(ue),V(ue),'.-r',t(le),V(le),'.-g');
    else
        h_envelope=plot(tuefit,Vuefit,'.-r',tlefit,Vlefit,'.-g');
    end
    title('Ringdown Data'); xlabel('time [sec]'); ylabel('Amplitude');
    grid on;
end


%% FFT for frequency estimation
LV = length(Vfit);
P = abs(fft(Vfit)); Ppos=P(1:(round(LV/2)+1));
faxis = 1/sample_int*(0:round(LV/2))/LV;
peakf=faxis(find(Ppos==max(P(1:(round(LV/2)+1))))); %#ok<FNDSB>
if plots >= 2
    fftfig=figure; subplot(1,2,1);
    semilogy(faxis,Ppos,'-'); hold on
    plot(peakf,max(Ppos),'dr');
    title('FFT'); xlabel('Frequency [Hz]'); ylabel('Power')
    fa=axis; text((fa(2)-fa(1))/2,(fa(4)-fa(3))/2,['f_0: ' num2str(peakf,'%.1f') ' Hz']);
end


%% Estimate Q from ringdown
% fit only to a portion of the envelope for Q

% find the linear fit to log envelope
envfitu=polyfit(tuefit,real(log(Vuefit)),1);
envfitl=polyfit(tlefit,real(log(Vlefit)),1);

% extract Q values
Qestu=-pi*peakf/real(envfitu(1));
Qestl=-pi*peakf/real(envfitl(1));
Qest=mean([Qestu Qestl]);

% plot Q estimated results
if plots >= 2
    figure(fftfig); subplot(1,2,2);
    plot(tuefit,real(log(Vuefit)),'.-r'); 
    hold on;
    plot(tlefit,real(log(Vlefit)),'.-g');
    title('Envelope & Log Fit');
    xlabel('Time [sec]'); ylabel('log(Amplitude)');
    legend(['Upper Q: ' num2str(Qestu,'%.1f')],['Lower Q: ' num2str(Qestl,'%.1f')]);

    plot(tuefit,polyval(envfitu,tuefit),'-m');
    plot(tlefit,polyval(envfitl,tlefit),'-c');
    qa=axis; text(0.1*(qa(2)-qa(1))+qa(1),(qa(4)-qa(3))/2+qa(3),['Q: ' num2str(Qest,'%.1f') ' (mean)']);
end

% show results on plot
if plots==1
    figure(datafig);
    legend([h_select; h_envelope(1)],['f_0: ' num2str(peakf,'%.1f') ' Hz'],['Q: ' num2str(Qest,'%.0f')]);
end


%% Fit to the ringdown data

%d is the data used for the exponential fit
d=[tfit Vfit];

% minimum search function for fit to data
rparams(1)=peakf;    % use fft for initial value
rparams(2)=Qest;     % use estimate from exponential fit for initial Q value
rparams(3)=max(Vfit);   % initial amplitude
rparams(4)=0;        % initial phase
rparams(5)=0.01;      % initial value- data is centered at zero
%rparams(5)=mean(Vfit);
%disp(rparams)

options.MaxFunEvals=MaxFunEvals;
if plots >=3, options.PlotFcns=@optimplotx; end
[rfit rfun] = fminsearch(@(p) ringfitD(p,d), rparams, options);
if verbose >= 2, fprintf(1,'ringdown: Min. search function value: %.3f\n   (smaller is better, <1 is good)\n',rfun); end

% plot fit: yfit = amp.*exp(-pi.*freq.*t./Q).*sin(2.*pi.*freq.*t+phi)+yinit;
if plots >= 2
    fitdata = rfit(3).*exp(-pi.*rfit(1).*tfit./rfit(2)).*sin(2*pi.*rfit(1).*tfit+rfit(4))+rfit(5);
    figure(datafig);
    h_minfit=plot(tfit,fitdata,'-m');
    legend([h_all;h_select;h_envelope;h_minfit],'Data','Data for Fit','Upper Env.','Lower Env.','Fit to Data');
end



%% Return results
res_rd=res;
res_rd.f0=peakf;
res_rd.Q=Qest;
res_rd.env_upper.x=tuefit; res_rd.env_upper.y=Vuefit+Vmean;
res_rd.env_lower.x=tlefit; res_rd.env_lower.y=Vlefit+Vmean;
res_rd.fit_f0=rfit(1);
res_rd.fit_Q=rfit(2);



%% function: ringfitD
function sumsq = ringfitD(params,data)
% RINGFITD Fit function for ringdown data
%  Returns the sum of squares of difference between data and fit, using the
%  fit function:
% y=amp*exp(-pi*freq*t/Q)*sin(2*pi*freq*t+phi)+yinitial
%
% DATA should be two columns: time and value
%
% PARAMS is a vector of:
%  freq  Q  amp  phi  yinit
%
t=data(:,1);
y=data(:,2);

yfit = params(3).*exp(-pi.*params(1).*t./params(2)).*sin(2*pi.*params(1).*t+params(4))+params(5);
sumsq = sum((y-yfit).^2);

return
