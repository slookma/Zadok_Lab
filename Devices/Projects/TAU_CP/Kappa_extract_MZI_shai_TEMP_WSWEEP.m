clc
clear all
% close all

W_start = 1540; % 1530;
W_end   = 1560; % 1570;
LorWsweep = 1; % 0: Wsweep, 1: new Wsweep, 2: Lsweep

params = struct('samplesNum', 18, 'batchNum', 4, 'xlabel', 'W [nm]');
samplesNum = params.samplesNum;
theta = 0:pi/10000:pi/2;
deltaL = 170e-6; % deltaL according to our design
alphaLin = 0.23*1400; % standard loss in our waveguides
ER_fit = ((exp(-alphaLin*deltaL)+tan(theta).^2)./(exp(-alphaLin*deltaL)-tan(theta).^2)).^2;

ER_fittest_bot_tot = zeros(samplesNum, 1);
ER_fittest_top_tot = zeros(samplesNum, 1);
kappa_bot          = zeros(samplesNum, 1);
kappa_top          = zeros(samplesNum, 1);
L                  = zeros(samplesNum, 1);

%%
% Wsweep_folders = {'U2','D2'};
Wsweep_folders = {'D2'}; % {'U2'};
folderNames = {fullfile('G:', 'users', 'Shai', 'TAU_CP', 'Data', '700to400_width_sweep_6Mar23'), fullfile('G:', 'users', 'Shai', 'TAU_CP', 'Data', '700to400_width_sweep_12Mar23')};
counter = 1;
for foldersNum = 1:length(folderNames)
    folderpath = folderNames{foldersNum};
    for batchNum = 1:length(Wsweep_folders)
        batchName = Wsweep_folders{batchNum};
        Folder = dir(fullfile(folderpath, ['*' batchName '*']));
        D = dir(fullfile(folderpath, Folder.name, '*nm*.txt*'));
        
        % Read D in a sensible order
        Lj = zeros(length(D), 1);
        for j = 1:length(D)
            if LorWsweep == 1
                Lj(j) = sscanf(D(j).name,'%dnm*');
            else
                Lj(j) = sscanf(D(j).name,'%dum*');
            end
        end
        [~, idx] = sort(Lj);
        
        % Find best way to subplot
        temp = factor(length(D));
        bestj = 1;
        for j = 1:length(temp)-1
            if (abs(prod(temp(1:j)) - prod(temp(j+1:end)))) < (abs(prod(temp(1:bestj)) - prod(temp(bestj+1:end))))
                bestj = j;
            end
        end
        subplotSize1 = prod(temp(1:bestj));
        subplotSize2 = prod(temp(bestj+1:end));
        
        figure
        for i = 1:length(D)
            L(counter) = sscanf(D(idx(i)).name,'%dnm*');
            filename = D(idx(i)).name;
            %%
            A = readtable(fullfile(folderpath, Folder.name, filename));
            Wavelength = A.XAxis_Wavelength_nm_;
            Loss       = A.InsertionLoss_dB_;
            
            %%
            span  = Wavelength > W_start & Wavelength < W_end;
            Loss = Loss(span);
            Wavelength = Wavelength(span);
            Loss_max = max(Loss);
            Loss_norm = Loss - Loss_max; % normalize
            
            %%
            [Mpeak, Lpeak, W, ER] = findpeaks(-Loss_norm, Wavelength, 'MinPeakDistance', 2, 'MinPeakWidth', 0.01);
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
            title({['L = ' num2str(L(counter)) ' \mum'], ['\kappa = ' num2str(kappa_bot(counter), '%.2f') ' / ' num2str(kappa_top(counter), '%.2f')]})
            
            %%
            counter = counter + 1;
        end
    end
end

%% Plot kappa vs. L
[Lsorted, LsortedIdx] = sort(L);
kappa_bot_sorted = kappa_bot(LsortedIdx);
kappa_top_sorted = kappa_top(LsortedIdx);

L = reshape(L, [9,2]);
kappa_bot = reshape(kappa_bot, [9,2]);
kappa_top = reshape(kappa_top, [9,2]);

mean_bot = mean(kappa_bot, 2);
mean_top = mean(kappa_top, 2);
errors_bot = std(kappa_bot, 1, 2);
errors_top = std(kappa_top, 1, 2);

figure
errorbar(L(:,1), mean_bot, errors_bot, '.', 'LineWidth', 1.5)
hold on
errorbar(L(:,1), mean_top, errors_top, '.', 'LineWidth', 1.5)
grid on
xlabel(params.xlabel, 'FontSize', 15)
ylabel('\kappa', 'FontSize', 20, 'Rotation', 0, 'HorizontalAlignment', 'right')
xlim([330 510])
ylim([0 1])
