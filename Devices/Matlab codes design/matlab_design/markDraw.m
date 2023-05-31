function [] = markDraw(x,y,Width,Length,layerO)
%The function recive XY and direction coordinates and draw optical gratting 
%addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
addpath(genpath('U:\My Documents\design\matlab_design'));





   
%%
resoultion = 0.2;
if strcmp('clad',layerO)
    coordinatsY = [x y-Length/2;x y+Length/2];
    coordinatsX = [x-Length/2 y;x+Length/2 y];

    MarkerY = cleWire(Width,'f',coordinatsY);
    cleDraw(MarkerY)
    
    MarkerX = cleWire(Width,'f',coordinatsX);
    cleDraw(MarkerX)
    
    coordinatsText = [x-100 y+Length/2+20;x+100 y+Length/2+20];
    TEXT = cleWire(20,'f',coordinatsText );
    
else
    markerUp = [x-resoultion x-Width/2 x+Width/2 x+resoultion;y y+Length/2 y+Length/2 y];
    markerDown = [x-resoultion x-Width/2 x+Width/2 x+resoultion;y y-Length/2 y-Length/2 y];
    
    markerLeft = [x x-Length/2 x-Length/2 x;y-resoultion y-Width/2 y+Width/2 y+resoultion];
    markerRight = [x x+Length/2 x+Length/2 x;y-resoultion y-Width/2 y+Width/2 y+resoultion];

    markerUp = clePolygon(markerUp);
    marker=cleGroup(markerUp,clePolygon(markerDown));
    marker=cleGroup(marker,clePolygon(markerLeft));
    marker=cleGroup(marker,clePolygon(markerRight));
    Font='Stencil';
    str=[sprintf(' x= '),num2str(x),sprintf(' um'),sprintf(' y= '),num2str(y),sprintf(' um')];
    TEXT=gphPolygonPrintf(x,y+Length+10,Font,20,'c',str);
   




cleDraw(marker)
end 
cleDraw(TEXT)
end

