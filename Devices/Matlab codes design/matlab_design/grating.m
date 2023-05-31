
function[x,yu,yl,xg,yg,str]=grating(period,x0,y0)

%periode-grating period;
%d_c=duti_cycle{%};
h=20;
w=100;
N=100;
wwg=0.7;
i_plot=0;

xh=2; %additional width (basic=10)

[x1,y1]=line_cle(x0,y0,[0,20],[1+wwg/2,1+wwg/2]);
[x2,y2]=line_cle(x1(end),y1(end),[0,70],[0,(5-wwg/2+xh/2)]);
[x3,y3]=line_cle(x2(end),y2(end),[0,55],[0,0]);
[x4,y4]=line_cle(x3(end),y3(end),[0,70],[0,-(5-wwg/2+xh/2)]);
[x5,y5]=line_cle(x4(end),y4(end),[0,20],[0,0]);

x=[x1;x2;x3;x4;x5];
yu=[y1;y2;y3;y4;y5];

yl=-yu+2*y0;

% [x6,y6]=line_cle(x5(end),y5(end),[0,-70],[0,-4.65]);
% [x7,y7]=line_cle(x6(end),y6(end),[0,-65],[0,0]);
% [x8,y8]=line_cle(x7(end),y7(end),[0,-70],[0,4.65]);



%grating
size=20;

xg=zeros(floor(size/period),2);
yg=zeros(floor(size/period),2);

%xh=xh/2;        %for chg in sio2

for i=1:floor(size/period)
    xg(i,:)=[period*(0.5+(i-1)),period*(0.5+(i-1))];
    xg(i,:)=xg(i,:)+((235/2)-(size/2))+x0;
    yg(i,:)=[(5+xh/2)+y0,-(5+xh/2)+y0];
    if i_plot==1
        plot(xg(i,:),yg(i,:));
        hold on
    end
end

xg=xg';
yg=yg';

    %LOWER ARM

%y=2*h+s-y+0.7;         %UPPER ARM

%plot(x,y,x,yu);
if i_plot==1
    plot(x,yu,x,yl);
    axis equal
end
str=sprintf('P=%.3fum',period);
%
