addpath(genpath('\\madrid.eng.biu.ac.il\e2016\dokhanl\Desktop\clewin\scripts\Draw scripts'));
% MISSING - ENTER VECTORS FOR THE COMPOSITE WIDTH AND LENGTH FOR THE SINGLE
% SEGMENT DESIGN

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CNOT GATE -  single segment design |G = 1000um| W1 = 450um| W2 = 450um| L = 9.483um%%%%%%%%%%%%%%%%%%%%%%%
Font='Stencil';                                                                                                         

%% Settings
WGWidth =0.7 ;   % waveguide width outside of coupling region
zeroLngth =0  ;  % variable only to get coordinates with busDraw command
Portbuslngth = 100;

ArmBus = 0;
ArmcouplerRadius = 75;
couplerDistance =1 ;
couplerRadius = 50;
Priod =0.6 ;
DC =0.385 ;
Rring = 150;
RingAcouplerLength =0 ;
RingBcouplerLength =0 ;
couplerDistance =1 ;
W = [0.450];
L = [9.483];   
Vpitch = 127.5;
TotalLngth = 220+4*couplerRadius-4*ArmcouplerRadius ;
% Core Draw - layer #66
setlayer('#66')
% First third                                                                           
% Position:
x =-3500 + 2000 ;
y =-600 - 450;
startX = x + TotalLngth*0.5;
startY = y - 0.5 * couplerDistance;


%% Optical gratting right and upper bus
%OGWGDraw(startX,startY,Priod,DC,WGWidth,'r')
coordinates = busDraw(WGWidth,[startX startY zeroLngth],'l')
[left1,right1,top] = LowerBusDraw_CP(couplerRadius,[coordinates(1) coordinates(2)],WGWidth,W,L)  % First waveguide C_2-12 
coordinates = busDraw(WGWidth,[left1(1) left1(2) 300],'l')
OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'l')
coordinates = busDraw(WGWidth,[right1(1) right1(2) 300],'r')
OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'r')
[left,right,top] = UpperBusDraw_CP(couplerRadius,[top(1) top(2)+Vpitch],WGWidth,W,L)     % Second waveguide
coordinates = busDraw(WGWidth,[right1(1) right1(2)+4*couplerRadius+10.16+Vpitch 300],'r')
OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'r')
coordinates = busDraw(WGWidth,[left1(1) left1(2)+4*couplerRadius+10.16+Vpitch 300],'l')
OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'l')

% 
% % Second third
% % Position:
% x =-3500 + 2000 ;
% y =-600 - 750;
% startX = x + TotalLngth*0.5;
% startY = y - 0.5 * couplerDistance;
% 
% 
% %% Optical gratting right and upper bus
% %OGWGDraw(startX,stratY,Priod,DC,WGWidth,'r')
% coordinates = busDraw(WGWidth,[startX startY zeroLngth],'l')
% [left1,right1,top1] = LowerBusDraw_CP(couplerRadius,[coordinates(1) coordinates(2)],WGWidth,W,L)   % Third waveguide  C_2-34
% [left,right,top] = UpperBusDraw_CP(couplerRadius,[top1(1) top1(2)],WGWidth,W,L)    % Fourth waveguide center
% coordinates = busDraw(WGWidth,[right1(1) right1(2)+4*couplerRadius+10.16 300],'r')
% OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'r')
% coordinates = busDraw(WGWidth,[left1(1) left1(2)+4*couplerRadius+10.16 300],'l')
% OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'l')
% [left,right,top] = UpperBusDraw_CP(couplerRadius,[left1(1)-2*couplerRadius left1(2)-2*couplerRadius-10.15],WGWidth,W,L)  % Fourth waveguide left C_1-45
% [left2,right,top] = UpperBusDraw_CP(couplerRadius,[right1(1)+2*couplerRadius+10.5 right1(2)-2*couplerRadius-10.35],WGWidth,W,L)  % Fourth waveguide right C_3-45
% coordinates = busDraw(WGWidth,[right1(1)+4*couplerRadius+10 right1(2)-0.2 100],'r')
% OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'r')
% coordinates = busDraw(WGWidth,[left1(1)-4*couplerRadius-10.5 left1(2)+0.2 100],'l')
% OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'l')
% 
% 
% 
% % Third third
% % Position:
% x =-3500 + 2000 - 2*couplerRadius ;
% y =-600 - 1150;
% startX = x + TotalLngth*0.5;
% startY = y - 0.5 * couplerDistance;
% 
% 
% %% Optical gratting right and upper bus
% %OGWGDraw(startX,stratY,Priod,DC,WGWidth,'r')
% coordinates = busDraw(WGWidth,[startX startY zeroLngth],'l')
% %[left1,right1,top1] = LowerBusDraw_CP(couplerRadius,[coordinates(1) coordinates(2)],WGWidth,W,L)
% [left1,right1,top1] = UpperBusDraw_CP(couplerRadius,[coordinates(1) coordinates(2)],WGWidth,W,L) % Fifth waveguide center C_2-56
% W5 = 0.390; % Modify width according to table
% L45 = 18.446;
% [left,right,top] = LowerBusDraw_CP(couplerRadius,[top1(1)-5.8 top1(2)-0.35],WGWidth,W,L)  % Fifth waveguide left 
% coordinates = busDraw(WGWidth,[left(1) left(2) 300-4*couplerRadius],'l')
% OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'l')
% [left,right,top] = LowerBusDraw_CP(couplerRadius,[top1(1)-5.8+8*couplerRadius+21.7 top1(2)-0.545],WGWidth,W,L) % Fifth waveguide right 
% coordinates = busDraw(WGWidth,[right(1) right(2) 300-4*couplerRadius],'r')
% OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'r')
% x =-3500 + 2000 - 2*couplerRadius ;
% y =-600 - 1250;
% startX = x + TotalLngth*0.5;
% startY = y - 0.5 * couplerDistance;
% coordinates = busDraw(WGWidth,[startX startY zeroLngth],'l')
% [left1,right1,top1] = LowerBusDraw_CP(couplerRadius,[coordinates(1)+2*couplerRadius coordinates(2)],WGWidth,W,L) % Sixth waveguide
% coordinates = busDraw(WGWidth,[left1(1) left1(2) 300],'l')
% OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'l')
% coordinates = busDraw(WGWidth,[right1(1) right1(2) 300],'r')
% OGWGDraw(coordinates(1),coordinates(2),Priod,DC,WGWidth,'r') 