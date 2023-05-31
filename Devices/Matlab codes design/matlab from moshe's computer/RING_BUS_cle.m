function[x,y,str]=RING_BUS_cle(Lc,x0,y0,Lt)

%Lc=14;
%s=0.3;
h=80;
Rt=1*51.25;     %w=100
w=2*sqrt(Rt^2-(Rt-h/2)^2);
%w=100;
N=200;

ds=100;  %share delay

%510=2*w-35-40+ds+40+45

l=Lt-2*w-Lc;

[x1,y1]=straight_cle(x0,y0,0.5*l);
%[x2,y2]=twist_cle(x1(end),y1(end),w,h,N,0);
[x2,y2]=twist2_cle(Rt,h,'up',x1(end),y1(end),'h',N);
[x3,y3]=straight_cle(x2(end),y2(end),Lc);
%[x4,y4]=twist_cle(x3(end),y3(end),w,h,N,1);
[x4,y4]=twist2_cle(Rt,h,'down',x3(end),y3(end),'h',N);
[x5,y5]=straight_cle(x4(end),y4(end),0.5*l);

x=[x1;x2;x3;x4;x5];
y=[y1;y2;y3;y4;y5];    %LOWER ARM

%yu=2*h+s-y+0.7;         %UPPER ARM

%plot(x,y,x,yu);
%plot(x,y,'r');
%axis equal
%

str=sprintf('Lc=%.2f um',Lc);

end