function [] = OGWGDTMDraw(x,y,period,DC,output_w,dir)
%The function recive XY and direction coordinates and draw optical gratting 
addpath(genpath('U:\My Documents\design\matlab_design'));


Font='Stencil';
%% Adiabatic coupler
input_w = 10; %um
Adiabatic_lngth = 100;%um
input_w_l = 15; %um

%%
% adiabatic_WG_cord = [x x-Adiabatic_lngth x-Adiabatic_lngth x;y+input_w/2 y+output_w/2 y-output_w/2 y-input_w/2];
% 
% adiabatic_WG = clePolygon(adiabatic_WG_cord);


%cleDraw(adiabatic_WG)
%% Gratting

str=[sprintf(' Period= '),num2str(period),sprintf(' um'),sprintf(' duty-cycle= '),num2str(DC*100)];

gratting_w = input_w;%um
lngth = 15;%um
gratting_num = floor(lngth/period);
gratting = {};%zeros(4,2);
for i=0:(gratting_num-1)
    gratt_cord = [x+period*i x+period*DC+period*i x+period*DC+period*i x+period*i;y+gratting_w/2 y+gratting_w/2 y-gratting_w/2 y-gratting_w/2];
    gratt = clePolygon(gratt_cord);
    gratting = cleGroup(gratting,gratt);
end
%     adiabatic_WG_mirror = cleMirror(adiabatic_WG,[x+(period*DC+period*i)/2 0 pi/2]);
%     gratting = cleGroup(gratting,adiabatic_WG_mirror);

if strcmp('r',dir)
    gratting = cleTranslate(gratting,[Adiabatic_lngth+input_w_l 0]);
   
    TEXT=gphPolygonPrintf(x+117.5,y+26,Font,10,'c',str);

else
    gratting = cleTranslate(gratting,[-Adiabatic_lngth-(period*DC+period*i)-input_w_l 0]);
    
    TEXT=gphPolygonPrintf(x-117.5,y+26,Font,10,'c',str);
    
end

if strcmp('u',dir) || strcmp('d',dir)
   gratting = cleMirror(gratting,[x y -pi/4])
   TEXT=gphPolygonPrintf(x,y+256,Font,10,'c',str);
   
  
end
cleDraw(TEXT);
cleDraw(gratting)

end

