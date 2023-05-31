function [coordinates] = busDraw(width,lngth,dir)
%The function recive XY coordinats of two ends or one cooridate and length in um and direction  and draw bus waveguide 
%  lngth = [X Y length] or [X1 Y1;X2 Y2] 
%  width = vector of pulses widthes

%  dir = direction
% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));

%%
offset = 20e-3;
dir_signx = 1;
dir_signy = 0;
if strcmp(dir,'l')
    dir_signx = -1;
    dir_signy = 0;
elseif strcmp(dir,'u')
    dir_signx = 0;
    dir_signy = 1;
elseif strcmp(dir,'d')  
    dir_signx = 0;
    dir_signy = -1;
end

if min(size(lngth)) == 1
     bus_WG_cord = [(lngth(1)-dir_signx*offset) (lngth(2)-dir_signy*offset);(lngth(1)+dir_signx*lngth(3)+dir_signx*offset) lngth(2)+dir_signy*lngth(3)+dir_signy*offset];
     bus_WG = cleWire(width,'f',bus_WG_cord); 
     coordinates = [lngth(1)+dir_signx*lngth(3) lngth(2)+dir_signy*lngth(3)];
elseif size(lngth) == [2 2]
     bus_WG_cord = [lngth(1,1) lngth(1,2);lngth(2,1) lngth(2,2)];
     bus_WG = cleWire(width,'f',bus_WG_cord);
     coordinates = [bus_WG_cord(2,1) bus_WG_cord(2,2)];
end

cleDraw(bus_WG)
end

