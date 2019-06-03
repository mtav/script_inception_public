
function [Camera,CurrentDir]=...
   maze6key(fig1,fig2,Camera,s1,CurrentDir,action)

%implements the navigation commands

%move forward
if (action==8) 
   Camera = Camera + 0.25*CurrentDir ; 
end

%turn left
if (action==4)
   if (CurrentDir==[1 0 0])
      CurrentDir=[0 1 0];
   elseif (CurrentDir==[0 1 0])
      CurrentDir=[-1 0 0];
   elseif (CurrentDir==[-1 0 0])
      CurrentDir=[0 -1 0];
   elseif (CurrentDir==[0 -1 0])
      CurrentDir=[1 0 0];
   end;
end  

%turn right
if (action==6)
   if (CurrentDir==[1 0 0])
      CurrentDir=[0 -1 0];
   elseif (CurrentDir==[0 -1 0])
      CurrentDir=[-1 0 0];
   elseif (CurrentDir==[-1 0 0])
      CurrentDir=[0 1 0];
   elseif (CurrentDir==[0 1 0])
      CurrentDir=[1 0 0];
   end;
end;

%backup without turning
if (action==2) 
   Camera = Camera - 0.25*CurrentDir ; 
end;   

set(gca,'cameraposition',Camera);
set(gca,'cameratarget', CurrentDir*10+Camera );

set(0,'currentfigure',fig1);
renderpatch(translate(s1,Camera(1),Camera(2),0));
line([Camera(1) Camera(1)+CurrentDir(1)/3], ...
   [Camera(2) Camera(2)+CurrentDir(2)/3], ...
   [Camera(3) Camera(3)]);

set(0,'currentfigure',fig2);
