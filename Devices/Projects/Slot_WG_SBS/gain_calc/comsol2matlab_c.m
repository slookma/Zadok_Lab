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

N = length(xComs);
%%
%figure
%plot(xComs,yComs,'x')
%%
rclad = Dclad/2;
x = -rclad:ep:rclad;
[X, Y] = meshgrid(x);
R = abs(X+1i*Y);
%mask = (R <= 62.5e-6);

Power = griddata(xComs,yComs,PComs,X,Y,method);
Power(isnan(Power)) = 0;

%% PLOT
% figure
% scatter(data(:,1), data(:,2), [], abs(data(:,3)), 'filled')
% hold on
% plot([-1,1]*2500  , [0, 0],       'k', 'linewidth', 2)
% plot([1 ,1]*(-170), [0, 1]*220,   'k', 'linewidth', 2)
% plot([1 ,1]*(+170), [0, 1]*220,   'k', 'linewidth', 2)
% plot([1 ,1]*(-20) , [0, 1]*220,   'k', 'linewidth', 2)
% plot([1 ,1]*(+20) , [0, 1]*220,   'k', 'linewidth', 2)
% plot([-170, -20]  , [1, 1]*220,   'k', 'linewidth', 2)
% plot([20  , 170]  , [1, 1]*220,   'k', 'linewidth', 2)

%%
toc
if plots == 1
    figure
    imagesc(x,x,abs(Power).^2);
    title(['Power, method = ' method])
    colormap jet
    colorbar
    set(gca,'YDir','normal');
end
end