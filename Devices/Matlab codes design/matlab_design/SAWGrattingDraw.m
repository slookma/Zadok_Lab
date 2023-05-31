function [] = SAWGrattingDraw(x,y,period,DC,size,dir)
%The function recive XY and direction coordinates and draw optical gratting 
addpath(genpath('U:\My Documents\design\matlab_design'));


Font='Stencil';
%% Adiabatic coupler

DC_text = DC;
DC = 1-DC;
num = floor(size/period);

%% Gratting

str=[sprintf(' Period= '),num2str(period),sprintf(' um'),sprintf(' size= '),num2str(size),sprintf(' um')];

TEXT=gphPolygonPrintf(x-5,y+100,Font,10,'c',str);
x=x-(num*period)/2;
gratting = {};
for i=0:(num-1)
    gratt_cord = [x+period*i x+period*DC+period*i x+period*DC+period*i x+period*i;y+size/2 y+size/2 y-size/2 y-size/2];
    gratt = clePolygon(gratt_cord);
    gratting = cleGroup(gratting,gratt);
end


% if strcmp('l',dir)
%     gratting = cleTranslate(gratting,[-num*period 0]);
%    
%     TEXT=gphPolygonPrintf(x+117.5,y+20,Font,10,'c',str);
% 
% else
%     gratting = cleTranslate(gratting,[-input_w_l-Adiabatic_lngth-(period*DC+period*i) 0]);
%     
%     TEXT=gphPolygonPrintf(x-117.5,y+20,Font,10,'c',str);
%     
% end

if strcmp('u',dir) || strcmp('d',dir)
   gratting = cleMirror(gratting,[x y -pi/4])
   TEXT=gphPolygonPrintf(x,y+250,Font,10,'c',str);
   
  
end
cleDraw(TEXT);
cleDraw(gratting)

end

