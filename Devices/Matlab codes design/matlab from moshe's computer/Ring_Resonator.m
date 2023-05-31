%addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\mltoolbox\clewin\clewin'));

%% Place of coupler
x =0 ; 
y =0 ;
%% Bus
WGWidth =0.7 ;
busLngth =3000  ;
Contour =5 ;
%% Ring
R =50 ;
Hight =0 ;
%% Coupler
couplerDistance =0.3 ;
couplerLength =353.1 ;
couplerRadius = 50;
%% Optical gratting
Priod =0.6 ;
DC =0.5 ;

%%
startX = x + busLngth*0.5; 
stratY = y - 0.5 * couplerDistance;
HBL = (busLngth - couplerLength)*0.5-2*couplerRadius;

OGWGDraw(startX,stratY,Priod,DC,WGWidth,'r')
coordinates = busDraw(WGWidth,[startX stratY HBL],'l')
%cleCircle(coordinates(1), coordinates(2),10)
[left,right,top] = busPortDraw(couplerRadius,[coordinates(1) coordinates(2)],couplerLength,WGWidth)
OringDraw(WGWidth,top(1),couplerDistance+top(2),R,couplerLength,Hight,WGWidth,'u')

new_coordinates = busDraw(0.7,[left(1) left(2) HBL],'l')

OGWGDraw(new_coordinates(1),new_coordinates(2),Priod,DC,WGWidth,'l')

setlayer('#clad');

OGCoDraw(startX,stratY,Priod,DC,WGWidth,'r')
coordinates = busDraw(Contour,[startX stratY HBL],'l')
%cleCircle(coordinates(1), coordinates(2),10)
[left,right,top] = busPortDraw(couplerRadius,[coordinates(1) coordinates(2)],couplerLength,Contour)
OringDraw(Contour,top(1),couplerDistance+top(2),R,couplerLength,Hight,WGWidth,'u')

new_coordinates = busDraw(Contour,[left(1) left(2) HBL],'l')

OGCoDraw(new_coordinates(1),new_coordinates(2),Priod,DC,WGWidth,'l')