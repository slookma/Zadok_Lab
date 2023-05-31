close all
clear
clc

%% Read AFM .txt data and deduce widths
verbose = 1;

% folderPath = 'CP_ref_AFM_340nm_to_400nm';
folderPath = 'All_AFM_data_WSweep';
D = dir(fullfile(folderPath, '*.txt'));

W1     = zeros(length(D), 1);
W2     = zeros(length(D), 1);
WREF   = zeros(length(D), 1);
Labels = cell(length(D),1);

for i = 1:length(D)
    A = readtable(fullfile(folderPath, D(i).name));
    Labels{i} = D(i).name;
%     [pks, locs] = findpeaks(abs(gradient(A.nm)), 'MinPeakDistance', 10, 'MinPeakProminence', 20);
    A.nm = smooth(A.nm, 10);
    [pks, locs] = findpeaks(max([gradient(gradient(A.nm)), zeros(length(A.nm),1)], [], 2), 'MinPeakDistance', 10, 'MinPeakProminence', 1);
    W1(i)   = A.x_m(locs(4)) - A.x_m(locs(3));
    W2(i)   = A.x_m(locs(2)) - A.x_m(locs(1));
    
    startIndex = regexp(Labels{i},'_REF');
    WREF(i) = sscanf(Labels{i}(startIndex+4:end),'%d')/1e3;
    
    if verbose
        figure
        plot(A.x_m, A.nm, '-o')
        grid on
        hold on
%         plot(A.x_m, abs(gradient(A.nm)), '-o')
        plot(A.x_m, max([gradient(gradient(A.nm)), zeros(length(A.nm),1)], [], 2), '-o')
        scatter(A.x_m(locs), pks, 'k', 'filled')
    end
end

Wall = [WREF, W1, W2] * 1e3;

%% Divide into CP1 and CP2
CP_divide = zeros(length(Labels), 1);
for i = 1:length(Labels)
    Label_i = char(Labels(i));
    CP_divide(i) = str2num(Label_i(3));
end

%% Plot
fig = figure('Position', [200 200 1000 500]);
for CP_idx = 1:2
    subplot(1,2,CP_idx)
    idxGroup = (CP_divide == CP_idx);
    scatter([Wall(idxGroup,1) ; Wall(idxGroup,1)], [Wall(idxGroup,2) ; Wall(idxGroup,3)], 'filled')
    hold on
    plot([min(Wall(idxGroup,1)) max(Wall(idxGroup,1))], [min(Wall(idxGroup,1)) max(Wall(idxGroup,1))], '--k')
    grid on
    xlim([min(Wall(idxGroup,1))*0.95 max(Wall(idxGroup,1))*1.05])
    ylim([min(min(Wall))*0.95 max(max(Wall))*1.05])
    xlabel('Designed Width [nm]')
    ylabel('Measured Width [nm]')
    
    fit = polyfit([Wall(idxGroup,1) ; Wall(idxGroup,1)], [Wall(idxGroup,2) ; Wall(idxGroup,3)], 1);
    plot(sort(Wall(idxGroup,1)), sort(Wall(idxGroup,1))*fit(1) + fit(2), '--r')
    
    minDes  = min(Wall(idxGroup,1));
    maxDes  = max(Wall(idxGroup,1));
    minMeas = min(sort(Wall(idxGroup,1))*fit(1) + fit(2));
    maxMeas = max(sort(Wall(idxGroup,1))*fit(1) + fit(2));
    
    mean_dev = ((minDes - minMeas) + (maxDes - maxMeas))/2;
    text((minDes + maxDes)/2, maxDes, ['Mean Deviation = ' num2str(mean_dev, '%.2f') ' nm'], 'FontSize', 13, 'HorizontalAlignment', 'center')
%     text(minDes, (minDes + minMeas)/2, [num2str(minDes - minMeas, '%.1f') ' nm'], 'FontSize', 13, 'HorizontalAlignment', 'center')
%     text(maxDes, (maxDes + maxMeas)/2, [num2str(maxDes - maxMeas, '%.1f') ' nm'], 'FontSize', 13, 'HorizontalAlignment', 'center')
    
    title(['CP ' num2str(CP_idx)], 'FontSize', 13)
    legend({'Designed W', 'Measured W', 'Fit'}, 'Location', 'southeast')
end

%% Save a table of 
saveTable = 0;
if saveTable
    CP   = zeros(length(Labels),1);
    Side = cell(length(Labels),1);
    for i = 1:length(Labels)
        Label_i = char(Labels(i));
        CP(i) = str2double(Label_i(3));
        
        Label_i = split(Label_i, '_');
        Side(i) = Label_i(3);
    end
    
    Labels_T = table(CP, Side, WREF, W1, W2);
    writetable(Labels_T, fullfile('results', 'W_design_vs_meas.txt'));
end

