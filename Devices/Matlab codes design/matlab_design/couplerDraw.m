function [left,right] = couplerDraw(R,coordinates,distance,coupler,contour,width)
%Draw coupler that is radius is R and coupler length is Coupler
%and it can be located by the coupler center or right coordinate 

% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
    
lngth = [coordinates(1)-0.5*coupler coordinates(2)+distance+contour coupler];

    next1 = QRindDraw(width,coordinates(1)-0.5*coupler,coordinates(2)+distance+contour,R,'LU');
    left = QRindDraw(width,next1(1),next1(2),R,'UL');
    next2 = busDraw(width,lngth,'r');
    next3 = QRindDraw(width,next2(1),next2(2),R,'RU');
    right = QRindDraw(width,next3(1),next3(2),R,'UR');
    
end
