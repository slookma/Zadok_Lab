fig = gcf;
dataObjs = findobj(fig,'-property','YData');
manualShifts  = [0 0 0 0 -0.004 0 0 -0.006];
manualScaling = [1 1 1 0.9 1 1 1 1];

XData = zeros(350, length(dataObjs));
YData = zeros(350, length(dataObjs));

f1 = figure('Position', [200, 300, 690, 430]);
hold on
for idx = length(dataObjs):-1:1
    Detector = dataObjs(idx).YData;
    wavelength = dataObjs(idx).XData;
    DisplayName = dataObjs(idx).DisplayName;
    
    [pks, locs] = findpeaks(Detector, 'MinPeakProminence', 3);
    locsWL = wavelength(locs);
    pks    = pks(locsWL    > 1549.8);
    locs   = locs(locsWL   > 1549.8);
    locsWL = locsWL(locsWL > 1549.8);
    if (length(locsWL) == 3)
        df2 = (max(locsWL)-min(locsWL))*1e-9*3e8/(1550e-9)^2;
        scaling = 2*5e9/df2 * manualScaling(idx);
        wavelength = wavelength*scaling;
        shiftWL = wavelength(locs(2));
        wavelength = wavelength - (shiftWL - 1549.913) + manualShifts(idx);
    else
        scaling = 1 * manualScaling(idx);
        wavelength = wavelength*scaling;
        [~, shiftWL] = max(Detector);
        wavelength = wavelength - (wavelength(shiftWL) - 1549.913) + manualShifts(idx);
    end
    
    XData(:,idx) = wavelength;
    YData(:,idx) = Detector;
    
    plot(wavelength, Detector, 'DisplayName', DisplayName, 'LineWidth', 2)
    hold on
end

legend
xlim([1549.865 1550.15])
xlabel('Wavelength [nm]')
ylabel('Normalized Detector Reading [dB]')
set(gca, 'FontSize', 14)