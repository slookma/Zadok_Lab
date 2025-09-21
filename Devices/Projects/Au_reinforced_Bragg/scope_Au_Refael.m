%% Read Data
Norm  = 1;
bound = 1;
CH    = 2;

path = 'Au_Sample_150925/ring7au.csv';
[t_Au_ring7,probe_Au_ring7,t_Au_ring7_sect,probe_Au_ring7_sect] = read_scope_data(path,Norm,bound,CH);

path = 'Au_Sample_150925/ring7au_invert.csv';
[t_Au_ring7Inv,probe_Au_ring7Inv,t_Au_ring7Inv_sect,probe_Au_ring7Inv_sect] = read_scope_data(path,Norm,bound*2,CH);

CH = 3;
pathList = {'no_au_sample_22_895.csv',...
            'no_au_sample_23_555.csv',...
            'no_au_sample_23_605.csv',...
            'no_au_sample_23_645.csv',...
            'no_au_sample_23_875.csv'};
for idx = 1:5
    path = fullfile('noAu_Sample_180925',pathList{idx});
    if idx == 4
        bound = 2;
    else
        bound = 1;
    end
    [t_noAu{idx},probe_noAu{idx},t_noAu_sect{idx},probe_noAu_sect{idx}] = read_scope_data(path,Norm,bound,CH);
end

%% Extract decay time (CH2)
fitdata_Au_ring7 = fit(t_Au_ring7_sect*1e6, probe_Au_ring7_sect, 'exp1');
fitdata_Au_ring7Inv = fit(t_Au_ring7Inv_sect(30:end)*1e6, probe_Au_ring7Inv_sect(30:end), 'exp1');
fitdata_noAu_2 = fit(t_noAu_sect{2}*1e6, probe_noAu_sect{2}, 'exp1');
fitdata_noAu_4 = fit(t_noAu_sect{4}*1e6, probe_noAu_sect{4}, 'exp1');

%% Plot LUNA
diode_temps = [22.895, 23.555, 23.605, 23.645, 23.875];
OSA_WLs     = [1556.548, 1556.614, 1556.618, 1556.624, 1556.646];
LUNA_WLs    = OSA_WLs + 0.699-0.646;

LUNA_data     = readtable('noAu_Sample_180925/Refael_LUNA/ring_8_no_Au_Shai_meas.txt');
LUNAmeas_WL   = LUNA_data.XAxis_Wavelength_nm_;
LUNAmeas_Loss = LUNA_data.InsertionLoss_dB_;

figure
plot(LUNAmeas_WL, LUNAmeas_Loss, 'LineWidth', 1.5)
xlim([1556.55 1556.75])
OSA_WLs     = [1556.548, 1556.614, 1556.618, 1556.624, 1556.646];
LUNA_WLs    = OSA_WLs + 0.699-0.646;
xline(LUNA_WLs, 'LineWidth', 1.2)
xlabel('Wavelength [nm]')
ylabel('Insertion Loss [dB]')
title({'Scope Measurements Taken vs. LUNA Curve', 'Ring 8, No Au Sample'})
ylim([-15 -7])
for idx = 1:5
    text(LUNA_WLs(idx), -8.5-1.5*(idx-1), num2str(LUNA_WLs(idx)), 'HorizontalAlignment', 'left', 'VerticalAlignment', 'bottom', 'Rotation', 90)
end

%% Plot Au Sample
figure
subplot(2,2,[1 3])
plot(t_Au_ring7*1e6, probe_Au_ring7, 'LineWidth', 1.5)
hold on
plot(t_Au_ring7Inv*1e6, probe_Au_ring7Inv, 'LineWidth', 1.5)
xlabel('time [\mus]')
legend('Gold \rightarrow Ring', 'Ring \rightarrow Gold')

subplot(2,2,2)
plot(t_Au_ring7_sect*1e6, probe_Au_ring7_sect, 'LineWidth', 1.5)
hold on
plot(t_Au_ring7_sect*1e6, fitdata_Au_ring7.a*exp(fitdata_Au_ring7.b*t_Au_ring7_sect*1e6), 'LineWidth', 1.5)
confData = confint(fitdata_Au_ring7);
xlabel('time [\mus]')
title({'Gold \rightarrow Ring (Single Period)',['\tau = ' num2str(-1/fitdata_Au_ring7.b, '%.2f') ' \mus'],['95% Confidence: ' num2str(-1/confData(1,2), '%.2f') '-' num2str(-1/confData(2,2), '%.2f') '\mus']})

subplot(2,2,4)
plot(t_Au_ring7Inv_sect*1e6, probe_Au_ring7Inv_sect, 'LineWidth', 1.5)
hold on
plot(t_Au_ring7Inv_sect*1e6, fitdata_Au_ring7Inv.a*exp(fitdata_Au_ring7Inv.b*t_Au_ring7Inv_sect*1e6), 'LineWidth', 1.5)
confData = confint(fitdata_Au_ring7Inv);
xlabel('time [\mus]')
title({'Ring \rightarrow Gold (Single Period)',['\tau = ' num2str(-1/fitdata_Au_ring7Inv.b, '%.2f') ' \mus'],['95% Confidence: ' num2str(-1/confData(1,2), '%.2f') '-' num2str(-1/confData(2,2), '%.2f') '\mus']})

fontsize(13,"points")

%% Plot No Au Sample
figure
for idx = 1:5
    plot(t_noAu{idx}*1e6, probe_noAu{idx} + 2e-3*(idx-1), 'LineWidth', 1.5)
    hold on
end
xlabel('time [\mus]')
legend(num2str(LUNA_WLs'))

fontsize(13,"points")

figure
subplot(2,1,1)
plot(t_noAu_sect{2}*1e6, probe_noAu_sect{2}, 'LineWidth', 1.5)
hold on
plot(t_noAu_sect{2}*1e6, fitdata_noAu_2.a*exp(fitdata_noAu_2.b*t_noAu_sect{2}*1e6), 'LineWidth', 1.5)
confData = confint(fitdata_noAu_2);
xlabel('time [\mus]')
title({['Probe WL = ' num2str(LUNA_WLs(2)) ' nm'],['\tau = ' num2str(-1/fitdata_noAu_2.b, '%.2f') ' \mus'],['95% Confidence: ' num2str(-1/confData(1,2), '%.2f') '-' num2str(-1/confData(2,2), '%.2f') '\mus']})

subplot(2,1,2)
plot(t_noAu_sect{4}*1e6, probe_noAu_sect{4}, 'LineWidth', 1.5)
hold on
plot(t_noAu_sect{4}*1e6, fitdata_noAu_4.a*exp(fitdata_noAu_4.b*t_noAu_sect{4}*1e6), 'LineWidth', 1.5)
confData = confint(fitdata_noAu_4);
xlabel('time [\mus]')
title({['Probe WL = ' num2str(LUNA_WLs(4)) ' nm'],['\tau = ' num2str(-1/fitdata_noAu_4.b, '%.2f') ' \mus'],['95% Confidence: ' num2str(-1/confData(1,2), '%.2f') '-' num2str(-1/confData(2,2), '%.2f') '\mus']})

fontsize(13,"points")


%%
figure
subplot(2,3, [1 4])
plot(LUNAmeas_Loss, LUNAmeas_WL, 'LineWidth', 1.5)
set(gca, 'YDir', 'reverse')
ylim([1556.55 1556.75])
OSA_WLs     = [1556.548, 1556.614, 1556.618, 1556.624, 1556.646];
LUNA_WLs    = OSA_WLs + 0.699-0.646;
yline(LUNA_WLs, 'LineWidth', 1.2)
ylabel('Wavelength [nm]')
xlabel('Insertion Loss [dB]')
title({'Scope Measurements Taken vs. LUNA Curve', 'Ring 8, No Au Sample'})
xlim([-15 -7])
for idx = 1:5
    text(-8.5-1.5*(idx-1), LUNA_WLs(idx), num2str(LUNA_WLs(idx)), 'HorizontalAlignment', 'left', 'VerticalAlignment', 'bottom')
end

subplot(2,3,[2 5])
for idx = 5:-1:1
    plot(t_noAu{idx}*1e6, probe_noAu{idx} + 2e-3*(idx-1), 'LineWidth', 1.5)
    hold on
end
xlabel('time [\mus]')
legend(num2str(LUNA_WLs'))


subplot(2,3,3)
plot(t_noAu_sect{2}*1e6, probe_noAu_sect{2}, 'LineWidth', 1.5)
hold on
plot(t_noAu_sect{2}*1e6, fitdata_noAu_2.a*exp(fitdata_noAu_2.b*t_noAu_sect{2}*1e6), 'LineWidth', 1.5)
confData = confint(fitdata_noAu_2);
xlabel('time [\mus]')
title({['Probe WL = ' num2str(LUNA_WLs(2)) ' nm'],['\tau = ' num2str(-1/fitdata_noAu_2.b, '%.2f') ' \mus'],['95% Confidence: ' num2str(-1/confData(1,2), '%.2f') '-' num2str(-1/confData(2,2), '%.2f') '\mus']})

subplot(2,3,6)
plot(t_noAu_sect{4}*1e6, probe_noAu_sect{4}, 'LineWidth', 1.5)
hold on
plot(t_noAu_sect{4}*1e6, fitdata_noAu_4.a*exp(fitdata_noAu_4.b*t_noAu_sect{4}*1e6), 'LineWidth', 1.5)
confData = confint(fitdata_noAu_4);
xlabel('time [\mus]')
title({['Probe WL = ' num2str(LUNA_WLs(4)) ' nm'],['\tau = ' num2str(-1/fitdata_noAu_4.b, '%.2f') ' \mus'],['95% Confidence: ' num2str(-1/confData(1,2), '%.2f') '-' num2str(-1/confData(2,2), '%.2f') '\mus']})




fontsize(13,"points")


% % % %% Approach 2 - Three points sample
% % % figure
% % % hold on
% % % for k = 1:90
% % %     sample1_ring7 = CH2_Au_ring7_sect(1);
% % %     sample2_ring7 = CH2_Au_ring7_sect(k+1);
% % %     sample3_ring7 = CH2_Au_ring7_sect(2*k+1);
% % %     rho = (sample1_ring7 - sample2_ring7)/(sample1_ring7 - sample3_ring7);
% % %     tau = (t_Au_ring7_sect(k+1) - t_Au_ring7_sect(1))*1e6/log(rho/(1-rho));
% % %     plot(k,tau,'k*')
% % % end
% % % 
% % % % figure
% % % hold on
% % % for k = 1:90
% % %     sample1_Ring7Inv = CH2_Au_ring7Inv_sect(1);
% % %     sample2_Ring7Inv = CH2_Au_ring7Inv_sect(k+1);
% % %     sample3_Ring7Inv = CH2_Au_ring7Inv_sect(2*k+1);
% % %     rho = (sample1_Ring7Inv - sample2_Ring7Inv)/(sample1_Ring7Inv - sample3_Ring7Inv);
% % %     tau = (t_Au_ring7Inv_sect(k+1) - t_Au_ring7Inv_sect(1))*1e6/log(rho/(1-rho));
% % %     plot(k,tau,'r*')
% % % end
% % % 
% % % 
% % % %% Approach 3 - derivative
% % % derv_ring7_sect = diff(CH2_Au_ring7_sect)./diff(t_Au_ring7_sect);
% % % 
% % % figure
% % % plot(t_Au_ring7_sect(2:end)*1e6, derv_ring7_sect)
% % % hold on
% % % 
% % % %% Approach 4 - Frequency Domain
% % % dt = t_Au_ring7_sect(2)-t_Au_ring7_sect(1);
% % % Fs = 1/dt;
% % % % figure


