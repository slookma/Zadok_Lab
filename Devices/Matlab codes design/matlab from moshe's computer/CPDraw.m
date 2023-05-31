function [coordinates] = CPDraw(X,Y,width,W,W1,L,L1,rep,dir)
%The function recive XY coordinats of two ends or one cooridate and length in um and direction  and draw bus waveguide 
%  [X Y] = starting point
%  W = vector of pulses widthes
%  L = vector of pulses lengthes
%  bus = direction
% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));

%%
%addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\mltoolbox\clewin\clewin'));
CouplerLength=sum(L)*rep;
taper = 1;
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
X = X - 0.1;
L = L-1;
L1 = L1-1;
for i=1:rep
    if i==1
        Taper = clePolygon([X X-taper X-taper X; Y+width/2 Y+W1(2)/2 Y-W1(2)/2 Y-width/2]);
        X0 = X-taper;
        Y0 = Y;
        cleDraw(Taper)
        
           bus_WG_cord = [X0 Y0;(X0+dir_signx*L1(2)) Y0+dir_signy*L1(2)];
           bus_WG = cleWire(W1(2),'f',bus_WG_cord);
           X0 = X0+dir_signx*L1(2);
           Y0 = Y0+dir_signy*L1(2);
           cleDraw(bus_WG)
           
           Taper = clePolygon([X0 X0-taper X0-taper X0; Y0+W1(2)/2 Y0+W1(1)/2 Y0-W1(1)/2 Y0-W1(2)/2]);
           X0 = X0-taper;
           Y0 = Y0; 
           cleDraw(Taper)
           
           bus_WG_cord = [X0 Y0;(X0+dir_signx*L1(1)) Y0+dir_signy*L1(1)];
           bus_WG = cleWire(W1(1),'f',bus_WG_cord);
           X0 = X0+dir_signx*L1(1);
           Y0 = Y0+dir_signy*L1(1);
           cleDraw(bus_WG)
           
           Taper = clePolygon([X0 X0-taper X0-taper X0; Y0+W1(1)/2 Y0+W(end)/2 Y0-W(end)/2 Y0-W1(1)/2]);
           X0 = X0-taper;
           Y0 = Y0; 
           cleDraw(Taper)
        
    end
        
   for ii=length(W):2
           bus_WG_cord = [X0 Y0;(X0+dir_signx*L(ii)) Y0+dir_signy*L(ii)];
           bus_WG = cleWire(W(ii),'f',bus_WG_cord);
           X0 = X0+dir_signx*L(ii);
           Y0 = Y0+dir_signy*L(ii);
           cleDraw(bus_WG)
           
           Taper = clePolygon([X0 X0-taper X0-taper X0; Y0+W(ii)/2 Y0+W(ii-1)/2 Y0-W(ii-1)/2 Y0-W(ii)/2]);
           X0 = X0-taper;
           Y0 = Y0; 
           cleDraw(Taper)
   end
   if i==rep
        
         bus_WG_cord = [X0 Y0;(X0+dir_signx*(L(1)-1)) Y0+dir_signy*(L(1)-1)];
        bus_WG = cleWire(W(1),'f',bus_WG_cord);
        X0 = X0+dir_signx*(L(1)-1);
        Y0 = Y0+dir_signy*(L(1)-1);
        cleDraw(bus_WG)
        Taper = clePolygon([X0 X0-taper X0-taper X0; Y0+W(1)/2 Y0+width/2 Y0-width/2 Y0-W(1)/2]);
        X0 = X-taper;
        Y0 = Y0;
        cleDraw(Taper)
   else
        bus_WG_cord = [X0 Y0;(X0+dir_signx*L(1)) Y0+dir_signy*L(1)];
        bus_WG = cleWire(W(1),'f',bus_WG_cord);
        X0 = X0+dir_signx*L(1);
        Y0 = Y0+dir_signy*L(1);
        cleDraw(bus_WG)
        Taper = clePolygon([X0 X0-taper X0-taper X0; Y0+W(1)/2 Y0+W(end)/2 Y0-W(end)/2 Y0-W(1)/2]);
        X0 = X0-taper;
        Y0 = Y0; 
        cleDraw(Taper)
    end
    
    
    
end
    coordinates = [X0 Y0];
    cleDraw(bus_WG)
end 





