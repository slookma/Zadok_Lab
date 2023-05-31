clc
clear all
close all
%% add Matlab toolbox path

addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\mltoolbox\clewin\clewin'));
%% Adiabatic coupler

input_w = 10; %um
output_w = 0.7;%um

Adiabatic_lngth = 100;%um
contour = 5;%um

%%
adiabatic_WG_cord = [0 -Adiabatic_lngth -Adiabatic_lngth 0;input_w/2 output_w/2 -output_w/2 -input_w/2];
adiabatic_Countor_cord = [0 -Adiabatic_lngth -Adiabatic_lngth 0;(input_w+contour)/2 (output_w+contour)/2 -(output_w+contour)/2 -(input_w+contour)/2];
adiabatic_WG = clePolygon(adiabatic_WG_cord);
adiabatic_Countor = clePolygon(adiabatic_Countor_cord);
adiabatic_XOR = cleXOR(adiabatic_WG,adiabatic_Countor);
%cleDraw(adiabatic_WG)
%% Gratting
period = 0.6;%um
DC = 0.5;
gratting_w = input_w;%um
lngth = 15;%um
gratting_num = floor(lngth/period);
gratting = adiabatic_XOR;%zeros(4,2);
for i=0:(gratting_num-1)
    gratt_cord = [0+period*i period*DC+period*i period*DC+period*i 0+period*i;gratting_w/2 gratting_w/2 -gratting_w/2 -gratting_w/2];
    gratt = clePolygon(gratt_cord);
    gratting = cleGroup(gratting,gratt);
end
gratting_contour = clePolygon([0 period*DC+period*i period*DC+period*i 0; (gratting_w+contour)/2 (gratting_w+contour)/2 (-gratting_w-contour)/2 (-gratting_w-contour)/2]);
gratting_XOR = cleXOR(gratting,gratting_contour);
adiabatic_WG_mirror = cleMirror(adiabatic_XOR,[(period*DC+period*i)/2 0 pi/2]);
gratting_XOR = cleGroup(gratting_XOR,adiabatic_WG_mirror);
gratting_XOR = cleTranslate(gratting_XOR,[Adiabatic_lngth 0]);
cleDraw(gratting_XOR)


%% Bus

WG_w = 0.7; %um
lngth = -3000;%um
contour = 5;%um

bus_WG_cord = [0 lngth lngth 0;WG_w/2 WG_w/2 -WG_w/2 -WG_w/2];
bus_Countor_cord = [0 lngth lngth 0;(WG_w+contour)/2 (WG_w+contour)/2 -(WG_w+contour)/2 -(WG_w+contour)/2];
bus_WG = clePolygon(bus_WG_cord)
bus_Countor = clePolygon(bus_Countor_cord);
bus = cleXOR(bus_WG,bus_Countor);
cleDraw(bus)


%% Qaurter circle

R = 25;%um
WG_w = 0.7;%um
contour = 5;%um
x = 100;
y = 100;
numOfpoints = 100;
%% l
teta = 0:0.5*pi/numOfpoints:0.5*pi;
xP = x-R+R*sin(teta);
yP = y+R*cos(teta);
plot(xP,yP,'.g')
%% d
teta = 0.5*pi:0.5*pi/numOfpoints:pi;
xP = x-R+R*sin(teta);
yP = y+R*cos(teta);
plot(xP,yP,'.g')

%% u
teta = pi:0.5*pi/numOfpoints:1.5*pi;
xP = x+R*sin(teta);
yP = y+R+R*cos(teta);
plot(xP,yP,'.g')
%% r
teta = 1.5*pi:0.5*pi/numOfpoints:2*pi;
xP = x+R+R*sin(teta);
yP = y+R*cos(teta);
plot(xP,yP,'.g')



