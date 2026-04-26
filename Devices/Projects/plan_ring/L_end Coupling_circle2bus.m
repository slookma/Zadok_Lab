%% Calculate coupling as a function of minimal gap, NO STRAIGHT SECTION
% Data from COMSOL:
% % Leroy:
y_sim     = (0.2:0.1:0.9)'*1e-6; % [m]
% neven_sim = [1.78069, 1.77824, 1.77676, 1.77585, 1.77528, 1.77491, 1.77469].';
% nodd_sim  = [1.76867, 1.77061, 1.77190, 1.77274, 1.77329, 1.77364, 1.77388].';
% neven_sim = [1.84417, 1.84195, 1.84085, 1.84026, 1.83992, 1.83972, 1.83960, 1.83953, 1.83949].';
% nodd_sim  = [1.83667, 1.83759, 1.83823, 1.83867, 1.83895, 1.83913, 1.83924, 1.83931, 1.83935].';

% Si3N4 300nm thickness X 1um width
% neven_sim = [1.7042216981667582, 1.6969075318418623, 1.6923412186959979, 1.6893705643165267, 1.6874071600397356, 1.6861004621632423, 1.6852199262362264, 1.684611616387299]';
% nodd_sim  = [1.6653854678124203, 1.670694973981679,  1.6745698454066558, 1.67729546181444,   1.6791819595664643, 1.6804844927247788, 1.6813775101964235, 1.6819780524984074]';

% Si3N4 350nm thickness X 1um width
neven_sim = [1.800453074270154, 1.793306803788649, 1.7892131011151116, 1.78677127384149, 1.785290609597843, 1.7843721668427786, 1.783789066262875, 1.7834250458890295]';
nodd_sim  = [1.76838676848287, 1.773350497641052, 1.7767075490182944, 1.7789020773312874, 1.7803233791932598, 1.781226755363197, 1.7817933991567592, 1.7821558404258648]';

% Fit to exponential curve:
feven = fit(y_sim, neven_sim - mean(neven_sim+nodd_sim)/2, 'exp1');
fodd  = fit(y_sim, nodd_sim  - mean(neven_sim+nodd_sim)/2, 'exp1');

% Parameters:
% Leroy:
R           = 100*1e-6; % Radius of curvature [m]
y0_sweep    = linspace(0.01,3,100)*1e-6; % Sweep over minimal coupler gap [m]
alpha_sweep = linspace(0.5, 5, 11); % Propagation loss estimation [dB/cm]
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