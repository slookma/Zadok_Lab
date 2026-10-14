load("C:\Users\zadok.lab\Documents\GitHub\Zadok_Lab\Devices\Projects\SBS\SBS_setup\CHIP_261014\measurement_Chip430nm_AntiPump_10-12ghz_High_Pump.mat")
R_chip_antipump = powerR;
load("C:\Users\zadok.lab\Documents\GitHub\Zadok_Lab\Devices\Projects\SBS\SBS_setup\CHIP_261014\measurement_Chip430nm_NoAntiPump_10-12ghz_High_Pump.mat")
R_chip_noantipump = powerR;
freqs_chip = freqs;
load("C:\Users\zadok.lab\Documents\GitHub\Zadok_Lab\Devices\Projects\SBS\SBS_setup\CHIP_261014\measurement_FiberOnly_AntiPump_9-15ghz_Med_Pump.mat")
R_fiber_antipump = powerR;
load("C:\Users\zadok.lab\Documents\GitHub\Zadok_Lab\Devices\Projects\SBS\SBS_setup\CHIP_261014\measurement_FiberOnly_NoAntiPump_9-15ghz_Med_Pump.mat")
R_fiber_noantipump = powerR;
freqs_fiber = freqs;

%%
Normalize = 1;

figure
semilogy(freqs_chip*1e-9, R_chip_antipump*(Normalize/max(R_chip_antipump) + 1-Normalize), 'b', 'DisplayName', ['Chip ; Anti Pump ; SNR = ' num2str(max(R_chip_antipump)/mean(mink(R_chip_antipump,50)), '%.0f')])
hold on
semilogy(freqs_chip*1e-9, R_chip_noantipump*(Normalize/max(R_chip_noantipump) + 1-Normalize), 'r', 'DisplayName', ['Chip ; No Anti Pump ; SNR = ' num2str(max(R_chip_noantipump)/mean(mink(R_chip_noantipump,50)), '%.0f')])
semilogy(freqs_fiber*1e-9, R_fiber_antipump*(Normalize/max(R_fiber_antipump) + 1-Normalize), 'b--', 'DisplayName', ['Fiber ; Anti Pump ; SNR = ' num2str(max(R_fiber_antipump)/mean(mink(R_fiber_antipump,50)), '%.0f')])
semilogy(freqs_fiber*1e-9, R_fiber_noantipump*(Normalize/max(R_fiber_noantipump) + 1-Normalize), 'r--', 'DisplayName', ['Fiber ; No Anti Pump ; SNR = ' num2str(max(R_fiber_noantipump)/mean(mink(R_fiber_noantipump,50)), '%.0f')])

grid on
xlim([10 12])
lgd = legend;
fontsize(lgd, 14, 'points');
xlabel('freq. [GHz]')
ylabel('LIA Reading [norm.]')
set(gca, 'FontSize', 15)