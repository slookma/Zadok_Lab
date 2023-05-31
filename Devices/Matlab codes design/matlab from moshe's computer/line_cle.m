
%%straight
function[x,y]=line_cle(x0,y0,xio,yio)

%L=40;

%xt=[-L/2;L/2];
xt=[xio(1);xio(2)];
yt=[yio(1);yio(2)];

x=x0+xt;
y=y0+yt;

end