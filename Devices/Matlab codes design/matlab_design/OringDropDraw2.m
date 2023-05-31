function [left,right,top] = OringDropDraw2(R,Rring,coordinates,coupler,width,distance,ring_width,contour,dir)
%Draw ring resonator that is radius is R and coupler length is Coupler
%and it can be located by the coupler center or right coordinate 

% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
lngth = [coordinates(1)-2*R coordinates(2)-2*R coupler];
if strcmp(dir,'d') 
    %%Upper ports
    QRindDraw(contour,coordinates(1)-coupler,coordinates(2),R,'LD')
    next = QRindDraw(contour,coordinates(1)-R-coupler,coordinates(2)-R,R,'DL');
    busDraw(contour,lngth,'l')
    top = [coordinates(1)-2*R-0.5*coupler coordinates(2)-2*R];
    QRindDraw(contour,top(1)+0.5*coupler,top(2),R,'LU');
    QRindDraw(contour,top(1)-R+0.5*coupler,top(2)+R,R,'UL');
    right(1,:) = coordinates;
    left(1,:) = [top(1)-0.5*coupler-2*R coordinates(2)];
    % ring
    if contour==abs(width)
        width1 = width;
    else
        width1 = -contour/2;
    end
    
    OringDraw(contour,top(1),top(2)-distance,Rring,coupler, ring_width,width,dir)
    
    %% lower port
    next1 = QRindDraw(contour,next(1),next(2)-2*Rring-3*width-2*distance,R,'RD');
    next2 = QRindDraw(contour,next1(1),next1(2),R,'DR');
    lngth1 = [coordinates(1)-2*R-coupler coordinates(2)-2*Rring-2*R-3*width-2*distance -coupler]
    next3 = busDraw(contour,lngth1,'l');
    next4 = QRindDraw(contour,next3(1),next3(2),R,'LD');
    next5 = QRindDraw(contour,next4(1),next4(2),R,'DL');
    
    
    top = [coordinates(1)-2*R-0.5*coupler coordinates(2)+2*R+width+distance];
    right(2,:) =next5;
    left(2,:) =next2;
else
    QRindDraw(contour,coordinates(1)-coupler,coordinates(2),R,'LU')
    next = QRindDraw(contour,coordinates(1)-R-coupler,coordinates(2)+R,R,'UL');
    busDraw(contour,lngth,'l')
    top = [coordinates(1)-2*R-0.5*coupler coordinates(2)+2*R];
    QRindDraw(contour,top(1)+0.5*coupler,top(2),R,'LD');
    QRindDraw(contour,top(1)-R+0.5*coupler,top(2)-R,R,'DL');
    right = coordinates;
    left = [top(1)-0.5*coupler-2*R coordinates(2)];
    %% ring
    if contour==abs(width)
        width1 = width;
    else
        width1 = -contour/2;
    end
    
    OringDraw(contour,next(1)+0.5*coupler,top(2)+2*width1+distance,Rring,-coupler, ring_width,contour,dir)
    
    %% upper port
    next1 = QRindDraw(contour,next(1),next(2)+2*Rring+2*width+3*distance,R,'RU');
    next2 = QRindDraw(contour,next1(1),next1(2),R,'UR');
    lngth1 = [coordinates(1)-2*R-coupler coordinates(2)+2*Rring+2*R+2*width+3*distance -coupler]
    next3 = busDraw(contour,lngth1,'l');
    next4 = QRindDraw(contour,next3(1),next3(2),R,'LU');
    next5 = QRindDraw(contour,next4(1),next4(2),R,'UL');
    
    
    top = [coordinates(1)-2*R-0.5*coupler coordinates(2)+2*R+width+distance];
    right(2,:) =next2;
    left(2,:) =next5;
end
end

