clc
clear all
close all

%% User input
% Data file path
verbose = 1; % "Verbal" (generate plots)
filepath = '\\madrid.eng.biu.ac.il\e2016\benamis9\Downloads'; % 'C:\Users\leroy\Desktop\Vshape\Vshape_sample8\15.6.23 - before gold\';
filename = 'ring32.txt';

% Wavelength span
W_start = 1540;
W_end   = 1560;

% Experimental setup
Bus_length  = 0.3;   % [cm]
EDFA_power  = 16;    % [dBm]
R           = 50e-6; % [m]
l_racetrack = 80e-6; % [m]

shape = 3; % 1=ring ; 2=racetrack ; 3=specify length manually
switch shape
    case 1
        l = 2*pi*R;
    case 2
        l = 2*pi*R + 2*l_racetrack;
    case 3
        l = 500e-6;
end

%% Read data
T = readtable(fullfile(filepath, filename));
Wavelength = T.XAxis_Wavelength_nm_;
Loss       = T.InsertionLoss_dB_;

%% Crop to desired wavelength span
span = Wavelength > W_start & Wavelength < W_end;

Loss       = Loss(span);
Wavelength = Wavelength(span);

%% Normalize loss
Loss_max = max(Loss);
Loss_norm = Loss - Loss_max;

%% Plot
if verbose
    figure
    plot(Wavelength, Loss_norm)
    grid on
    xlabel('Wavelength[nm]')
    ylabel('Normalaized Insertion Loss[dB]')
    xlim([Wavelength(1) Wavelength(end)])
end

%% Find peaks + maximum extinction ratio peak + FSR
[Mpeak, Lpeak, W, ER] = findpeaks(-Loss_norm, Wavelength, 'MinPeakDistance', 1);
[mER, LER] = max(ER);
if LER < length(Lpeak)
    FSR = abs(Lpeak(LER) - Lpeak(LER+1));
else
    FSR = abs(Lpeak(LER) - Lpeak(LER-1));
end

%% plot
if verbose
    figure
    plot(Wavelength, -Loss_norm);
    hold on
    plot(Lpeak, Mpeak, 'go')
    plot(Lpeak(LER), Mpeak(LER), 'b+')
    for idx = 1:length(ER)
        plot([Lpeak(idx)-W/2, Lpeak(idx)+W/2], [1, 1]*(Mpeak(idx)-ER(idx)/2), 'k')
        plot([1, 1]*Lpeak(idx), [Mpeak(idx), Mpeak(idx)-ER(idx)], 'k')
    end
end

%% Isolate the highest ER peak
logical_span = (Wavelength > Lpeak(LER)-0.5*FSR) & (Wavelength < Lpeak(LER)+0.5*FSR);
peak_span = Wavelength(logical_span);
peak_mag  = Loss_norm(logical_span);

%% Interpolate
inter = 7;
peak_span_q = peak_span(1) : (peak_span(2)-peak_span(1))/inter : peak_span(end);
peak_mag_q = interp1(peak_span, peak_mag, peak_span_q, 'spline');

%% Find peak in the interpolated vector
[value, index] = min(peak_mag_q);
lambda_0 = peak_span_q(index);

%% Find FWHM of highest ER peak
baseAmpLeft  = mean(peak_mag_q(index - ceil(FSR/3  / (peak_span_q(2) - peak_span_q(1))) : index - floor(FSR/10 / (peak_span_q(2) - peak_span_q(1)))));
baseAmpRight = mean(peak_mag_q(index + ceil(FSR/10 / (peak_span_q(2) - peak_span_q(1))) : index + floor(FSR/3  / (peak_span_q(2) - peak_span_q(1)))));
FWHM_mag = mean([baseAmpLeft, baseAmpRight]) - 3;
normTo_0 = abs(peak_mag_q - FWHM_mag);

[Half_Max1, Half_Max_index1] = sort(normTo_0(1:ceil(length(normTo_0)/2)));
[Half_Max2, Half_Max_index2] = sort(normTo_0(ceil(length(normTo_0)/2):end));
Half_Max_index2 = Half_Max_index2 + ceil(length(normTo_0)/2);

% Half_Max_WL = peak_span_q([Half_Max_index1(1) Half_Max_index2(1)]);
% Delta_Lambda = abs(Half_Max_WL(2)-Half_Max_WL(1));
Delta_Lambda = peak_span_q(Half_Max_index2(1)) - peak_span_q(Half_Max_index1(1));

%% Plot
if verbose
    figure
    plot(peak_span_q, peak_mag_q)
    hold on
    plot(lambda_0 + 0.5*Delta_Lambda*[-1, 1], [1, 1]*FWHM_mag)
    xlabel('Wavelength[nm]','FontSize',20,'FontWeight','bold')
    ylabel('dB','FontSize',20,'FontWeight','bold')
    %title({'\alpha = ' num2str(alpha_dB),'Q factor = ' num2str(Q_loaded)})
end

%% Outputs
Q_loaded      = lambda_0/Delta_Lambda
Q_int         = 2*Q_loaded/(1+(sqrt(mER))^-1)
Finesse       = FSR/Delta_Lambda
n_g           = (lambda_0*10^-9)^2/((FSR*10^-9)*l)
alpha_dB      = 4.34*n_g*pi*(1+sqrt((10^(-mER/10))))/(lambda_0*10^-7*Q_loaded)
Coupling_Loss = Loss_max + alpha_dB*Bus_length - EDFA_power
