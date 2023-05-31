function [left,right,top] = busPortDraw2(R,coordinates,coupler,width,distance,countor)
%Draw ring resonator that is radius is R and coupler length is Coupler
%and it can be located by the coupler center or right coordinate 

% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
    
lngth = [coordinates(1)-2*R coordinates(2)+2*R coupler];

    QRindDraw(countor,coordinates(1),coordinates(2),R,'LU')
    next = QRindDraw(countor,coordinates(1)-R,coordinates(2)+R,R,'UL');
    busDraw(countor,lngth,'l')
    top = [coordinates(1)-2*R-0.5*coupler coordinates(2)+2*R];
    QRindDraw(countor,top(1)-0.5*coupler,top(2),R,'LD');
    QRindDraw(countor,top(1)-R-0.5*coupler,top(2)-R,R,'DL');
    right = coordinates;
    left = [top(1)-0.5*coupler-2*R coordinates(2)];
    %% upper port
    next1 = QRindDraw(countor,next(1),next(2)+width+distance,R,'RU');
    next2 = QRindDraw(countor,next1(1),next1(2),R,'UR');
    lngth1 = [coordinates(1)-2*R coordinates(2)+2*R+width+distance coupler];
    next3 = busDraw(countor,lngth1,'l');
    next4 = QRindDraw(countor,next3(1),next3(2),R,'LU');
    next5 = QRindDraw(countor,next4(1),next4(2),R,'UL');
    
    
    top = [coordinates(1)-2*R-0.5*coupler coordinates(2)+2*R+width+distance];
    right(2,:) =next2;
    left(2,:) =next5;
end

