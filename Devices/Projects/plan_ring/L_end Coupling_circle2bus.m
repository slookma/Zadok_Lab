%% Calculate coupling as a function of minimal gap, NO STRAIGHT SECTION
% Data from COMSOL:
Shai:
y_sim     = (0.2:0.1:0.9)'*1e-6; % [m]
neven_sim = [2.992085, 2.987510, 2.984189, 2.981771, 2.979920, 2.978539, 2.977463, 2.976653]';
nodd_sim  = [2.953587, 2.959000, 2.963029, 2.966059, 2.968240, 2.969853, 2.970995, 2.971831]';

% Fit to exponential curve:
feven = fit(y_sim, neven_sim - mean(neven_sim+nodd_sim)/2, 'exp1');
fodd  = fit(y_sim, nodd_sim  - mean(neven_sim+nodd_sim)/2, 'exp1');

% Parameters:
R           = 200*1e-6; % Radius of curvature [m]
y0_sweep    = linspace(0.01,3,100)*1e-6; % Sweep over minimal coupler gap [m]
alpha_sweep = linspace(10, 20, 10); % Propagation loss estimation [dB/cm]
OUT_tot     = zeros(size(y0_sweep));

idx = 1;
for y0 = y0_sweep
    % Define the shape of the coupler:
    z  = linspace(-R,0,1000);
    dz = z(2) - z(1);
    y  = y0 + R - sqrt(R^2 - z.^2);

    % Extrapolate n_even & n_odd according to the path + calculate Lc:
    neven = feven.a*exp(feven.b*y) + mean(neven_sim+nodd_sim)/2;
    nodd  = fodd.a *exp(fodd.b*y)  + mean(neven_sim+nodd_sim)/2;
    Lc    = 1550e-9 ./ (2 * (neven - nodd));

    % Calculate total coupling:
    OUT_tot(idx) = sin(pi*dz * sum(1./Lc)).^2;
    idx = idx+1;
end

%% Plot
figure
subplot(2,12,1:4)
plot(z*1e6,y*1e6, 'LineWidth',1.5)
grid on
xlabel('z [um]')
ylabel('y [um]')
title('Shape of the Coupler')

subplot(2,12,6:12)
plot(y0_sweep*1e6, OUT_tot, 'LineWidth',1.5)
grid on
xlabel('y0 [um]')
ylabel('L_{end} Coupling')
title('Couping VS. Minimal Gap')

subplot(2,12,13:17)
semilogy(y*1e6,Lc, 'LineWidth',1.5)
grid on
xlabel('y [um]')
ylabel('Lc [m]')
title('Lc VS. Gap')

subplot(2,12,20:24)
semilogy(z*1e6,Lc, 'LineWidth',1.5)
grid on
xlabel('z [um]')
ylabel('Lc [m]')
title('Lc VS. Z')

%% Calculate coupling as a function of straight section, GIVEN GAP
y0 = 200*1e-9; % Minimal coupler gap [m]
L_sweep = linspace(0,50,1000)*1e-6; % Sweep over straight section of coupler [m]
OUT_tot  = zeros(size(L_sweep));

idx = 1;
for L = L_sweep
    % Define the shape of the coupler:
    z  = linspace(-R,0,1000);
    dz = z(2) - z(1);
    y  = y0 + R - sqrt(R^2 - z.^2);

    % Extrapolate n_even & n_odd according to the path + calculate Lc:
    neven = feven.a*exp(feven.b*y) + mean(neven_sim+nodd_sim)/2;
    nodd  = fodd.a *exp(fodd.b*y)  + mean(neven_sim+nodd_sim)/2;
    Lc    = 1550e-9 ./ (2 * (neven - nodd));

    % Calculate total coupling:
    OUT_tot(idx) = sin(pi*dz * sum(1./Lc) + pi/2*L/Lc(end)).^2;
    idx = idx+1;
end

%%
figure
subplot(1,2,1)
plot(z*1e6,y*1e6, 'LineWidth',1.5)
grid on
xlabel('z [um]')
ylabel('y [um]')
title('Shape of the Coupler')

subplot(1,2,2)
plot(L_sweep*1e6, OUT_tot, 'LineWidth',1.5)
grid on
xlabel('L [um]')
ylabel('Total Coupling')
hold on
for alpha = alpha_sweep
    plot(L_sweep*1e6, 1-exp(-2*alpha/4.3429*(L_sweep + 2*pi*R)*100))
end
title('Couping VS. Coupler Straight Section')