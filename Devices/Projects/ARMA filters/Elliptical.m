%% Elliptical Filter
%------1----------3-----
%------2----------4-----
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 15dB e2e loss
% k1 = 0.942
% k2 = 0.942
% k3 = 0.484
% k4 = 0.484
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Optimal Rejection Ratio (13.10):
% % Voltages:   (4)  14.4796 V ; 3.1  mA (Ring 3)
% %             (6)  9.6087  V ; 2.8  mA (Ring 1)
% %             (9)  4.9491  V ; 15.6 mA (MZI)
% %             (11) 6.442   V ; 1    mA (Ring 2)
% %             (12) 11.8969 V ; 2.9  mA (Ring 4)
% % WITH TEC (10kohm, 25deg):
% % Voltages:   (4)  15.4894 V ; 3.9 mA (Ring 3)
% %             (6)  11.9177 V ; 3.9 mA (Ring 1)
% %             (9)  5.1252  V ; 17  mA (MZI)
% %             (11) 11.145  V ; 3   mA (Ring 2)
% %             (12) 13.5738 V ; 4.2 mA (Ring 4)
% % Phases:      0.88*pi (Ring 1)
% %             -0.88*pi (Ring 2)
% %             -0.35*pi (Ring 3)
% %              0.35*pi (Ring 4)
% %             -0.49*pi (MZI)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Optimal Flatness (14.10):
% % Voltages:   (4)  6.5604  V ; 1.2  mA (Ring 3)
% %             (6)  11.1292 V ; 3.5  mA (Ring 1)
% %             (9)  4.2493  V ; 12.8 mA (MZI)
% %             (11) 11.011  V ; 2    mA (Ring 2)
% %             (12) 2.3299  V ; 0.5  mA (Ring 4)
% % WITH TEC (10kohm, 25deg):
% % Voltages:   (4)  6.5302 V ; 1.2  mA (Ring 3)
% %             (6)  8.1089 V ; 2.7  mA (Ring 1)
% %             (9)  3.6232 V ; 12.8 mA (MZI)
% %             (11) 10.513 V ; 3    mA (Ring 2)
% %             (12) 3.3522 V ; 1.1  mA (Ring 4)
% % Phases:      0.76*pi (Ring 1)
% %             -0.76*pi (Ring 2)
% %             -0.54*pi (Ring 3)
% %              0.54*pi (Ring 4)
% %             -0.85*pi (MZI)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simple MZI V3 (Double Period) (14.10):
% % Voltages:   (4)  5.7994  V ; 0.9 mA (Ring 3)
% %             (6)  10.9876 V ; 3.5 mA (Ring 1)
% %             (9)  4.6783  V ; 14  mA (MZI)
% %             (11) 9.715   V ; 2   mA (Ring 2)
% %             (12) 13.2581 V ; 3.8 mA (Ring 4)
% % Phases:     -0.25*pi (Ring 1)
% %              0.25*pi (Ring 2)
% %             -0.64*pi (Ring 3)
% %              0.64*pi (Ring 4)
% %              0.365*pi (MZI)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simple MZI V4 (Best) (14.10):
% % Voltages:   (4)  6.0092  V ; 0.9 mA (Ring 3)
% %             (6)  6.7278  V ; 2.1 mA (Ring 1)
% %             (9)  4.6482  V ; 14  mA (MZI)
% %             (11) 10.015  V ; 2   mA (Ring 2)
% %             (12) 10.9374 V ; 3.2 mA (Ring 4)
% % Phases:     -0.25*pi (Ring 1)
% %              0.25*pi (Ring 2)
% %             -0.01*pi (Ring 3)
% %              0.01*pi (Ring 4)
% %              1.05*pi (MZI)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Narrow Filter 2.2GB (14.10):
% % Voltages:   (4)  4.7497 V ; 0.6  mA (Ring 3)
% %             (6)  1.5884 V ; 0.1  mA (Ring 1)
% %             (9)  3.8294 V ; 11.5 mA (MZI)
% %             (11) 15.653 V ; 4    mA (Ring 2)
% %             (12) 8.4791 V ; 2.5  mA (Ring 4)
% % Phases:     *pi (Ring 1)
% %             *pi (Ring 2)
% %             *pi (Ring 3)
% %             *pi (Ring 4)
% %             *pi (MZI)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Narrow Filter Better 1.1875GB (14.10):
% % Voltages:   (4)  4.6498 V ; 0.5  mA (Ring 3)
% %             (6)  1.5883 V ; 0.1  mA (Ring 1)
% %             (9)  3.9093 V ; 11.3 mA (MZI)
% %             (11) 15.733 V ; 4    mA (Ring 2)
% %             (12) 8.6192 V ; 2.3  mA (Ring 4)
% % Phases:      0.04*pi (Ring 1)
% %             -0.04*pi (Ring 2)
% %             -0.01*pi (Ring 3)
% %              0.01*pi (Ring 4)
% %              0.01*pi (MZI)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Narrow Filter Better2 0.775GB (14.10):
% % Voltages:   (4)  4.319   V ; 0.6  mA (Ring 3)
% %             (6)  13.8568 V ; 4.5  mA (Ring 1)
% %             (9)  3.9634  V ; 11.6 mA (MZI)
% %             (11) 15.725  V ; 4    mA (Ring 2)
% %             (12) 8.2668  V ; 2.5  mA (Ring 4)
% % Phases:      1.010*pi (Ring 1)
% %             -1.010*pi (Ring 2)
% %             -1.024*pi (Ring 3)
% %              1.024*pi (Ring 4)
% %             -0.055*pi (MZI)
% % OR:
% %              0.04*pi (Ring 1)
% %             -0.04*pi (Ring 2)
% %             -0.01*pi (Ring 3)
% %              0.01*pi (Ring 4)
% %              0.01*pi (MZI)
% % OR:
% %              0.01*pi (Ring 1)
% %             -0.01*pi (Ring 2)
% %             -0.01*pi (Ring 3)
% %              0.01*pi (Ring 4)
% %              0.01*pi (MZI)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Ring:
% % Voltages:   (4)  V ; mA (Ring 3)
% %             (6)  V ; mA (Ring 1)
% %             (9)  V ; mA (MZI)
% %             (11) V ; mA (Ring 2)
% %             (12) V ; mA (Ring 4)
% % Phases:     -1.000*pi (Ring 1)
% %              1.000*pi (Ring 2)
% %              0.975*pi (Ring 3)
% %             -0.975*pi (Ring 4)
% %             -0.300*pi (MZI)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

k1 = 0.942; %(Matan) % 0.1035; %(Madsen) %0.489; %(Saawan)
k2 = 0.942; %(Matan) % 0.1035; %(Madsen) %0.489; %(Saawan)
k3 = 0.484; %(Matan) % 0.3551; %(Madsen) %0.943; %(Saawan)
k4 = 0.484; %(Matan) % 0.3551; %(Madsen) %0.943; %(Saawan)

% for phiscan = -0.1*pi:0.01*pi:0.1*pi
%     phi1 = +0.04*pi; % (Shai) % -0.3480; %(Madsen) % 2*pi*rand(); % +1.5029; %(Saawan)
%     phi2 = -phi1;    % (Shai) % +0.3480; %(Madsen) % 2*pi*rand(); % -1.5029; %(Saawan)
%     phi3 = -0.01*pi; % (Shai) % +0.1944; %(Madsen) % 2*pi*rand(); % -1.7232; %(Saawan)
%     phi4 = -phi3;    % (Shai) % -0.1944; %(Madsen) % 2*pi*rand(); % +1.7232; %(Saawan)
%     phit = +0.01*pi; % (Shai) % +0.0700; %(Madsen) % 1.24 %(Saawan) %[2553.81] (Matan)

zp_analysis = 1;
alpha  = 356; % [dB/m]
n      = 4.2; % [Si eff index (Matan)] % 1.9963; % [SiN refractive index]
c      = 299792458; % [m*s^-1]
L      = 2*pi*100e-6*5/5.5; % [m]
T      = L*n/c; % [s]
N      = 1000;
lambda = linspace(1548*1e-9, 1552*1e-9, N); % [m]
k      = 2*pi./lambda; % [rad*m^-1]
gamma  = 10^(-alpha*L/20);
FSR    = lambda(end/2)^2/(lambda(end/2) + n*L);


idx = 1;
step = 0.05*pi;
% for phi1 = -pi:step:pi
%     for phi2 = -pi:step:pi
%         for phi3 = -pi:step:pi
%             for phi4 = -pi:step:pi
%                 for phit = -pi:step:pi

% for iii = 1:length(saveFWHM)
% % WORKING POINTS: iii = 22538, 82, 86, 123 ,140
% % for iii = 22450:22600
% 
% %                     if saveFWHM(iii)*1e12 < 40
% %                         continue
% %                     end
% 
%                     phi1 = savePhi1(iii);
%                     phi2 = savePhi2(iii);
%                     phi3 = savePhi3(iii);
%                     phi4 = savePhi4(iii);
%                     phit = savePhit(iii);

iii = 1;
% iii = 82;
% iii = 6703;

phi1 = savePhi1(iii) - 0.03*pi;
phi2 = savePhi2(iii) - 0.05*pi;
phi3 = savePhi3(iii) + 0.05*pi;
phi4 = savePhi4(iii) + 0.02*pi;
phit = savePhit(iii) + 0.095*pi;


f1 = figure('Position', [100,70,1100,550]);

for iii = [1]
% for phi1 = [1] %-1*pi:0.005*pi:1*pi %0.07*pi % %savePhit(iii) + (-0.05*pi:0.001*pi:0.05*pi)

    phi1 = -0.25*pi;
    phi2 =  0.25*pi;
    phi3 = -0.64*pi;
    phi4 =  0.64*pi;
    phit =  0.365*pi;

    disp({['phi_1 = ' num2str(phi1/pi, '%.3f') ' pi'],
        ['phi_2 = ' num2str(phi2/pi, '%.3f') ' pi'],
        ['phi_3 = ' num2str(phi3/pi, '%.3f') ' pi'],
        ['phi_4 = ' num2str(phi4/pi, '%.3f') ' pi'],
        ['phi_t = ' num2str(phit/pi, '%.3f') ' pi']})
    
    T1 = (sqrt(1-k1) - gamma*exp(-1j*n*k*L-1j*phi1))./(1 - sqrt(1-k1)*gamma*exp(-1j*n*k*L-1j*phi1));
    T2 = (sqrt(1-k2) - gamma*exp(-1j*n*k*L-1j*phi2))./(1 - sqrt(1-k2)*gamma*exp(-1j*n*k*L-1j*phi2));
    T3 = (sqrt(1-k3) - gamma*exp(-1j*n*k*L-1j*phi3))./(1 - sqrt(1-k3)*gamma*exp(-1j*n*k*L-1j*phi3));
    T4 = (sqrt(1-k4) - gamma*exp(-1j*n*k*L-1j*phi4))./(1 - sqrt(1-k4)*gamma*exp(-1j*n*k*L-1j*phi4));
    
    H11 = 1/2  *(T1.*T3  - T2.*T4*exp(-1j*phit));
    %                     H12 = -1j/2*(T1.*T3  + T2.*T4*exp(-1j*phit));
    %                     H21 = -1j/2*(T1.*T3  + T2.*T4*exp(-1j*phit));
    %                     H22 = 1/2  *(-T1.*T3 + T2.*T4*exp(-1j*phit));
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    Loss = 10*log10(abs(H11).^2);
    Loss = Loss - max(Loss);
    % [pks, locs] = findpeaks(Loss, 'MinPeakProminence', 5);
    % [~, sortingOrder] = sort(pks, 'descend');
    % pks  = pks(sortingOrder);
    % locs = locs(sortingOrder);
    % 
    % mainPeak = pks(1);
    % mainPeakloc = locs(1);
    % 
    % scanWidth = 10;
    % narrowLambda = lambda(max([1,(mainPeakloc-scanWidth)]):min([length(Loss), (mainPeakloc+scanWidth)]));
    % narrowLoss   =   Loss(max([1,(mainPeakloc-scanWidth)]):min([length(Loss), (mainPeakloc+scanWidth)]));
    % 
    % narrowLambdaDense = linspace(narrowLambda(1), narrowLambda(end), 1e3);
    % narrowLossDense = interp1(narrowLambda, narrowLoss, narrowLambdaDense);
    % 
    % [~, Imax] = min(abs(narrowLossDense - mainPeak));
    % aux1 = narrowLossDense > -3;
    % aux2 = find(aux1 - circshift(aux1,-1));
    % I3dB1 = min(aux2(aux2>Imax));
    % I3dB2 = max(aux2(aux2<Imax));
    % I = [I3dB1, I3dB2];
    % if isempty(I3dB1) || isempty(I3dB2)
    %     FWHM = 10;
    % else
    %     FWHM = abs(narrowLambdaDense(I(2)) - narrowLambdaDense(I(1)));
    % end
    
    
    if zp_analysis
        a = zeros(1,5);
        b = zeros(1,5);
        z = zeros(4,1);
        p = zeros(4,1);
        
        z(1) = gamma / sqrt(1-k1) * exp(-1j*phi1);
        z(2) = gamma / sqrt(1-k2) * exp(-1j*phi2);
        z(3) = gamma / sqrt(1-k3) * exp(-1j*phi3);
        z(4) = gamma / sqrt(1-k4) * exp(-1j*phi4);
        p(1) = gamma * sqrt(1-k1) * exp(-1j*phi1);
        p(2) = gamma * sqrt(1-k2) * exp(-1j*phi2);
        p(3) = gamma * sqrt(1-k3) * exp(-1j*phi3);
        p(4) = gamma * sqrt(1-k4) * exp(-1j*phi4);
        
        a(1) = 2;
        a(2) = -2*sum(p);
        a(3) = 2*(p(1)*p(2) + p(1)*p(3) + p(1)*p(4) + p(2)*p(3) + p(2)*p(4) + p(3)*p(4));
        a(4) = -2*(p(1)*p(2)*p(3) + p(1)*p(2)*p(4) + p(1)*p(3)*p(4) + p(2)*p(3)*p(4));
        a(5) = 2*prod(p);
        
        b(1) = 1 - exp(-1j*phit);
        b(2) = -(z(1)+p(2)+z(3)+p(4) - exp(-1j*phit) * (p(1)+z(2)+p(3)+z(4)));
        b(3) = z(1)*p(2) + z(3)*p(4) + z(1)*z(3) + z(1)*p(4) + p(2)*z(3) + p(2)*p(4) - exp(-1j*phit) * (p(1)*z(2) + p(3)*z(4) + p(1)*p(3) + p(1)*z(4) + z(2)*p(3) + z(2)*z(4));
        b(4) = -(z(1)*p(2)*z(3) + z(1)*p(2)*p(4) + z(1)*z(3)*p(4) + p(2)*z(3)*p(4) - exp(-1j*phit) * (p(1)*z(2)*p(3) + p(1)*z(2)*z(4) + p(1)*p(3)*z(4) + z(2)*p(3)*z(4)));
        b(5) = z(1)*p(2)*z(3)*p(4) - exp(-1j*phit) * (p(1)*z(2)*p(3)*z(4));
        
        subplot(1,2,1)
        zplane(b,a)
        grid on
        % Design the figure a bit better
        ax = gca;
        datasets = ax.Children;
        datasets(1).LineWidth = 1.5;
        datasets(2).LineWidth = 1.5;
        datasets(3).LineWidth = 1.5;
        datasets(2).Color = [0 0.4470 0.7410];
        datasets(3).Color = [0.8500 0.3250 0.0980];
        hold on
        plot([-1,1]*5, [0,0]*5, 'k', 'LineWidth', 1.2)
        plot([0,0]*5, [-1,1]*5, 'k', 'LineWidth', 1.2)
        legend('Zeros', 'Poles')
        xlim([-1,1]*1.2)
        ylim([-1,1]*1.2)
        hold off
        
        subplot(1,2,2)
        % plot(lambda*1e9, Loss)
        plot(lambda*1e9, abs(H11).^2./max(abs(H11).^2))
        % title({['iii = ' num2str(iii)],['\phi_1 = ' num2str(phi1/pi) '\pi ; \phi_2 = ' num2str(phi2/pi) '\pi ; \phi_3 = ' num2str(phi3/pi) '\pi ; \phi_4 = ' num2str(phi4/pi) '\pi ; \phi_t = ' num2str(phit/pi) '\pi'], ['FWHM = ' num2str(FWHM*1e12, '%.3f') ' [pm]']})
%         title({['iii = ' num2str(iii)],['\phi_1 = ' num2str(phi1/pi) '\pi ; \phi_2 = ' num2str(phi2/pi) '\pi ; \phi_3 = ' num2str(phi3/pi) '\pi ; \phi_4 = ' num2str(phi4/pi) '\pi ; \phi_t = ' num2str(phit/pi) '\pi']})
        title(['\phi_1 = ' num2str(phi1/pi) '\pi ; \phi_2 = ' num2str(phi2/pi) '\pi ; \phi_3 = ' num2str(phi3/pi) '\pi ; \phi_4 = ' num2str(phi4/pi) '\pi ; \phi_t = ' num2str(phit/pi) '\pi'])
%         ylim([-60 2])
%         ylim([0 1])
        grid on
        hold on
%         plot(narrowLambdaDense(I(1)), narrowLossDense(I(1)), '*')
%         plot(narrowLambdaDense(I(2)), narrowLossDense(I(2)), '*')
%         plot([lambda(1) lambda(end)], [-10 -10], '--k', 'LineWidth', 1.5)
        hold off
        drawnow
        pause(0.1)
    end
    
    %                     if (FWHM < 0.05e-9) && (FWHM > 5e-13)
    %                         savePhi1(idx) = phi1;
    %                         savePhi2(idx) = phi2;
    %                         savePhi3(idx) = phi3;
    %                         savePhi4(idx) = phi4;
    %                         savePhit(idx) = phit;
    %                         saveFWHM(idx) = FWHM;
    %                         idx = idx + 1;
    %                     end
    %                 end
    %             end
    %         end
    %     end
end


%% Elliptical Filter
%------1----------3-----
%------2----------4-----

kt0 = 0.501;
k1  = 0.1035;
k2  = 0.1035;
k3  = 0.3551;
k4  = 0.3551;
kt1 = 0.500;

phi1 = -0.3480;
phi2 = +0.3480;
phi3 = +0.1944;
phi4 = -0.1944;
phit = 0.07;

ct0 = sqrt(1-kt0);
st0 = sqrt(kt0);
c1  = sqrt(1-k1);
s1  = sqrt(k1);
c2  = sqrt(1-k2);
s2  = sqrt(k2);
c3  = sqrt(1-k3);
s3  = sqrt(k3);
c4  = sqrt(1-k4);
s4  = sqrt(k4);
ct1 = sqrt(1-kt1);
st1 = sqrt(kt1);

alpha = 1*100; % [dB/m]
n     = 1.9963; % [SiN refractive index]
c     = 299792458; % [m*s^-1]
L     = 100e-6; % [m]
T     = L*n/c; % [s]
N     = 1000;
Omega = linspace(193e12-2*pi/T, 193e12+2*pi/T, N); % [rad/sec]

gamma = 10^(-alpha*L/20);

T1 = (c1 - gamma*exp(-1j*Omega*T-1j*phi1))./(1 - c1*gamma*exp(-1j*Omega*T-1j*phi1));
T2 = (c2 - gamma*exp(-1j*Omega*T-1j*phi2))./(1 - c2*gamma*exp(-1j*Omega*T-1j*phi2));
T3 = (c3 - gamma*exp(-1j*Omega*T-1j*phi3))./(1 - c3*gamma*exp(-1j*Omega*T-1j*phi3));
T4 = (c4 - gamma*exp(-1j*Omega*T-1j*phi4))./(1 - c4*gamma*exp(-1j*Omega*T-1j*phi4));

H11 = ct0*ct1*T1.*T3 - st0*st1*T2.*T4*exp(-1j*phit);
H12 = -1j*(ct1*st0*T1.*T3 + st1*ct0*T2.*T4*exp(-1j*phit));
H21 = -1j*(st1*ct0*T1.*T3 + ct1*st0*T2.*T4*exp(-1j*phit));
H22 = -st0*st1*T1.*T3 + ct0*ct1*T2.*T4*exp(-1j*phit);


figure
semilogy(Omega, abs(H11).^2)
hold on
semilogy(Omega, abs(H12).^2)
grid on
xlabel('\Omega [rad \cdot s^{-1}]')
ylabel('H_{11}')
ylim([1e-4 1.05])
legend('Through', 'Cross')
title(['\phi_1 = ' num2str(phi1)])

%% Plot VS. Experiment
T = readtable('new_tec_meas\Through171124_OptRR.txt');
lambdaExp = T.XAxis_Wavelength_nm_;
Loss      = T.InsertionLoss_dB_;
Loss      = Loss - max(Loss);
PhaseExp  = T.JMElementAPhase_rad_;
H11Sim    = 10*log10(circshift(abs(H11).^2, 70));
H11Sim    = H11Sim - max(H11Sim);

figure
% subplot(2,1,1)
plot(lambda*1e9, H11Sim, 'LineWidth', 1.5)
hold on
plot(lambdaExp, Loss, 'LineWidth', 1.5)
grid on
xlabel('\lambda [nm]', 'FontSize', 15)
ylabel('Through [dB]', 'FontSize', 15)
title('Elliptical Filter (AMF)', 'FontSize', 15)

% subplot(2,1,2)
% plot(lambda*1e9, angle(H11), 'LineWidth', 1.5)
% hold on
% plot(lambdaExp, PhaseExp, 'LineWidth', 1.5)
% grid on
% xlabel('\lambda [nm]', 'FontSize', 15)
% ylabel('Phase [rad]', 'FontSize', 15)


%% Plot Experiment Only (duty cycle sweep)
figure
tuneWL = [-20 -30 -20 0];
idx = 1;
for DC = [25 30 40 50]
    T = readtable(['new_tec_meas\Through171124_' num2str(DC) 'DC.txt']);
    lambdaExp = T.XAxis_Wavelength_nm_;
    Loss      = T.InsertionLoss_dB_;
    Loss      = Loss - max(Loss);
    Loss      = circshift(Loss, tuneWL(idx));
    
    plot(lambdaExp, Loss, 'LineWidth', 1.5, 'DisplayName', ['~' num2str(DC) '% DC'])
    hold on
    grid on
    xlabel('\lambda [nm]', 'FontSize', 15)
    ylabel('Through [dB]', 'FontSize', 15)
    title('Elliptical Filter (AMF)', 'FontSize', 15)
    legend show
    idx = idx+1;
end


%% Plot Experiment Only optimal rejection ratio vs. optimal flatness
figure

T = readtable('new_tec_meas\Through171124_OptRR.txt');
lambdaExp_optRR = T.XAxis_Wavelength_nm_;
Loss_optRR      = T.InsertionLoss_dB_;
Loss_optRR      = Loss_optRR - max(Loss_optRR);
Loss_optRR      = circshift(Loss_optRR, -150);

T = readtable('new_tec_meas\Through171124_OptFlatness.txt');
lambdaExp_optFlat = T.XAxis_Wavelength_nm_;
Loss_optFlat      = T.InsertionLoss_dB_;
Loss_optFlat      = Loss_optFlat - max(Loss_optFlat);
Loss_optFlat      = Loss_optFlat(lambdaExp_optFlat <= 1552);
lambdaExp_optFlat = lambdaExp_optFlat(lambdaExp_optFlat <= 1552);

plot(lambdaExp_optRR,   Loss_optRR,   'LineWidth', 1.5, 'DisplayName', 'Optimal Rejection Ratio')
hold on
plot(lambdaExp_optFlat, Loss_optFlat, 'LineWidth', 1.5, 'DisplayName', 'Optimal Flatness')
grid on
xlabel('\lambda [nm]', 'FontSize', 15)
ylabel('Through [dB]', 'FontSize', 15)
title('Elliptical Filter (AMF)', 'FontSize', 15)
legend show
ylim([-27 5])

%% Plot Experiment Only (Sine)
figure
T = readtable('new_tec_meas\MZI_double.txt');
lambdaExp = T.XAxis_Wavelength_nm_;
Loss      = T.InsertionLoss_dB_;
Loss      = Loss - max(Loss);
log_scale = 0;

if log_scale
    plot(lambdaExp, Loss, 'LineWidth', 1.5)
else
    plot(lambdaExp, 10.^(Loss/10), 'LineWidth', 1.5)
end
grid on
xlabel('\lambda [nm]', 'FontSize', 15)
ylabel('Through [dB]', 'FontSize', 15)
hold on
if log_scale
    plot(lambdaExp, 10*log10(cos(2*pi*lambdaExp / 2).^2))
    ylabel('Through [dB]', 'FontSize', 15)
else
    plot(lambdaExp, cos(2*pi*lambdaExp / 0.9785 + 0.35*pi).^2)
    ylabel('Through [Norm.]', 'FontSize', 15)
end


%% Plot Experiment narrow
figure
T = readtable('new_tec_meas\narrow.txt');
lambdaExp = T.XAxis_Wavelength_nm_;
Loss      = T.InsertionLoss_dB_;
Loss      = Loss - max(Loss);

plot(lambdaExp, Loss, 'LineWidth', 1.5)
grid on
xlabel('\lambda [nm]', 'FontSize', 15)
ylabel('Through [dB]', 'FontSize', 15)

