%%
clc
close all
clear all
delete(instrfindall)
%% LIA connection
LIA = visa('agilent','USB0::0xB506::0x2000::003969::0::INSTR');
fopen(LIA);
% %%
fprintf(LIA, '%s\n', '*IDN?');
idn_LIA = fscanf(LIA)
% %% LIA take data
% fprintf(LIA, '%s\n',  'SNAP? 2,3,15');
% powerStr = fscanf(LIA);
% commaP = find(powerStr==',');
% powerR = str2double(powerStr(1:(commaP-1)));
%% RS connection
RS = visa('agilent','TCPIP0::10.11.68.12::inst0::INSTR');
fopen(RS);
fprintf(RS, '%s\n', '*IDN?');
idn_RS = fscanf(RS)
% %% RS set output
% % RS_SetFreq = @(freq)(['FREQ ' num2str(freq) ' KHz']); ???
% 
% % Set frequency:
% freq = 10e3;
% fprintf(RS,['SOURce1:FREQuency:CW ' num2str(freq)]);
% 
% % Set power:
% power = -10; % dBm
% fprintf(RS,['SOURce1:POWer:POWer ' num2str(power)]);
% 
% % Output on/off:
% OnOff = 0;
% fprintf(RS,[':OUTPut:ALL:STATe ' num2str(OnOff)]);
% 

%% Scope connection (Small Keysight DSOX3034A)
% scope = visadev('USB0::0x0957::0x17A4::MY54232198::0::INSTR');
% idn = writeread(scope, "*IDN?");
% % Open connection
% fopen(scope);


%% Scope connection (Small Keysight MSO7034A)
% scope = visadev('USB0::0x0957::0x1735::MY48260106::0::INSTR');
% idn = writeread(scope, "*IDN?");
% % Open connection
% fopen(scope);


%% Scope connection (Large Agilent DSO90604A)
scope = visa('agilent','USB0::0x0957::0x9005::MY50520105::0::INSTR');
scope.InputBufferSize = 1024 * 1024 * 4;
fopen(scope);

% % Scope commands

scope_set_channel = @(Channel)([':WAV:SOUR CHAN',num2str(Channel)]);
scope_read_query = @(scope)(str2num(query(scope,':WAVeform:Data?')));
scope_count = @(scope)(str2num(query(scope,':WAV:COUNT?')));
scope_average = @(Averages)([':ACQuire:AVERage:COUNt ' ,num2str(Averages)]);
scope_set_sample_rate = @(Srate)([':ACQuire:SRATe:ANALog ' num2str(Srate)]);

Srate = 20e9;
dt = 1/Srate;
fprintf(scope,scope_set_sample_rate(Srate));
Averages = 256;
Channel = 1;
Nt = length(scope_read_query(scope));
time = (0:1:(Nt-1))*dt;

%% Set RS and read lock in:
% Measurement Device
Dev = 1; % 1 - LIA ; 2 - small scope ; 3 - DSO scope; 4 - MSO scope

% Set power:
power = 23; % dBm
fprintf(RS,['SOURce1:POWer:POWer ' num2str(power)]);

% Output on/off:
OnOff = 1;
 
fprintf(RS,[':OUTPut:ALL:STATe ' num2str(OnOff)]);

f_start     = 10.5e9;
f_stop      = 11.5e9;
Nf          = 201;
Tpause      = 0.5;
freqs       = linspace(f_start, f_stop, Nf);
df          = (freqs(2) - freqs(1))*1e-6; % MHz
powerR      = zeros(size(freqs));
powerR_av   = zeros(size(freqs));
powerX      = zeros(size(freqs));
powerY      = zeros(size(freqs));
vpp         = zeros(size(freqs));
N_av        = 1;
powerR_arr  = zeros(N_av, length(freqs));
powerX_arr  = zeros(N_av, length(freqs));
powerY_arr  = zeros(N_av, length(freqs));
Sig         = zeros(length(time), length(freqs));

WB = waitbar(0,'Please wait...');

Testimate = Nf*Tpause;
Tcurrent  = 0;

for idx_av = 1:N_av
    for idx = 1:Nf
        if idx == 1
            Tstart = tic;
        else
            Tcurrent = toc(Tstart);
            Testimate = Tcurrent*(Nf-1)/(idx-1);
        end
        fprintf(RS,['SOURce1:FREQuency:CW ' num2str(freqs(idx), '%.2f')]);
        
        % Perform Measurement
        switch Dev
            case 1
                fprintf(LIA, '%s\n',  'SNAP? 2,0,1');
                powerStr = fscanf(LIA);
                powerStr_split = split(powerStr, ',');
                powerR(idx) = double(string((powerStr_split(1))));
                powerX(idx) = double(string((powerStr_split(2))));
                powerY(idx) = double(string((powerStr_split(3))));
                pause(Tpause);
            case 2
                fprintf(scope, ':MEASure:VPP CHAN1');   % Set measurement type
                pause(Tpause);
                
                % Measure Vpp in scope
                fprintf(scope, ':MEASure:VPP? CHAN1');
                vpp(idx) = str2double(fscanf(scope));
            case 3
                pause(0.5)
                fwrite(scope, scope_average(Averages))
                
                fprintf(scope,'single');
                while (scope_count(scope) <Averages) %wait to finish averaging
                    pause(0.01)
                    scope_count(scope);
                end
                % If waiting fails, wait a certain time:
                % pause(5)
                fwrite(scope, scope_set_channel(1));
                Sig(:,idx) = scope_read_query(scope);
            case 4
                % ???????

        end

        waitbar(idx/Nf, WB, {['Please Hold, ' num2str(idx/Nf * 100, '%.2f') '% completed. Iteration: ' num2str(idx_av)], ['Approximate Time Left: ' num2str(Tcurrent, '%.2f') '/' num2str(Testimate, '%.2f') ' sec.']});
    end
    
    powerR_arr(idx_av, :) = powerR;
    powerX_arr(idx_av, :) = powerX;
    powerY_arr(idx_av, :) = powerY;
end

powerR_av = sum(powerR_arr, 1) / N_av;

close(WB)

% % Output on/off:
% OnOff = 0;
% fprintf(RS,[':OUTPut:ALL:STATe ' num2str(OnOff)]);

gL = 1.7;         % Measured every day [W^-1]
pIn = -9.8;       % dBm at tap
pIn = pIn + 16.8; % dBm at DUT
sensitivity = 1000; % in LIA [uv]
ppm = (exp(gL*(db2pow(pIn))/1000)-1)*1e6; % Fiber
% ppm = (exp(16.98*0.008*(db2pow(pIn-13))/1000)-1)*1e6; % Device
ppm1 = round(ppm);

for x = 1
% % Plot X
% figure 
% plotbrowser('on')
% plot(freqs*1e-9, powerX,'DisplayName',['ppm = ' num2str(ppm1)])
% xlabel('$f$ [GHz]', 'Interpreter', 'latex', 'FontSize', 15)
% ylabel('Amplitude [V]', 'FontSize', 15)
% title([num2str(ppm1) 'ppm, $\tau = 300ms$, X amplitude'], 'Interpreter', 'latex')

% % Plot Y
% figure 
% plotbrowser('on')
% plot(freqs*1e-9, powerY,'DisplayName',['ppm = ' num2str(ppm1)])
% xlabel('$f$ [GHz]', 'Interpreter', 'latex', 'FontSize', 15)
% ylabel('Amplitude [V]', 'FontSize', 15)
% title([num2str(ppm1) 'ppm, $\tau = 300ms$, Y amplitude'], 'Interpreter', 'latex')
end


switch Dev
    case 1
        % % Plot R
        figure
        % plotbrowser('on')
        % hold on
        semilogy(freqs*1e-9, powerR, 'DisplayName', ['R, ppm = ' num2str(ppm1), 'pump = ' num2str(pIn), ' dbm']);%'R  ,','ppm = ' num2str(ppm1) ', diff., Sens. = ' num2str(sensitivity) 'uV'])
        % semilogy(freqs*1e-9, powerX, 'DisplayName', ['X, ppm = ' num2str(ppm1), 'pump = ' num2str(pIn), ' dbm']);%['X ,','ppm = ' num2str(ppm1) ', diff., Sens. = ' num2str(sensitivity) 'uV'])
        % semilogy(freqs*1e-9, powerY, 'DisplayName', ['Y, ppm = ' num2str(ppm1), 'pump = ' num2str(pIn), ' dbm']);%['Y ,','ppm = ' num2str(ppm1) ', diff., Sens. = ' num2str(sensitivity) 'uV'])
        % hold off
        % plot(freqs*1e-9, powerR,'DisplayName',['gain  ,','ppm = ' num2str(ppm1) ', diff., Sens. = ' num2str(sensitivity) 'uV'])
        xlabel('$f$ [GHz]', 'Interpreter' , 'latex', 'FontSize', 15)
        ylabel('Amplitude [V]', 'FontSize', 15)
        % % title([num2str(ppm1) 'ppm, $\tau = 300ms$','Sens. = ' num2str(sensitivity) '[uV]'], 'Interpreter', 'latex')
        % % title(['$\tau = 300ms$, R amplitude'], 'Interpreter', 'latex')
        %
        % % % % Plot phase
        % % % yyaxis right
        % % % phase = atan2(powerY,powerX);
        % % % plot(freqs*1e-9, phase,'DisplayName',['phase  ,','ppm = ' num2str(ppm1)])
        % % % xlabel('$f$ [GHz]', 'Interpreter' , 'latex', 'FontSize', 15)
        % % % ylabel('radians', 'FontSize', 15)
        % % % grid on

        % % % Save the data
        % % filename = sprintf('fiber_only.mat', pIn);
        % % save(filename, 'freqs', 'fiber_only');

        % figure
        % semilogy(freqs*1e-9, vpp)
        % xlabel('$f$ [GHz]', 'Interpreter' , 'latex', 'FontSize', 15)
        % ylabel('Vpp [V]', 'FontSize', 15)
        % title('P_{Pump} = 12.1dBm (Average)')
    case 3
        figure
        imagesc(time*1e9,freqs*1e-9,Sig')
        set(gca,'YDir','normal')
        xlabel('Time [ns]')
        ylabel('Freq. [GHz]')
end

%%
figure
subplot(2,2,1)
imagesc(freqs*1e-9,time*1e9, Sig_10ns_SMFDS)
set(gca,'YDir','normal')
ylabel('Time [ns]')
xlabel('Freq. [GHz]')
title('10ns Pulse')
% xlim([10.7 11.05])
% ylim([30 70])
colorbar

subplot(2,2,2)
imagesc(freqs*1e-9,time*1e9, Sig_10_5ns_SMFDS)
set(gca,'YDir','normal')
ylabel('Time [ns]')
xlabel('Freq. [GHz]')
title('10.5ns Pulse')
% xlim([10.7 11.05])
% ylim([30 70])
colorbar

subplot(2,2,3.5)
imagesc(freqs*1e-9,time*1e9, diff_sig_10ns_SMFDS)
set(gca,'YDir','normal')
ylabel('Time [ns]')
xlabel('Freq. [GHz]')
title('Difference between 10ns/10.5ns')
% xlim([10.7 11.05])
% ylim([30 70])
colorbar

sgtitle('SMF + DS + long SMF (Pump side)')

%%
freqs_dense = linspace(freqs(1),freqs(end),10000);
counter = 1;
leftFWHM_50ns_vec  = 0;
rightFWHM_50ns_vec = 0;
leftFWHM_55ns_vec  = 0;
rightFWHM_55ns_vec = 0;
times_vec = 0;
figure
for idx = 2000:10:6000
    Sig_50ns_shortPS_temp = interp1(freqs, Sig_50ns_shortPS(idx,:), freqs_dense, "spline");
    Sig_55ns_shortPS_temp = interp1(freqs, Sig_55ns_shortPS_shift(idx,:), freqs_dense, "spline");

    plot(freqs_dense*1e-9, Sig_50ns_shortPS_temp)
    ylim([-0.1 0.7])
    hold on
    plot(freqs_dense*1e-9, Sig_55ns_shortPS_temp)
    drawnow
    hold off

    [pks_50ns, locs_50ns] = findpeaks(Sig_50ns_shortPS_temp, 'MinPeakProminence', 0.1);
    [pks_55ns, locs_55ns] = findpeaks(Sig_55ns_shortPS_temp, 'MinPeakProminence', 0.1);
    if (length(pks_55ns) ~= 2) || (length(pks_50ns) ~= 2)
        continue
    end

    

    left_cross_up_50ns = find(diff(Sig_50ns_shortPS_temp-pks_50ns(1)/2>=0) == 1);
    left_cross_up_50ns = left_cross_up_50ns(left_cross_up_50ns<5000);
    left_cross_dn_50ns = find(diff(Sig_50ns_shortPS_temp-pks_50ns(1)/2>=0) == -1);
    left_cross_dn_50ns = left_cross_dn_50ns(left_cross_dn_50ns<5000)+1;

    right_cross_up_50ns = find(diff(Sig_50ns_shortPS_temp-pks_50ns(2)/2>=0) == 1);
    right_cross_up_50ns = right_cross_up_50ns(right_cross_up_50ns>5000);
    right_cross_dn_50ns = find(diff(Sig_50ns_shortPS_temp-pks_50ns(2)/2>=0) == -1);
    right_cross_dn_50ns = right_cross_dn_50ns(right_cross_dn_50ns>5000)+1;

    leftFWHM_50ns  = (freqs_dense(left_cross_dn_50ns)  - freqs_dense(left_cross_up_50ns)) *1e-6;
    rightFWHM_50ns = (freqs_dense(right_cross_dn_50ns) - freqs_dense(right_cross_up_50ns))*1e-6;



    left_cross_up_55ns = find(diff(Sig_50ns_shortPS_temp-pks_55ns(1)/2>=0) == 1);
    left_cross_up_55ns = left_cross_up_55ns(left_cross_up_55ns<5000);
    left_cross_dn_55ns = find(diff(Sig_50ns_shortPS_temp-pks_55ns(1)/2>=0) == -1);
    left_cross_dn_55ns = left_cross_dn_55ns(left_cross_dn_55ns<5000)+1;

    right_cross_up_55ns = find(diff(Sig_50ns_shortPS_temp-pks_55ns(2)/2>=0) == 1);
    right_cross_up_55ns = right_cross_up_55ns(right_cross_up_55ns>5000);
    right_cross_dn_55ns = find(diff(Sig_50ns_shortPS_temp-pks_55ns(2)/2>=0) == -1);
    right_cross_dn_55ns = right_cross_dn_55ns(right_cross_dn_55ns>5000)+1;

    leftFWHM_55ns  = (freqs_dense(left_cross_dn_55ns)  - freqs_dense(left_cross_up_55ns)) *1e-6;
    rightFWHM_55ns = (freqs_dense(right_cross_dn_55ns) - freqs_dense(right_cross_up_55ns))*1e-6;
    
    if (length(leftFWHM_50ns) ~= 1) || (length(rightFWHM_50ns) ~= 1) || (length(leftFWHM_55ns) ~= 1) || (length(rightFWHM_55ns) ~= 1)
        continue
    end

    leftFWHM_50ns_vec(counter)  = leftFWHM_50ns;
    rightFWHM_50ns_vec(counter) = rightFWHM_50ns;

    leftFWHM_55ns_vec(counter)  = leftFWHM_55ns;
    rightFWHM_55ns_vec(counter) = rightFWHM_55ns;

    times_vec(counter)          = time(idx);

    hold on
    text(freqs_dense(locs_50ns(1))*1e-9, pks_50ns(1), ['FWHM (50ns) = ' num2str(leftFWHM_50ns,  '%.0f')], 'VerticalAlignment','bottom', 'HorizontalAlignment','center')
    text(freqs_dense(locs_50ns(2))*1e-9, pks_50ns(2), ['FWHM (50ns) = ' num2str(rightFWHM_50ns, '%.0f')], 'VerticalAlignment','bottom', 'HorizontalAlignment','center')
    text(freqs_dense(locs_55ns(1))*1e-9, pks_55ns(1), ['FWHM (55ns) = ' num2str(leftFWHM_50ns,  '%.0f')], 'VerticalAlignment','top',    'HorizontalAlignment','center')
    text(freqs_dense(locs_55ns(2))*1e-9, pks_55ns(2), ['FWHM (55ns) = ' num2str(rightFWHM_50ns, '%.0f')], 'VerticalAlignment','top',    'HorizontalAlignment','center')
    
    drawnow
    pause(0.1)
    hold off
    counter = counter + 1;
end


figure
subplot(1,2,1)
plot(times_vec*1e9, leftFWHM_50ns_vec)
hold on
plot(times_vec*1e9, leftFWHM_55ns_vec)
xlabel('time [ns]')
ylabel('FWHM [MHz]')
legend('50ns', '55ns')

subplot(1,2,2)
plot(times_vec*1e9, rightFWHM_50ns_vec)
hold on
plot(times_vec*1e9, rightFWHM_55ns_vec)
xlabel('time [ns]')
ylabel('FWHM [MHz]')
legend('50ns', '55ns')

%%
freqs_dense = linspace(freqs(1),freqs(end),10000);
temp = Sig_55ns_shortPS_shift(2801:4401,:);
counter = 1;
left_peak_freqs  = 0;
right_peak_freqs = 0;
times_vec = 0;
for idx = 1:size(temp,1)
    temp2 = interp1(freqs, temp(idx,:), freqs_dense);
    [pks, locs] = findpeaks(temp2, 'MinPeakProminence', 0.1);

    if length(pks) ~= 2
        continue
    end

    left_peak_freqs(counter)  = freqs_dense(locs(1));
    right_peak_freqs(counter) = freqs_dense(locs(2));
    times_vec(counter) = time(2800 + idx);
    counter = counter + 1;
end


left_peak  = mean(left_peak_freqs);
right_peak = mean(right_peak_freqs);


%%
Sig_left = Sig_55ns_shortPS_shift(:,1:round(end/2));
Sig_right = Sig_55ns_shortPS_shift(:,round(end/2):end);
freqs_left = freqs(1:round(end/2));
freqs_right = freqs(round(end/2):end);

[~, left_peak_loc]  = min(abs(left_peak  - Sig_left(3801, :)));
[~, right_peak_loc] = min(abs(right_peak - Sig_right(3801, :)));

for scale = [45 47.5 50 52.5 55 57.5 60 62.5 65]/55
    Sig_left_new  = (squeeze_y_anchor(Sig_left',  scale, left_peak_loc, 'max'))';
    Sig_right_new = (squeeze_y_anchor(Sig_right', scale, right_peak_loc, 'max'))';

    Sig_55ns_shortPS_sqz = [Sig_left_new(:,1:end-1) , Sig_right_new];

    diff_sig_sqz = abs(Sig_55ns_shortPS_sqz - Sig_50ns_shortPS);

    figure
    imagesc(time*1e9,freqs*1e-9,diff_sig_sqz')
    set(gca,'YDir','normal')
    xlabel('Time [ns]')
    ylabel('Freq. [GHz]')
    title({['diff 50/55ns with shift & Scaling: ' num2str(scale*55)],'0.5m Pure Silica'})
    xlim([120 250])
end

%%
function B = squeeze_y_anchor(A, scale, y0, combineMode)
% squeeze_y_anchor  Squeeze in Y around a fixed anchor row y0.
%
% A: Ny x Nx map
% scale < 1  -> squeeze (compress vertically)
% y0: anchor row index (can be non-integer if you want sub-row anchoring)
% combineMode: 'last' (default) or 'max' for collisions

if nargin < 4, combineMode = 'last'; end

[Ny, Nx] = size(A);
B = zeros(Ny, Nx);

src = (1:Ny).';                         % all source rows
dst = round(y0 + scale*(src - y0));     % forward map around anchor

valid = (dst >= 1) & (dst <= Ny);
src = src(valid);
dst = dst(valid);

switch lower(combineMode)
    case 'last'
        % If multiple src map to same dst, the later src overwrites earlier (simple & fast)
        B(dst, :) = A(src, :);

    case 'max'
        % If collisions happen, keep the per-column maximum (often preserves peaks better)
        for x = 1:Nx
            B(:,x) = accumarray(dst, A(src,x), [Ny 1], @max, 0);
        end

    otherwise
        error("combineMode must be 'last' or 'max'.");
end
end

