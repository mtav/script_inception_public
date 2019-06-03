function HHgraph(fcn)

%demo of user interface construction
%this function CALLS ITSELF via GUI callbacks

% By default make the GUI
%This code detects the first entry into the function
%from the command line with no parameters
if nargin == 0
   fcn = 'makeGUI';
end

%This is the main decision point of the function.
%The switch statement is executed once-per-fuction call
switch fcn
   
   %This code is executed ONCE when the function enters with
   %no arguments
case 'makeGUI'
   
   % Determine the name of this function and store it in the
   %figure plotinfo variable.
   %Since variables used in a function are not persistent after
   %the function exits we will need to store the state-variables
   %in a data structure associated with the persistent Figure-window.
   %The plotinfo sturcture will be saved into the Figure's UserData
   %area and retrieved from there as necessary.
   plotinfo.myname = mfilename;
   
   % ===Create main figure==========================
   fig = figure('Position',centerfig(660,630),...
      'Resize','off',...
      'NumberTitle','off',...
      'Name','Hodgkin-Huxley model',...
      'Interruptible','off',...
      'Menubar','none',...
      'Color',get(0,'DefaultUIControlBackgroundColor'));
   
   %===Header text===================================
   uicontrol(gcf,'Style','text', ...
      'String','HH model--A simple GUI example',...
      'fontsize',15, ...
      'HorizontalAlignment','Center',...
      'Position',[100,590,320,30],...
      'BackgroundColor',[0.8 1 0.8]);
   
   % ===Create axes=================================
   plotinfo.ax = axes('Units','pixels',...
      'Position',[235 165 395 360],...
      'Box','on',...
      'XLim',[0 50],'YLim',[-50 150]);
   xlabel('t (msec)'); ylabel('v (mV)');
   
   % ===The quit button===============================
   uicontrol('Style','pushbutton',...
      'Position',[595 595 45 25],...
      'String','Quit',...
      'Interruptible','off',...
      'BusyAction','cancel',...
      'Callback',[plotinfo.myname,' quit']);
   
   %==Current slider=========================== 
   plotinfo.freq=10.0;
   plotinfo.s1 = uicontrol(gcf,'Style','text', ...
      'String','current',...
      'fontsize', 12, ...
      'Position',[10,240,100,20],...
      'BackgroundColor',[0.8,0.8,0.8]);
   plotinfo.s2 = uicontrol(gcf,'Style','text',...
      'String',num2str(plotinfo.freq),...
      'Position',[110,240,50,20],...
      'BackgroundColor',[0.8,0.8,0.8]);
   plotinfo.s3 = uicontrol(gcf,...
      'Style','slider',...
      'Min' ,-20,'Max',20, ...
      'Position',[10,220,150,20], ...
      'Value', 10,...
      'SliderStep',[0.01 0.1], ...
      'BackgroundColor',[0.8,0.8,0.8],...
      'CallBack', [plotinfo.myname,' setfreq']);
   
   %==Draw button===========================
   uicontrol(gcf,'Style','Pushbutton', ...
      'String','Compute',...
      'Position',[10,450,70,20],...
      'BackgroundColor',[0.8,0.8,0.8], ...
      'CallBack',[plotinfo.myname,' draw'] );
   
   %put all the variables in a safe place (the figure's data area)
   set(fig,'UserData',plotinfo);
   
case 'draw'
   x=0:0.01:1;
   amp=1.0;
   %Get data from the figure's data area
   plotinfo=get(gcf,'UserData');   
   y=amp*sin(2*pi*plotinfo.freq*x);
   %plot(x,y,'black');
   HH(plotinfo.freq)
   
case 'quit'
   fig = gcf;
   quit_reply = questdlg('Really quit HHgraph?');
   if strcmp(quit_reply,'Yes')
      close(fig);
   end
   
case 'setfreq'
   %Get data from the figure's data area
   plotinfo=get(gcf,'UserData'); 
   %Get the value from the slider
   plotinfo.freq=get(plotinfo.s3,'Value');
   %Update the text which shows the slider value
   set(plotinfo.s2,'String',plotinfo.freq);
   %Store the new slider value back into the figure's data area
   set(gcf,'UserData',plotinfo);
   
end
return

%===A utility to center the window on the screen============
function pos = centerfig(width,height)
% Find the screen size in pixels
screen_s = get(0,'ScreenSize');
pos = [screen_s(3)/2 - width/2, screen_s(4)/2 - height/2, width, height];
return

%===Comopute the HH model====================================
function HH(current)
%----------------------------------------------------------------------
% Physiology 317 - Methods in Computational Neurobiology
% hw3p2.m - Homework #3, Problem #2
% HODGKIN-HUXLEY: Response of Squid Axon to Current Injection
% M. Nelson  1995, 1997
%
%Slightly modified by BRL to be a function which plots
%a result for one current
%----------------------------------------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%
% INITIALIZATION
%%%%%%%%%%%%%%%%%%%%%%%
DT = 0.025;
TMAX = 50;
t = 0:DT:TMAX;

VREST = 0.0;

GNA = 120.0;	% mS/cm^2
GK = 36.0;	% mS/cm^2
GLEAK = 0.3;	% mS/cm^2

ENA = 115.0;	% mV
EK = -12.0;	% mV
ELEAK = 10.613;	% mV

C_M = 1.0;	% uF/cm^2

INJECT_LIST = [current];

for ival = 1

    I = INJECT_LIST(ival)*(t>5 & t<=30);

    %%%%%%%%%%%%%%%%%%%%%%%
    % MAIN SIMULATION LOOP
    %%%%%%%%%%%%%%%%%%%%%%%

    clear v  m  h  n				% clear old varibles
    v = VREST;					% initial membrane voltage
    m = alpha_m(v)/(alpha_m(v)+beta_m(v));	% initial (steady-state) m
    h = alpha_h(v)/(alpha_h(v)+beta_h(v));	% initial (steady-state) h
    n = alpha_n(v)/(alpha_n(v)+beta_n(v));	% initial (steady-state) n

    for i=2:length(t)

	M = m(i-1);	% get values from last time step
	H = h(i-1);	% (hopefully this substitution makes 
	N = n(i-1);	% the following code a bit easier to read)
	V = v(i-1);

	gNa = GNA * M^3 * H;
	gK  = GK  * N^4;

	mdot = alpha_m(V)*(1-M) - beta_m(V)*M;
	hdot = alpha_h(V)*(1-H) - beta_h(V)*H;
	ndot = alpha_n(V)*(1-N) - beta_n(V)*N;
	vdot = (I(i-1) - gNa*(V-ENA) - gK*(V-EK) - GLEAK*(V-ELEAK))/C_M;

	m(i) = m(i-1) + mdot*DT;		% Euler integration
	h(i) = h(i-1) + hdot*DT;
	n(i) = n(i-1) + ndot*DT;
	v(i) = v(i-1) + vdot*DT;
    end
    
    cla
    hold on
    plot(t,v,'b-');
    plot(t,I,'r:')
    str = sprintf('Inject = %2.2f \\muA/cm^2',INJECT_LIST(ival));
    title(str);
end
return

function rate = alpha_h(v)
rate = zeros(size(v));
rate = 0.07*exp(-v/20.0);
return

function rate = beta_h(v)
rate = zeros(size(v));
rate =  1.0 ./ (exp((-v+30.0)/10.0) + 1.0);
return

function rate = alpha_m(v)
rate = zeros(size(v));		% DEFAULT RATE TO ZERO     
idx = find(v~=25.0);			% HANDLE NORMAL (NON-SINGULAR) CASE
if(~isempty(idx))
   rate(idx) = 0.1*(-v(idx)+25.0) ./ (exp((-v(idx)+25.0)/10.0)-1.0);
end
idx = find(v == 25.0);		% HANDLE SIGULARITY AT V=25.0 
if(~isempty(idx))
   rate(idx) = 1.0/exp((-v(idx)+25.0)/10.0);
end
return

function rate =  beta_m(v)
  rate = zeros(size(v));
  rate = 4.0*exp(-v/18.0);
  return
  
function rate = alpha_n(v)
rate = zeros(size(v));
idx = find(v ==10.0);		% HANDLE SIGULARITY AT V=10.0 
if(~isempty(idx))
   rate(idx) = 0.1/exp((-v(idx)+10.0)/10.0);
end     
idx = find(v~=10.0);
if(~isempty(idx))
   rate(idx) = 0.01*(-v(idx)+10.0) ./ (exp((-v(idx)+10.0)/10.0) - 1.0);
end
return

function rate = beta_n(v)
  rate = zeros(size(v));
  rate = 0.125*exp(-v/80.0);
return