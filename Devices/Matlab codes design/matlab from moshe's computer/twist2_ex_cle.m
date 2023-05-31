function[x,y]=twist2_cle(R,p,v,x0,y0,s,N)

%R=Radii
%p= parameter, w or h
%v= direction 'up' or 'down'
%s= detrmine p, 'w' or 'h'

sig=sign(p);
p=abs(p);

if p==0
    sig=1;
end

%N=200;

if s=='h'
    f=acos((1-(p)/(2*R)))/pi;
elseif s=='w'
    f=asin((p)/(2*R))/pi;
end

if sig==1
    if strcmp(v,'up1')==1
        [x1,y1]=curve_cle(x0,y0,1.5*pi,2*pi,R,N);
    elseif strcmp(v,'up2')==1    
        [x1,y1]=curve_cle(x0(end),y0(end),1*pi,(0.5)*pi,R,N);
    elseif strcmp(v,'down1')==1
        [x1,y1]=curve_cle(x0,y0,0.5*pi,0*pi,R,N);
    elseif strcmp(v,'down2')==1
        [x1,y1]=curve_cle(x0(end),y0(end),1*pi,(1.5)*pi,R,N);
    end
    
elseif sig==-1
   if strcmp(v,'up')==1
        [x1,y1]=curve_cle(x0,y0,(0.5)*pi,(0.5+f)*pi,R,N);
        [x2,y2]=curve_cle(x1(end),y1(end),(1.5+f)*pi,1.5*pi,R,N);
 
   elseif strcmp(v,'down')==1
        [x1,y1]=curve_cle(x0,y0,(1.5)*pi,(1.5-f)*pi,R,N);
        [x2,y2]=curve_cle(x1(end),y1(end),(0.5-f)*pi,0.5*pi,R,N);
   end
end
    
x=x1;
y=y1;

% plot(x,y);
% axis equal
 abs(x(end)-x(1));
end
    