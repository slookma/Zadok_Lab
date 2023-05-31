
%%straight
function[x,y]=straight_ex_cle(x0,y0,L)

%L=40;

%xt=[-L/2;L/2];
xt=[0;0];
yt=[0;L];

x=x0+xt-xt(1);
y=y0+yt-yt(1);

end