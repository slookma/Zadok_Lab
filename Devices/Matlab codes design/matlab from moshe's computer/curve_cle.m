
function[x,y]=curve_cle(x0,y0,ai,ao,R,N)

%w=100;
%h=10;
%N=100;

angle=linspace(ai,ao,N);
c=R*exp(1i*angle);

xt=real(c);
yt=imag(c);

x=x0+xt-xt(1);
y=y0+yt-yt(1);

x=x';
y=y';

% plot(x,y);
% axis equal
% text(x(1),y(1),'\leftarrow start')
% text(x(end),y(end),'\leftarrow end')
end