
function[x,yu,yl,xg,yg,str]=grating_m(period,x0,y0)

%periode-grating period;
%d_c=duti_cycle{%};
h=20;
w=100;
N=100;

size_x=60;
size_y=60;

[x1,y1]=line_cle(x0,y0,[0,20],[1.35,1.35]);
[x2,y2]=line_cle(x1(end),y1(end),[0,70],[0,4.65]);
[x3,y3]=line_cle(x2(end),y2(end),[0,55],[0,0]);
[x4,y4]=line_cle(x3(end),y3(end),[0,70],[0,-4.65]);
[x5,y5]=line_cle(x4(end),y4(end),[0,20],[0,0]);

x=[x1;x2;x3;x4;x5];
yu=[y1;y2;y3;y4;y5];

yl=-yu;

% [x6,y6]=line_cle(x5(end),y5(end),[0,-70],[0,-4.65]);
% [x7,y7]=line_cle(x6(end),y6(end),[0,-65],[0,0]);
% [x8,y8]=line_cle(x7(end),y7(end),[0,-70],[0,4.65]);



%grating

xg=zeros(floor(size_y/period),2);
yg=zeros(floor(size_y/period),2);

for i=1:floor(size_y/period)
    xg(i,:)=[period*(0.5+(i-1)),period*(0.5+(i-1))];
    xg(i,:)=xg(i,:)+x0;
    yg(i,:)=[size_x/2+y0,-size_x/2+y0];
    plot(xg(i,:),yg(i,:));
    hold on
end

xg=xg';
yg=yg';

    %LOWER ARM

%y=2*h+s-y+0.7;         %UPPER ARM

%plot(x,y,x,yu);
plot(x,yu,x,yl);
axis equal

str=sprintf('P=%.1fum',period*1e0);
%
