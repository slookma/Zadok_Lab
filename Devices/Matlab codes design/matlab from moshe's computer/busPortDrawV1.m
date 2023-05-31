function [left,right,top] = busPortDrawV1(R,coordinates,coupler,width,dir)
%Draw ring resonator that is radius is R and coupler length is Coupler
%and it can be located by the coupler center or right coordinate 

% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
    
if strcmp(dir,'d')     
    lngth = [coordinates(1)-2*R coordinates(2)-2*R coupler]

    QRindDraw(width,coordinates(1),coordinates(2),R,'LD')
    QRindDraw(width,coordinates(1)-R,coordinates(2)-R,R,'DL')
    busDraw(width,lngth,'l')
    Bottom = [coordinates(1)-2*R-0.5*coupler coordinates(2)-2*R];
    QRindDraw(width,Bottom(1)-0.5*coupler,Bottom(2),R,'LU');
    QRindDraw(width,Bottom(1)-R-0.5*coupler,Bottom(2)+R,R,'UL');
    right = coordinates;
    left = [Bottom(1)-0.5*coupler-2*R coordinates(2)];
    top = Bottom;
else    
    lngth = [coordinates(1)-2*R coordinates(2)+2*R coupler]
    QRindDraw(width,coordinates(1),coordinates(2),R,'LU')
    QRindDraw(width,coordinates(1)-R,coordinates(2)+R,R,'UL')
    busDraw(width,lngth,'l')
    top = [coordinates(1)-2*R-0.5*coupler coordinates(2)+2*R];
    QRindDraw(width,top(1)-0.5*coupler,top(2),R,'LD');
    QRindDraw(width,top(1)-R-0.5*coupler,top(2)-R,R,'DL');
    right = coordinates;
    left = [top(1)-0.5*coupler-2*R coordinates(2)];
end

