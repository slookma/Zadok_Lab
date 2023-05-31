%%
clear
clc
close all

%% Constants
lambda = 1550e-9;
k0 = 2*pi/lambda;

L    = linspace(0, 100, 1000); % [um]
Lend = 19; % [um]

W_model_or_meas = 0; % 0 - modeled , 1 - measured

%% Prepare data
if W_model_or_meas == 0 % Modeled
    D = dir(fullfile('Model', '*.txt'));
elseif W_model_or_meas == 1 % Measured
    D = dir(fullfile('Model', 'model_exp', '*.txt'));
end
N = length(D);

W     = zeros(N,1);
Lc    = zeros(N,1);
kappa = zeros(N, length(L));

%% Compute Lc for each W and plot
f1 = figure('Position', [200, 400, 800, 400]);
for i = 1:N
    tx = D(i).name;
    if W_model_or_meas == 0 % Modeled
        W(i) = str2double(tx(10:12));
        lgnd{i} = ['$W = ' num2str(W(i)) ' nm$'];
    elseif W_model_or_meas == 1 % Measured
        W_idx = str2double(tx(tx>=48 & tx <=57));
        W(i) = (Wmeas_T.W1(W_idx) + Wmeas_T.W2(W_idx))/2 * 1e3;
        lgnd{i} = ['$W = ' num2str(W(i), '%.1f') ' nm$'];
    end
    
    T = readtable(fullfile(D(i).folder, D(i).name));
    
    n_even = table2array(T(1,end));
    n_odd  = table2array(T(1,end-1));
    
    beta_odd  = n_odd*k0;
    beta_even = n_even*k0;
    
    S = (beta_even - beta_odd)/2;
    Lc(i) = pi./(2*S);
    
    kappa(i, :) = sin(pi/2 * (L+Lend)/(Lc(i)*1e6)).^2;
end

if W_model_or_meas == 1 % Measured
    [W, order] = sort(W);
    kappa = kappa(order, :);
end
for i = 1:N
    plot(L, kappa(i, :), 'Color', [(N-i+1)/N , 0, (i-1)/N], 'LineWidth', 1.6)
    hold on
end


xline(51, '--k', 'LineWidth', 1.5);
text(51, 0.7, '$51 \mu m$', 'Interpreter', 'latex', 'Rotation', 90, 'VerticalAlignment', 'bottom', 'FontSize', 12)
grid on
title(['Wsweep Model ; $L_{\textrm{end}} = ' num2str(Lend) ' \mu m$'], 'FontSize', 15, 'Interpreter', 'latex')
xlabel('$L [\mu m]$', 'FontSize', 15, 'Interpreter', 'latex')
ylabel('\kappa', 'Rotation', 0, 'HorizontalAlignment', 'right', 'FontSize', 15)
legend(lgnd, 'Location', 'northeastoutside', 'Interpreter', 'latex', 'FontSize', 12)

%% Compute intersections with L = 51um
[~, I_intersect] = min(abs(L-51));
figure
scatter(W, kappa(:, I_intersect),   '*k')
hold on
scatter(W, 1-kappa(:, I_intersect), '*k')





