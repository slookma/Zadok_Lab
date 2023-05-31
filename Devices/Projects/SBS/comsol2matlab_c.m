function [Power] = comsol2matlab_c( fileName,Dclad,ep,plots,method )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

%%
if nargin < 3
    ep = 1;
end
if nargin < 4
    plots = 1;
end
if nargin < 5
    method = 'cubic';
end

tic
%data = load(fileName);

fidi = fopen(fileName,'r');
data = textscan(fidi, '%f%f%f', 'HeaderLines',9, 'CollectOutput',1);
data = cell2mat(data);


xComs = data(:,1);
yComs = data(:,2);
PComs = data(:,3);
%dxComs = data(:,4);
%dyComs = data(:,5);

%  ddComs = sqrt(dxComs.^2+dyComs.^2);
%  figure
%  plot3(xComs,yComs,ddComs)
%
% rComs = sqrt(xComs.^2+yComs.^2);
% tComs = atan2(yComs,xComs);
% sinComs = sin(tComs);
% cosComs = cos(tComs);
% drComs = dxComs.*cosComs + dyComs.*sinComs;
% dtComs = dyComs.*cosComs - dxComs.*sinComs;
%
% figure
% plot3(xComs,yComs,drComs)
%
% figure
% plot3(xComs,yComs,dtComs)

N = length(xComs);
%%
%figure
%plot(xComs,yComs,'x')
%%
rclad = Dclad/2;
x = -rclad:ep:rclad;
[X Y] = meshgrid(x);
R = abs(X+1i*Y);
%mask = (R <= 62.5e-6);

Power = griddata(xComs,yComs,PComs,X,Y,method);
Power(find(isnan(Power))) = 0;


%%
toc
%%
%  figure
%  imagesc(x,x,dABS);
%  title(['abs displacement '])
%  colorbar
if plots == 1
    figure
    imagesc(x,x,abs(Power).^2);
    title(['Power, method = ' method])
    colormap jet
    colorbar
    set(gca,'YDir','normal');
end
end