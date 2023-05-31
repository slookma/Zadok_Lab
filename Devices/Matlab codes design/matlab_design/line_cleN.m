
%%straight
function[x,y]=line_cleN(x0,y0,xio,yio)

%L=40;

%xt=[-L/2;L/2];
xt=[xio(1);xio(2)];
yt=[yio(1);yio(2)];

%N=1e1*max([abs(xio(1)-xio(2)),abs(yio(1)-yio(2))]);

stepX=min([1 abs(xio(2)-xio(1))]);
stepY=min([1 abs(yio(2)-yio(1))]);

xt=[xio(1):stepX*sign(xio(2)-xio(1)):xio(2)];xt=xt';
yt=[yio(1):stepY*sign(yio(2)-yio(1)):yio(2)];yt=yt';

if length(xt)<=1
    xt=xio(1)*ones(size(yt));
elseif length(yt)<=1
    yt=yio(1)*ones(size(xt));
end

x=x0+xt;
y=y0+yt;

if diff(xio)==0 && diff(yio)==0
    x=x0;
    y=y0;
end

end