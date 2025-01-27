y_sim     = (0.2:0.1:0.9)'*1e-6;
neven_sim = [1.590688, 1.584119, 1.579750, 1.576689, 1.574478, 1.572851, 1.571639, 1.570728]';
nodd_sim  = [1.547180, 1.551920, 1.555684, 1.558603, 1.560833, 1.562525, 1.563803, 1.564768]';

L        = 62*1e-6;
H        = 47*1e-6;
y0_sweep = linspace(0.01,3,100)*1e-6;
OUT_tot  = zeros(size(y0_sweep));

idx = 1;
for y0 = y0_sweep

    z  = linspace(0,L,1000);
    dz = z(2) - z(1);
    y  = (H-y0)/2 * (1+cos(pi*z/L)) + y0;

    feven = fit(y_sim, neven_sim - mean(neven_sim+nodd_sim)/2, 'exp1');
    fodd  = fit(y_sim, nodd_sim  - mean(neven_sim+nodd_sim)/2, 'exp1');
    neven = feven.a*exp(feven.b*y) + mean(neven_sim+nodd_sim)/2;
    nodd  = fodd.a *exp(fodd.b*y)  + mean(neven_sim+nodd_sim)/2;
    Lc    = 1550e-9 ./ (2 * (neven - nodd));

    OUT_tot(idx) = sin(pi*dz * sum(1./Lc)).^2;
    idx = idx+1;
end

%%
figure
subplot(2,12,1:4)
plot(z*1e6,y*1e6, 'LineWidth',1.5)
grid on
xlabel('z [um]')
ylabel('y [um]')
% rectangle('Position',[190 110 710 30], 'FaceColor', 'w', 'EdgeColor', 'none')
% text(200,125, '$y = \frac{H-y_0}{2} \cdot \left[ 1 + \cos{(\pi z/L)} \right] + y_0$', 'Interpreter', 'latex', 'FontSize',12)

subplot(2,12,6:12)
plot(y0_sweep*1e6, OUT_tot, 'LineWidth',1.5)
grid on
xlabel('y0 [um]')
ylabel('L_{end} Coupling')

subplot(2,12,13:17)
semilogy(y*1e6,Lc, 'LineWidth',1.5)
grid on
xlabel('y [um]')
ylabel('Lc [m]')

subplot(2,12,20:24)
semilogy(z*1e6,Lc, 'LineWidth',1.5)
grid on
xlabel('z [um]')
ylabel('Lc [m]')
