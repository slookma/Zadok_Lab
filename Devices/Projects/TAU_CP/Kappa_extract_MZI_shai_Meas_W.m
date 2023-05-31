clc
clear all
close all

%%
W_start = 1540; % 1530;
W_end   = 1560; % 1570;

sorter = [];
D = dir(fullfile('Data', 'Wsweep_AFM_Only', '6Mar23', 'D1', '*.txt'));
sorter(1:length(D)) = 1;
D = [D ; dir(fullfile('Data', 'Wsweep_AFM_Only', '6Mar23', 'U1', '*.txt'))];
sorter(length(sorter)+1 : length(D)) = 2;
D = [D ; dir(fullfile('Data', 'Wsweep_AFM_Only', '6Mar23', 'D2', '*.txt'))];
sorter(length(sorter)+1 : length(D)) = 3;
D = [D ; dir(fullfile('Data', 'Wsweep_AFM_Only', '6Mar23', 'U2', '*.txt'))];
sorter(length(sorter)+1 : length(D)) = 4;
sorter = sorter';

samplesNum = length(D);
theta = 0:pi/10000:pi/2;
deltaL = 170e-6; % deltaL according to our design
alphaLin = 0.23*1400; % standard loss in our waveguides
ER_fit = ((exp(-alphaLin*deltaL)+tan(theta).^2)./(exp(-alphaLin*deltaL)-tan(theta).^2)).^2;

ER_fittest_bot_tot = zeros(samplesNum, 1);
ER_fittest_top_tot = zeros(samplesNum, 1);
kappa_bot          = zeros(samplesNum, 1);
kappa_top          = zeros(samplesNum, 1);
W                  = zeros(samplesNum, 1);
WRef               = zeros(samplesNum, 1);
CP                 = zeros(samplesNum, 1);
location           = cell(samplesNum, 1);

%%
Wmeas_T = readtable(fullfile('results', 'W_design_vs_meas.txt'));
counter = 1;
for CP_idx = 1:2
    idxGroup = (sorter == 2*CP_idx-1) | (sorter == 2*CP_idx);
    D_i = D(idxGroup);
    
    % Find best way to subplot
    temp = factor(length(D_i));
    bestj = 1;
    for j = 1:length(temp)-1
        if (abs(prod(temp(1:j)) - prod(temp(j+1:end)))) < (abs(prod(temp(1:bestj)) - prod(temp(bestj+1:end))))
            bestj = j;
        end
    end
    subplotSize1 = prod(temp(1:bestj));
    subplotSize2 = prod(temp(bestj+1:end));
    
    fig = figure;
    for i = 1:length(find(idxGroup))
        
        % Find correct line from Wmeas_T according to D_i
        branches = split(D_i(i).folder, '\');
        classification = char(branches(end));
        if classification(1) == 'D'
            location_i = 'down';
        elseif classification(1) == 'U'
            location_i = 'up';
        end
        chipNum = classification(2);
        WRef_i = D_i(i).name;
        WRef_i = str2double(WRef_i(1:3));
        
        idx2save = find((table2array(Wmeas_T(:, 1)) == str2double(chipNum)) & strcmp(table2array(Wmeas_T(:, 2)), location_i) & (table2array(Wmeas_T(:, 3)) == WRef_i*1e-3));
        W(counter)        = (table2array(Wmeas_T(idx2save, 4)) + table2array(Wmeas_T(idx2save, 5)))/2 * 1e3;
        WRef(counter)     = WRef_i;
        CP(counter)       = str2double(chipNum);
        location(counter) = cellstr(location_i);
        
        %%
        A = readtable(fullfile(D_i(i).folder, D_i(i).name));
        Wavelength = A.XAxis_Wavelength_nm_;
        Loss       = A.InsertionLoss_dB_;
        
        %%
        span  = Wavelength > W_start & Wavelength < W_end;
        Loss = Loss(span);
        Wavelength = Wavelength(span);
        Loss_max = max(Loss);
        Loss_norm = Loss - Loss_max; % normalize
        
        %%
        [Mpeak, Lpeak, ~, ER] = findpeaks(-Loss_norm, Wavelength, 'MinPeakDistance', 2, 'MinPeakWidth', 0.01);
        [mER, LER] = max(ER);
        
        if LER == length(Lpeak)
            FSR = abs(Lpeak(LER) - Lpeak(LER-1));
        else
            FSR = abs(Lpeak(LER) - Lpeak(LER+1));
        end
        
        logical_span = Wavelength>Lpeak(LER)-0.5*FSR & Wavelength<Lpeak(LER)+0.5*FSR;
        peak_span = Wavelength(logical_span);
        peak_mag = Loss_norm(logical_span);
        
        %%
        Max_ER = min(peak_mag) - max(peak_mag);
        ER_Lin = db2pow(-Max_ER);
        ER_sort = abs(ER_fit - ER_Lin);
        
        [~, ER_fittest_index_bot] = sort(ER_sort(1:ceil(length(ER_sort)/2)));
        [~, ER_fittest_index_top] = sort(ER_sort(ceil(length(ER_sort)/2):end));
        ER_fittest_index_top = ER_fittest_index_top + ceil(length(ER_sort)/2);
        
        Theta_bot = theta(ER_fittest_index_bot(1));
        Theta_top = theta(ER_fittest_index_top(1));
        
        kappa_bot(counter) = sin(Theta_bot)^2; % (1-cos(Theta_bot)^2);
        kappa_top(counter) = sin(Theta_top)^2; % (1-cos(Theta_top)^2);
        ER_fittest_bot_tot(counter) = ER_fit(ER_fittest_index_bot(1));
        ER_fittest_top_tot(counter) = ER_fit(ER_fittest_index_top(1));
        
        
        %% Plot Luna
        subplot(subplotSize1, subplotSize2, i)
        plot(Wavelength, Loss_norm)
        grid on
        xlabel('\lambda [nm]')
        ylabel('Loss')
        ylim([-30 0])
        title({['W = ' num2str(W(counter), '%.1f') ' nm'], ['\kappa = ' num2str(kappa_bot(counter), '%.2f') ' / ' num2str(kappa_top(counter), '%.2f')]})
        %%
        counter = counter + 1;
    end
end

%% Plot kappa vs. W
fig = figure('Position', [200 200 1000 500]);
for CP_i = 1:2
    subplot(1,2,CP_i)
    scatter(W(CP == CP_i), kappa_bot(CP == CP_i), 'filled')
    hold on
    scatter(W(CP == CP_i), kappa_top(CP == CP_i), 'filled')
    grid on
    xlabel('W (Measured) [nm]', 'FontSize', 15)
    ylabel('\kappa', 'FontSize', 20, 'Rotation', 0, 'HorizontalAlignment', 'right')
    ylim([0 1])
    title(['CP' num2str(CP_i)])
end

