function [] = OGCoDraw(x,y,period,DC,output_w,dir)
%The function recive XY and direction coordinates and draw optical gratting 
% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
%addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\mltoolbox\clewin\clewin'));
%% Adiabatic coupler
input_w = 5; %um
Adiabatic_lngth = 100;%um
contour = 10;%um
input_w_l = 15;%um
%%

adiabatic_Countor_cord = [x x-input_w_l x-input_w_l-Adiabatic_lngth x-input_w_l-Adiabatic_lngth x-input_w_l x;y+(input_w+contour)/2 y+(input_w+contour)/2 y+(input_w+contour)/2 y-(input_w+contour)/2 y-(input_w+contour)/2 y-(input_w+contour)/2];

adiabatic_Countor = clePolygon(adiabatic_Countor_cord);
%cleDraw(adiabatic_WG)
%% Gratting
period = 0.6;%um
DC = 0.5;
gratting_w = input_w;%um
lngth = 15;%um
gratting_num = floor(lngth/period);
gratting = adiabatic_Countor;%zeros(4,2);
%x=x+input_w_l;
i = gratting_num-1;
gratting_contour = clePolygon([x x+period*DC+period*i x+period*DC+period*i x; y+(gratting_w+contour)/2 y+(gratting_w+contour)/2 y+(-gratting_w-contour)/2 y+(-gratting_w-contour)/2]);
gratting = cleGroup(gratting,gratting_contour);
adiabatic_WG_mirror = cleMirror(adiabatic_Countor,[x+(period*DC+period*i)/2 0 pi/2]);
gratting = cleGroup(gratting,adiabatic_WG_mirror);
if strcmp('r',dir)
    gratting = cleTranslate(gratting,[Adiabatic_lngth+input_w_l 0]);
    TEXT=cleWire(15,'f',[x+117.5-100 y+27.5;x+117.5+100 y+27.5;]);

else
    gratting = cleTranslate(gratting,[-input_w_l-Adiabatic_lngth-(period*DC+period*i) 0]);
    TEXT=cleWire(15,'f',[x-117.5-100 y+27.5;x-117.5+100 y+27.5;]);
end

if strcmp('u',dir) || strcmp('d',dir)
   gratting = cleMirror(gratting,[x y -pi/4])
   TEXT=cleWire(15,'f',[x-100 y+257.5;x+100 y+257.5;]);
end

cleDraw(gratting)
cleDraw(TEXT)
end

