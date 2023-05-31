function [Power] = comsol2matlab_c_verification( fileName,Dclad,ep,plots,method, diam)
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

% % % % fidi = fopen(fileName,'r');
% % % % data = textscan(fidi, '%f%f%f', 'HeaderLines',9, 'CollectOutput',1);
% % % % data = cell2mat(data);
% % % % 
% % % % xComs = data(:,1);
% % % % yComs = data(:,2);
% % % % PComs = data(:,3);
% % % % %dxComs = data(:,4);
% % % % %dyComs = data(:,5);


% T = readtable(fileName);
% xComs = str2double(split(table2array(T(10,1))));
% yComs = str2double(split(table2array(T(12,1))));
% PComs = str2double(split(table2array(T(14,1))));

T = readtable(fileName, 'Delimiter', '\t');
xComs = str2double(split(table2array(T(9,1))));
yComs = str2double(split(table2array(T(11,1))));
if diam == 550
    PComs = str2double(split(table2array(T(15,1))));
else
    PComs = str2double(split(table2array(T(13,1))));
end


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
rclad = max(xComs);
x = linspace(-rclad, rclad, 5e3);
[X, Y] = meshgrid(x);

% Power = griddata(xComs,yComs,PComs,X,Y,method);
% Power(isnan(Power)) = 0;

r_WG = diam*1e-9 / 2;
logical_WG_grid   = (X.^2 + Y.^2 <= r_WG^2);
logical_WG_nogrid = (xComs.^2 + yComs.^2 <= r_WG^2);

Power_in  = griddata(xComs,yComs,PComs.*logical_WG_nogrid,    X, Y);
Power_out = griddata(xComs,yComs,PComs.*(~logical_WG_nogrid), X, Y);

Power = Power_in.*logical_WG_grid + Power_out.*(~logical_WG_grid);
Power(isnan(Power)) = 0;

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