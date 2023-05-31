clc
clear all
% close all

W_start = 1540; % 1530;
W_end   = 1560; % 1570;
LorWsweep = 1; % 0: Wsweep, 1: new Wsweep, 2: Lsweep

if LorWsweep == 0
    params = struct('samplesNum', 9,  'batchNum', 1, 'xlabel', 'W [nm]');
elseif LorWsweep == 1
    params = struct('samplesNum', 37, 'batchNum', 4, 'xlabel', 'W [nm]');
elseif LorWsweep == 2
    params = struct('samplesNum', 29, 'batchNum', 2, 'xlabel', 'L [\mum]');
end

samplesNum = params.samplesNum;
theta = 0:pi/10000:pi/2;
deltaL = 170e-6; % deltaL according to our design
alphaLin = 0.23*1400; % standard loss in our waveguides
ER_fit = ((exp(-alphaLin*deltaL)+tan(theta).^2)./(exp(-alphaLin*deltaL)-tan(theta).^2)).^2;

Wsweep_folders = {'U1','D1','U2','D2'};

ER_fittest_bot_tot = zeros(samplesNum, 1);
ER_fittest_top_tot = zeros(samplesNum, 1);
kappa_bot          = zeros(samplesNum, 1);
kappa_top          = zeros(samplesNum, 1);
L                  = zeros(samplesNum, 1);

%%
counter = 1;
for batchNum = 1:params.batchNum
    if LorWsweep == 0
        filepath = fullfile('G:', 'users', 'Shai', 'TAU_CP', 'Data', 'Wsweep');
        D = dir(fullfile(filepath, '*um*'));
    elseif LorWsweep == 1
        filepath = fullfile('G:', 'users', 'Shai', 'TAU_CP', 'Data', '700to400_width_sweep_6Mar23', ['700to400_width_sweep_6Mar23_' Wsweep_folders{batchNum}]);
        D = dir(fullfile(filepath, '*nm*.txt*'));
    elseif LorWsweep == 2
        filepath = fullfile('G:', 'users', 'Shai', 'TAU_CP', 'Data', 'New', ['batch' num2str(batchNum)]);
        D = dir(fullfile(filepath, '*um*'));
    end
    
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
        if LorWsweep == 1
            L(counter) = sscanf(D(idx(i)).name,'%dnm*');
        else
            L(counter) = sscanf(D(idx(i)).name,'%dum*');
        end
        
        filename = D(idx(i)).name;
        %%
        A = readtable(fullfile(filepath, filename));
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

%% Plot kappa vs. L
[Lsorted, LsortedIdx] = sort(L);
kappa_bot_sorted = kappa_bot(LsortedIdx);
kappa_top_sorted = kappa_top(LsortedIdx);

figure
scatter(Lsorted, kappa_bot_sorted, 'filled')
hold on
scatter(Lsorted, kappa_top_sorted, 'filled')
grid on
xlabel(params.xlabel, 'FontSize', 15)
ylabel('\kappa', 'FontSize', 20, 'Rotation', 0, 'HorizontalAlignment', 'right')
ylim([0 1])

%% Find set of kappa (choose bot/top for each L) that best fit a sin with 5<Lend<15 and 22<Lc<35
% For each L, we need to decide between kappa_bot and kappa_top.
% checking all permutations is too costly, so:
% if kappa_top > 0.7, we will choose the same branch as the previous point.
% else, we will insert this point into the permutation check set.
% 
% For each such permutation, we check correlation with a sine of a given
% Lc, Lend (looped over).
% 
% Finally, the highest correlation will tell us:
% 1. The best permutation
% 2. The best Lend
% 3. The best Lc

LendMin = 9;%5;
LendMax = 10;%15;
LcMin = 25;%22;
LcMax = 26;%35;
Lend_vec = linspace(LendMin, LendMax, 50);
Lc_vec   = linspace(LcMin,   LcMax,   50);

branchChoice = zeros(size(kappa_top_sorted)); % 1: top branch, 0: bottom branch
kappa_tot    = zeros(size(kappa_top_sorted));
skipIdx = (kappa_top_sorted > 0.7); % Indices to skip
Nperm = samplesNum - length(find(skipIdx)); % num of points to permute
permutations = ff2n(Nperm);
Corr = zeros(size(permutations, 1), length(Lend_vec), length(Lc_vec));

for permIdx = 1:size(permutations, 1)
    branchChoice(~skipIdx) = permutations(permIdx, :);
    for i = 2:samplesNum
        if skipIdx(i)
            branchChoice(i) = branchChoice(i-1);
        end
    end
    for LendIdx = 1:length(Lend_vec)
        for LcIdx = 1:length(Lc_vec)
            kappaFit = sin(pi/2* (Lsorted + Lend_vec(LendIdx)) / Lc_vec(LcIdx)).^2;
            kappa_tot(logical(branchChoice))  = kappa_top_sorted(logical(branchChoice));
            kappa_tot(~logical(branchChoice)) = kappa_bot_sorted(~logical(branchChoice));
            Corr(permIdx, LendIdx, LcIdx) = sum((kappaFit - mean(kappaFit)) .* (kappa_tot - mean(kappa_tot))) / samplesNum;
        end
    end
end


[M,I] = max(Corr(:)); %I is the index maximun Here tu can change the function to max or min
[permIdxBest, LendIdxBest, LcIdxBest] = ind2sub(size(Corr),I); %I_row is the row index and I_col is the column index
LendBest = Lend_vec(LendIdxBest);
LcBest = Lc_vec(LcIdxBest);

branchChoice(~skipIdx) = permutations(permIdxBest, :);
for i = 2:samplesNum
    if skipIdx(i)
        branchChoice(i) = branchChoice(i-1);
    end
end
kappa_tot(logical(branchChoice))  = kappa_top_sorted(logical(branchChoice));
kappa_tot(~logical(branchChoice)) = kappa_bot_sorted(~logical(branchChoice));


%% Final Plot
L_vec = linspace(Lsorted(1), Lsorted(end), 1000);
figure
plot(L_vec, sin(pi/2* (L_vec + LendBest) / LcBest).^2, 'LineWidth', 1.8)
hold on
plot(Lsorted, kappa_tot, '-o')
grid on
xlabel(params.xlabel, 'FontSize', 15)
ylabel('\kappa', 'FontSize', 15)
legend('Theory', 'Exp.')
text(80, 0.7,  ['L_{end} = ' num2str(LendBest, '%.2f')], 'HorizontalAlignment', 'left', 'FontSize', 12)
text(80, 0.8,  ['L_c = ' num2str(LcBest, '%.2f')],       'HorizontalAlignment', 'left', 'FontSize', 12)


