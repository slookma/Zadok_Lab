addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));


%%
Font='Stencil';
%% Place of coupler
x =0 ;
y =0 ;
%% Bus
WGWidth =0.7 ;
busLngth =8000  ;
Portbuslngth = 1000;
Contour =5 ;
%% Ring
Rring = 100;

Hight =0 ;
%% Coupler
R =50 ;
couplerDistance =0.3 ;
PortcouplerLength =8 ;
RingcouplerLength =0 ;
couplerRadius = 50;
%% Optical gratting
Period =0.6 ;
DC =0.385 ;

%%
TotalLngth = Portbuslngth+busLngth+4*couplerRadius+RingcouplerLength;
HBL = (TotalLngth - PortcouplerLength)*0.5-2*couplerRadius;

startX = x + TotalLngth*0.5; 
stratY = y - 0.5 * couplerDistance;
%%


%% Optical gratting right and upper bus
OGWGDraw(startX,stratY,Period,DC,WGWidth,'r')
coordinates = busDraw(WGWidth,[startX stratY busLngth],'l')


%% Coupler
[left,right,top] = busPortDraw2(couplerRadius,[coordinates(1) coordinates(2)],PortcouplerLength,WGWidth,couplerDistance,WGWidth)
%% Optical gratting right and lower bus
coordinates = busDraw(WGWidth,[right(2,1) right(2,2) busLngth],'r')
OGWGDraw(coordinates(1),coordinates(2),Period,DC,WGWidth,'r')

str=[sprintf(' Period= '),num2str(Period),sprintf(' um'),sprintf(' duty-cycle= '),num2str(DC*100)];

TEXT=gphPolygonPrintf(coordinates(1)+117.5,coordinates(2)+20,Font,10,'c',str);
cleDraw(TEXT);
%% Lower output port , ring + drop port and optical grattings
new_coordinates = busDraw(WGWidth,[left(1,1) left(1,2) Portbuslngth/2],'l')
new_coordinates = new_coordinates+[-4*R+RingcouplerLength 0]
[left_ring,right_ring,top_ring] = OringDropDraw(-R,-Rring,new_coordinates,RingcouplerLength,-WGWidth,-couplerDistance,-Hight,WGWidth,'u');
new_coordinates = busDraw(WGWidth,[new_coordinates(1)-RingcouplerLength new_coordinates(2) Portbuslngth/2],'l')
OGWGDraw(new_coordinates(1),new_coordinates(2),Period,DC,WGWidth,'l')

new_coordinates = QRindDraw(WGWidth,left(2,1),left(2,2),R,'LU')
OGWGDraw(new_coordinates(1),new_coordinates(2),Period,DC,WGWidth,'u')
new_coordinates = QRindDraw(WGWidth,left_ring(2,1),left_ring(2,2),R,'RD')
new_coordinates = QRindDraw(WGWidth,new_coordinates(1),new_coordinates(2),R,'DL')
new_coordinates = busDraw(WGWidth,[new_coordinates(1) new_coordinates(2) Portbuslngth/2],'l')
OGWGDraw(new_coordinates(1),new_coordinates(2),Period,DC,WGWidth,'l')
OGWGDraw(right_ring(2,1),right_ring(2,2),Period,DC,WGWidth,'l')


setlayer('#88');

%% Optical gratting right and upper bus
OGCoDraw(startX,stratY,Period,DC,WGWidth,'r')
coordinates = busDraw(Contour,[startX stratY busLngth],'l')
%% Coupler
[left,right,top] = busPortDraw2(couplerRadius,[coordinates(1) coordinates(2)],PortcouplerLength,WGWidth,couplerDistance,Contour)
coordinates = busDraw(Contour,[right(2,1) right(2,2) busLngth],'r')
%% Optical gratting right and lower bus
OGCoDraw(coordinates(1),coordinates(2),Period,DC,WGWidth,'r')
new_coordinates = busDraw(Contour,[left(1,1) left(1,2) Portbuslngth/2],'l')
%% Lower output port , ring + drop port and optical grattings
new_coordinates = new_coordinates+[-4*R+RingcouplerLength 0]
[left_ring,right_ring,top_ring] = OringDropDraw(-R,-Rring,new_coordinates,RingcouplerLength,-WGWidth,-couplerDistance,-Hight,Contour,'u');
new_coordinates = busDraw(Contour,[new_coordinates(1)-RingcouplerLength new_coordinates(2) Portbuslngth/2],'l')
OGCoDraw(new_coordinates(1),new_coordinates(2),Period,DC,WGWidth,'l')
new_coordinates = QRindDraw(Contour,left(2,1),left(2,2),R,'LU')
OGCoDraw(new_coordinates(1),new_coordinates(2),Period,DC,WGWidth,'u')
new_coordinates = QRindDraw(Contour,left_ring(2,1),left_ring(2,2),R,'RD')
new_coordinates = QRindDraw(Contour,new_coordinates(1),new_coordinates(2),R,'DL')
new_coordinates = busDraw(Contour,[new_coordinates(1) new_coordinates(2) Portbuslngth/2],'l')
OGCoDraw(new_coordinates(1),new_coordinates(2),Period,DC,WGWidth,'l')
OGCoDraw(right_ring(2,1),right_ring(2,2),Period,DC,WGWidth,'l')