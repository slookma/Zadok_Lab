function[x,y,str]=RING_BUS_ex_cle(Lc,x0,y0,Lt,up,left)

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

[x1,y1]=straight_cle(x0,y0,0.1*l);
%[x2,y2]=twist_cle(x1(end),y1(end),w,h,N,0);
[x2,y2]=twist2_ex_cle(Rt,h,'up1',x1(end),y1(end),'h',N);
[x3,y3]=straight_ex_cle(x2(end),y2(end),up);
[x4,y4]=twist2_ex_cle(Rt,h,'up2',x3(end),y3(end),'h',N);
[x5,y5]=straight_cle(x4(end),y4(end),left);
[x6,y6]=twist2_ex_cle(Rt,h,'down1',x5(end),y5(end),'h',N);
[x7,y7]=straight_ex_cle(x6(end),y6(end),-Lc);
[x8,y8]=twist2_ex_cle(Rt,h,'up1',x7(end)-Rt,y7(end)-Rt,'h',N);
 x8 = flip(x8);
 y8 = flip(y8);
[x9,y9]=straight_cle(x8(end),y8(end),-(left-Rt));

[x10,y10]=twist2_ex_cle(Rt,h,'up2',x9(end)-Rt,y9(end)-Rt,'h',N);
 x10 = flip(x10);
 y10 = flip(y10);
[x11,y11]=straight_ex_cle(x10(end),y10(end),-(up-2*Rt));
%[x4,y4]=twist_cle(x3(end),y3(end),w,h,N,1);
[x12,y12]=twist2_ex_cle(Rt,h,'down2',x11(end),y11(end),'h',N);
[x13,y13]=straight_cle(x12(end),y12(end),0.9*l);

x=[x1;x2;x3;x4;x5;x6;x7;x8;x9;x10;x11;x12;x13];
y=[y1;y2;y3;y4;y5;y6;y7;y8;y9;y10;y11;y12;y13];    %LOWER ARM

%yu=2*h+s-y+0.7;         %UPPER ARM

%plot(x,y,x,yu);
%plot(x,y,'r');
%axis equal
%

str=sprintf('Lc=%.2f um',Lc);

end