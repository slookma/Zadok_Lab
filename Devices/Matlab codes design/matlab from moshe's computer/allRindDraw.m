function [point] = allRindDraw(width,teta,x,y,R,dir)
%%The function recive XY coordinates and radii and direction and draw circle qaurter waveguide 
% teta - anglr boundries in degrees 
% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));

offset = 0.001;
numOfpoints = abs(abs((teta(1))-abs((teta(2)))))/90*200;
%%
 teta = teta(1):(teta(2)-teta(1))/numOfpoints:teta(2);
    xP = x-R*sind(teta(1))+R*sind(teta);
    yP = y-R*cosd(teta(1))+R*cosd(teta);



% if strcmp(dir,'UL')||strcmp(dir,'RD')
%     % l
%     teta = (0-offset):0.5*pi/numOfpoints:(0.5+offset)*pi+0.5*pi/numOfpoints;
%     xP = x-R+R*sin(teta);
%     yP = y+R*cos(teta);
%      
%     if strcmp(dir,'RD')
%         xP = x+R*sin(teta);
%         yP = y-R+R*cos(teta);
%         xP = flip(xP);
%         yP = flip(yP);
%     end
%     plot(xP,yP,'.g')
% end
% if strcmp(dir,'DL')||strcmp(dir,'RU')
%     % d
%     teta = (0.5-offset)*pi:0.5*pi/numOfpoints:(pi+offset)+0.5*pi/numOfpoints;
%     xP = x-R+R*sin(teta);
%     yP = y+R*cos(teta);
%     xP = flip(xP);
%     yP = flip(yP);
%    
%     if strcmp(dir,'RU')
%         xP = x+R*sin(teta);
%         yP = y+R+R*cos(teta);
%     end
%     plot(yP,xP,'.g')
% end
% if strcmp(dir,'DR')||strcmp(dir,'LU')
%     % u
%     teta = (pi-offset):0.5*pi/numOfpoints:(1.5+offset)*pi+0.5*pi/numOfpoints;
%     xP = x+R*sin(teta);
%     yP = y+R+R*cos(teta);
%     xP = fliplr(xP);
%     yP = fliplr(yP);
%     if strcmp(dir,'DR')
%         xP = x+R+R*sin(teta);
%         yP = y+R*cos(teta);
%     end
%     plot(xP,yP,'.g')
% end
% if strcmp(dir,'UR')||strcmp(dir,'LD')
%     % r
%     teta = (1.5-offset)*pi:0.5*pi/numOfpoints:(2*pi+offset)+0.5*pi/numOfpoints;
%     xP = x+R+R*sin(teta);
%     yP = y+R*cos(teta);
%     xP = fliplr(xP);
%     yP = fliplr(yP);
%     if strcmp(dir,'LD')
%        xP = x+R*sin(teta);
%        yP = y-R+R*cos(teta);
%     end
%     plot(xP,yP,'.g')
% end
qaurterCirc = cleWire(width,'f',[xP' yP']);

cleDraw(qaurterCirc)
point = [xP(end) yP(end)];

end

