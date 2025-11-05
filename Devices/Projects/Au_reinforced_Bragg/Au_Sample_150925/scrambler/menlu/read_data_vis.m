% --- Polarization Filter Data Analysis ---
% This script reads CSV files ring_1.csv ... ring_13.csv
% Each file has the format:
%   x-axis   2
%   second   Volt
%   <time>   <value>

clear; clc; close all

nFiles = 13;
results = zeros(nFiles, 3); % columns: [mean, std, std/mean]

for k = 1:nFiles
    filename = sprintf('ring_%d.csv', k);
    fprintf('Processing %s...\n', filename);

    % --- Read data ---
    opts = detectImportOptions(filename, 'NumHeaderLines', 2);
    data = readtable(filename, opts);

    % Extract columns (assuming 2 columns: time and voltage)
    time = data{:,1};
    value = data{:,2};

    % --- Compute statistics ---
    m = mean(value);
    s = std(value);
    ratio = s / m;

    results(k,:) = [m, s, ratio];
    fprintf('File %d: mean = %.4g, std = %.4g, std/mean = %.4g\n', k, m, s, ratio);

    % --- Plot signal ---
    figure('Name', sprintf('ring_%d', k), 'NumberTitle', 'off');
    subplot(2,1,1)
    plot(time, value, 'LineWidth', 1)
    xlabel('Time [s]')
    ylabel('Voltage [V]')
    title(sprintf('ring\\_%d signal', k))
    grid on

    % --- Plot histogram ---
    subplot(2,1,2)
    histogram(value, 50, 'FaceColor', [0.2 0.6 0.8])
    xlabel('Voltage [V]')
    ylabel('Count')
    title('Histogram')
    grid on
end

% --- Summary table ---
T = array2table(results, ...
    'VariableNames', {'Mean', 'Std', 'std_over_Mean'}, ...
    'RowNames', compose('ring_%d', 1:nFiles));
disp('--- Summary ---');
disp(T);

x = 0:0.01:1;
y = (1-x)./(sqrt(2)*(1+x));
plot(x,y)