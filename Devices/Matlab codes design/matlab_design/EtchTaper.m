function [x,y] = EtchTaper(x,y,Taper,WidthIn,EtchWidth,dir)
%The function recive XY and direction coordinates and draw optical gratting 
% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
%addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\mltoolbox\clewin\clewin'));
%% Adiabatic coupler




if strcmp('r',dir)
   
%%

    adiabatic_Countor_cord = [x-Taper x x x-Taper x x x-Taper;y+EtchWidth/2 y+EtchWidth/2 y+WidthIn/2 y y-WidthIn/2 y-EtchWidth/2 y-EtchWidth/2];

    adiabatic_Countor = clePolygon(adiabatic_Countor_cord);




else
    adiabatic_Countor_cord = [x x-Taper x-Taper x x-Taper x-Taper x;y+EtchWidth/2 y+EtchWidth/2 y+WidthIn/2 y y-WidthIn/2 y-EtchWidth/2 y-EtchWidth/2];

    adiabatic_Countor = clePolygon(adiabatic_Countor_cord);
x=x+Taper;
end    
x=x-Taper;


cleDraw(adiabatic_Countor)
end

