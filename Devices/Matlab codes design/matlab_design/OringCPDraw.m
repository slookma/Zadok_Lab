function [] = OringCPDraw(width,x,y,R,W,W1,L,L1,rep,ring_width,contour,dir)
%%The function recive XY coordinates and radii and direction and draw circle qaurter waveguide 

% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
coupler = sum(L)*rep+sum(L1);
if strcmp(dir,'l')
    %ring = cleRing(x-R-contour,y,width,R);
    busDraw(width,[x-contour y-0.5*coupler coupler],'u')
    QRindDraw(width,x-contour,y+0.5*coupler,R,'UR')
    busDraw(width,[x-contour+R y+0.5*coupler+R ring_width],'l')
    QRindDraw(width,x-contour+R+ring_width,y+R+0.5*coupler,R,'RD')
    busDraw(width,[x-contour+2*R y-0.5*coupler coupler],'u')
    QRindDraw(width,x-contour+2*R+ring_width,y-0.5*coupler,R,'DL')
    busDraw(width,[x-contour+Ry-0.5*coupler-R ring_width],'l')
    QRindDraw(width,x-contour+R,y-R-0.5*coupler,R,'LU')
end
if strcmp(dir,'r')
    %ring = cleRing(x+R+contour,y,width,R);
    QRindDraw(width,x+contour,y,R,'UL')
    QRindDraw(width,x+contour-R,y+R,R,'LD')
    QRindDraw(width,x+contour-2*R,y,R,'DR')
    QRindDraw(width,x+contour-R,y-R,R,'RU')
end
if strcmp(dir,'u')
    %ring = cleRing(x,y+R+contour,width,R);
    CPDraw(x+0.5*coupler,y+contour,width,W,W1,L,L1,rep,'l')
    %busDraw(width,[x+0.5*coupler y+contour coupler],'l')
    next = QRindDraw(width,x+0.5*coupler,y+contour,R,'RU');
    next1 = busDraw(width,[next(1) next(2) ring_width],'u');
    next2 = QRindDraw(width,next1(1),next1(2),R,'UL');
    next3 = busDraw(width,[next2(1) next2(2) coupler],'l');
    next4 = QRindDraw(width,next3(1),next3(2),R,'LD');
    next5 = busDraw(width,[next4(1) next4(2) ring_width],'d');
    QRindDraw(width,next5(1),next5(2),R,'DR')
end
if strcmp(dir,'d')
    %ring = cleRing(x,y-R-contour,width,R);
     
    QRindDraw(width,x,y-contour,R,'RD')
    QRindDraw(width,x+R,y-R-contour,R,'DL')
    QRindDraw(width,x,y-2*R-contour,R,'LU')
    QRindDraw(width,x-R,y-R-contour,R,'UR')
end
%cleDraw(ring)
end

