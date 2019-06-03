%Generate a maze and define nagigation controls
%REQUIRES 3D stuff from Heirarchy page

clear all;

%initialize a couple of figures
fig1=figure(1);
clf;
fig2=figure(2);
clf;

%n is the size of the maze
n=10;

%Build a platform for the maze
base=translate(scale(UnitCube, n/2+1,n/2+1,1),n/2+.5,n/2+.5,-1);
base.facecolor=[.1,.8,.1];
base.facelighting='flat';

%Build prototype walls in the x and y directions
thickness=.1;
len=.5;
xwall=scale(UnitCube,len,thickness,1);
xwall.facecolor='red';
xwall.facelighting='flat';
xwall.edgecolor='black';

ywall=scale(UnitCube,thickness,len,1);
ywall.facecolor='yellow';
ywall.facelighting='flat';
ywall.edgecolor='black';

%set the probability of putting a wall at a given x.y location
Pwallsx=.4;
Pwallsy=.4;
%initialize the geometric structure to be rendered later
mymaze=base;

%threshold probabilities in the x and y directions
thx=rand(n,n);
thy=rand(n,n);

%build the maze geometry
for x=1:n-1  
   for y=1:n-1
      if (thx(x,y)>Pwallsx)
         mymaze=combine(mymaze,translate(xwall,x,y,1));
      end
      if (thy(x,y)>Pwallsy)
         mymaze=combine(mymaze,translate(ywall,x,y,1));
      end
      
   end
end

%Spheres to show current location and goal location
s1=scale(UnitSphere(2),.15,.15,.15); 
s2=scale(UnitSphere(2),.2,.2,.2);
s1.facecolor='white';
s2.facecolor='white';

%camera location, lookto point, goal location
Camera=[-.25, n/2, 1.5];     
LookX=n; LookY=n/2;
GoalX=n/2+.5; GoalY=n/2+.5;
%start by facing along the x-axis
CurrentDir=[1 0 0];

%============================================
%Render the scene into figure one (overhead view)
set(0,'currentfigure',fig1);
count=renderpatch(mymaze);
count=renderpatch(translate(s1,Camera(1),Camera(2),0));     
count=renderpatch(translate(s2,GoalX,GoalY,Camera(3)));

%control to clear all the previous positions
uicontrol('style','pushbutton',...
   'string','Clear history',...
   'position',[0 0 70 15],...
   'callback',...
   ['cla;count=renderpatch(mymaze);'...
   'count=renderpatch(translate(s1,Camera(1),Camera(2),0));'...     
   'count=renderpatch(translate(s2,GoalX,GoalY,Camera(3)));'...
   'figure(fig2);'...
]);

axis off;
daspect([1 1 1]);
%set(gca,'projection','perspective');
set(gca,'CameraViewAngle',5);
light('position',[3,5,10],'style','local')
set(gcf,'color', [.6,.8,.8])
rotate3d on

%==========================================
%render figure 2 (maze internal view) and set up 
%nagivation controls
set(0,'currentfigure',fig2);
set(gcf,'renderer','zbuffer');

%string to ge used in callbacks
funcall=...
   '[Camera,CurrentDir]=maze6key(fig1,fig2,Camera,s1,CurrentDir,action);';

%Navigation controls
uicontrol('style','pushbutton',...
   'string','Frwd',...
   'position',[30 35 30 15],...
   'backgroundcolor','white',...
   'callback',...
   ['action=8;'funcall]);

uicontrol('style','pushbutton',...
   'string','Left',...
   'position',[15 20 30 15],...
   'backgroundcolor','white',...
   'callback',...
   ['action=4;'funcall]);

uicontrol('style','pushbutton',...
   'string','Rght',...
   'position',[45 20 30 15],...
   'backgroundcolor','white',...
   'callback',...
   ['action=6;'funcall]);

uicontrol('style','pushbutton',...
   'string','Back',...
   'position',[30 5 30 15],...
   'backgroundcolor','white',...
   'callback',...
   ['action=2;'funcall]);

count=renderpatch(combine ...
   (translate(s2,GoalX,GoalY,Camera(3)),mymaze));
axis off;
daspect([1 1 1]);

%Do a persptective transform and position the camera
set(gca,'projection','perspective');
set(gca,'CameraViewAngle',90);
set(gca,'cameraviewanglemode','manual');
set(gca,'cameraposition',Camera);
set(gca,'camerapositionmode','manual');
set(gca,'cameratarget',[LookX,LookY,Camera(3)]);
set(gca,'cameratargetmode','manual');

camlight('right','local');

%The frame background color
set(gcf,'color', [.6,.8,.8])
%view(-0,90)
rotate3d off

%Dislay elapsed time in the maze
elapsed=uicontrol('style','text',...
   'string','0',...
   'units','normalized', ...
   'position',[.45 .0 .1 .04],...
   'backgroundcolor','white' ...
   );

%outa here
uicontrol('style','pushbutton',...
   'string','EXIT', ...
   'units','normalized', ...
   'position',[.45 .95 .1 .05],...
   'backgroundcolor','red',...
   'callback','clf;figure(fig1);clf;exitflag=0;');

%time display
tic;
exitflag=1;

while(exitflag==1)
   set(elapsed, 'string', num2str(toc,'%6.0f'));
   drawnow
end

