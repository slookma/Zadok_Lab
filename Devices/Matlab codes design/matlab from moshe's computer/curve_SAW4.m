function[x,y,x1i,y1i,x2i,y2i,W,Ww]=curve_SAW3(W,D,x0,y0,ss)
%%Inputs
% W: Tap's weight
% D: length of tap sagment
% x0,y0: starting point
% ss = direction
%%Outputs
%x,y: x&y vectors coordinats
%x1i,y1i,x2i,y2i: detection area borders
%W: Tap's weight
%Ww: = Wavegiude width duo to weight
%%
% clear all;clc
% x0=0;
% y0=0;
% N=200;
W = 0.5;
D = 150;
x0 = 0;
y0 = 0;
ss = -1;


flag_plot=1;

L=1.4;  %acoustic wavelength
R=50;
Y_T=abs(D);
Ys=90;      %extended saw segment
Ysaw=60;    %estimated saw aperture
ex=5;
Yt=(Y_T-Ys-2*ex)/2;

q=2*pi/L;

% Ww=0.7:0.001:1.4;
% Wsim=0.5*(1-cos(2*pi*Ww/L));

Ww=0.7:0.001:4;
load('p_w3new.mat');
Wsim=polyval(p,Ww*1e3);

if flag_plot==1
figure(4)
    plot(Ww,Wsim,'r');
end
    
[ww,iw]=min(abs(Wsim-W));
Ww=Ww(iw);
if W==1
    Ww=0.7;
end
%

if flag_plot==1
    line([Ww Ww],[min([Wsim]) max([Wsim])]);
end

x=zeros(9,1);
y=zeros(9,1);

x(1)=x0;y(1)=y0;
x(2)=x(1);y(2)=y(1)-ex;
x(3)=x(2)+ss*(Ww/2-0.7/2);y(3)=y(2)-Yt;
x(4)=x(3);y(4)=y(3)-(Ys-Ysaw)/2;
x(5)=x(4);y(5)=y(4)-(Ysaw)/2;
x(6)=x(5);y(6)=y(5)-(Ysaw)/2;
x(7)=x(6);y(7)=y(6)-(Ys-Ysaw)/2;
x(8)=x(7)-ss*(Ww/2-0.7/2);y(8)=y(7)-Yt;
x(9)=x(8);y(9)=y(8)-ex;

x1i=x(4);y1i=y(4);
x2i=x(6);y2i=y(6);
    
if sign(D)==1
    y=-y+2*y0;
    x=-x+2*x0;
    y1ii=-y1i+2*y0;
    y2ii=-y2i+2*y0;
    x1ii=-x1i+2*x0;
    x2ii=-x2i+2*x0;
    y1i=y1ii;
    y2i=y2ii;
    x1i=x1ii;
    x2i=x2ii;
end

if flag_plot==1
    figure(5)
    plot(x,y);hold on;plot(x1i,y1i,'r*');plot(x2i,y2i,'b*');
    str=sprintf('W = %.3f',W);
    title(str);
%     axis equal
    % grid on
end

%%