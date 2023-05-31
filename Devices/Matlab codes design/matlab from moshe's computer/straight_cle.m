
%%straight
function[x,y]=straight_cle(x0,y0,L)

%L=40;

%xt=[-L/2;L/2];
xt=[0;L];
yt=[0;0];

x=x0+xt-xt(1);
y=y0+yt-yt(1);

end