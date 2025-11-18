%% LIA connection
LIA = visa('agilent','USB0::0xB506::0x2000::003969::0::INSTR');
fopen(LIA);

%% Set RS and read lock in:

f_start     = 100e3;
f_stop      = 4e6;
Nf          = 201;
Tpause      = 0.2;
freqs       = logspace(log10(f_start), log10(f_stop), Nf);
powerR      = zeros(size(freqs));
powerR_av   = zeros(size(freqs));
powerX      = zeros(size(freqs));
powerY      = zeros(size(freqs));
N_av        = 1;
powerR_arr  = zeros(N_av, length(freqs));
powerX_arr  = zeros(N_av, length(freqs));
powerY_arr  = zeros(N_av, length(freqs));

WB = waitbar(0,'Please wait...');

tic
for idx_av = 1:N_av
    for idx = 1:Nf
        fprintf(LIA, ['FREQINT ' num2str(freqs(idx))]);
        pause(Tpause);
        fprintf(LIA, '%s\n',  'SNAP? 2,0,1');
        powerStr = fscanf(LIA);
        powerStr_split = split(powerStr, ',');
        powerR(idx) = double(string((powerStr_split(1))));
        powerX(idx) = double(string((powerStr_split(2))));
        powerY(idx) = double(string((powerStr_split(3))));

        waitbar(idx / length(freqs), WB, {['Please Hold, ' num2str(idx / length(freqs) * 100, '%.2f') '% completed. Iteration: ' num2str(idx_av)], ['Approximate Time Left: ' num2str((Nf - idx)*Tpause, '%.2f') '/' num2str(Nf*Tpause, '%.2f') ' sec.']});
    end
    
    powerR_arr(idx_av, :) = powerR;
    powerX_arr(idx_av, :) = powerX;
    powerY_arr(idx_av, :) = powerY;
end
toc

powerR_av = sum(powerR_arr, 1) / N_av;

close(WB)

% % Output on/off:
% OnOff = 0;
% fprintf(RS,[':OUTPut:ALL:STATe ' num2str(OnOff)]);

% powerR = powerR *0.41 / powerR(39);

% Plot R
figure
plotbrowser('on')
hold on
semilogy(freqs*1e-6, powerR, 'DisplayName', 'R')
semilogy(freqs*1e-6, powerX, 'DisplayName', 'X')
semilogy(freqs*1e-6, powerY, 'DisplayName', 'Y')
hold off

xlabel('$f$ [MHz]', 'Interpreter' , 'latex', 'FontSize', 15)
ylabel('Percentage [%]', 'FontSize', 15)

% 
% % Save the data
% filename = sprintf('Rafael_SIN_AU_strIpe.mat');
% save(filename, 'freqs', 'powerX', 'powerY', 'powerR');