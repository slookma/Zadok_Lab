 clc

clear all
close all

%%
% filepath = '\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\SAW\APL\measurments\8Tap\081220\';
% filename = '8tap.txt';
filepath = '';
filename = 'Ring_10um.txt';
%%
% [Wavelength Frequency Loss Time Time_Domain_Amplitude] = textread([filepath,filename], '%f %f %f %f %f', 'headerlines', 8);
T = readtable([filepath, filename]);
Wavelength              = T.XAxis_Wavelength_nm_;
Frequency               = T.XAxis_Frequency_GHz_;
Loss                    = T.InsertionLoss_dB_;
Time                    = T.GroupDelay_ps_;
Time_Domain_Amplitude   = T.ChromaticDispersion_ps_nm_;

%%

Loss_max = max(Loss(1:2:end));
%Loss_max = 0;
Loss_norm = Loss(1:2:end) - Loss_max; 
W_start = 1540;
W_end = 1560;
Wavelength = Wavelength(1:2:end);
span  = Wavelength > W_start & Wavelength < W_end;
R = 200e-6;
l = 2*pi*R;
%l  = 1.3*10^-2;
Bus_length = 0.3;%[cm]
EDFA_power = 16;%[dBm]
Loss_norm = Loss_norm(span);
Wavelength = Wavelength(span);
figure
plot(Wavelength,Loss_norm)
hold on
xlabel('Wavelength[nm]')
ylabel('Normalaized Insertion Loss[dB]')
xlim([Wavelength(1) Wavelength(end)])
hold off

%%

figure
%Wavelength_q = linspace(W_start,W_end,5*length(span));
Wavelength_q = Wavelength(1:3:end);
Loss_norm_q = Loss_norm(1:3:end);



vq = interp1(Wavelength_q,Loss_norm_q,Wavelength,'cubic');
%[Mpeak,Lpeak,W,ER] = findpeaks(-vq,Wavelength,'MinPeakDistance',0.9);
[Mpeak,Lpeak,W,ER] = findpeaks(-Loss_norm,Wavelength,'MinPeakDistance',0.3);
%plot(Wavelength,-vq);
plot(Wavelength,-Loss_norm);
hold on
plot(Wavelength,-Loss_norm,'r')
plot(Lpeak,Mpeak,'go')

[mER,LER] = max(ER)
plot(Lpeak(LER),Mpeak(LER),'b+')

%FSR = mean(diff(Lpeak))
FSR = abs(Lpeak(LER)-Lpeak(LER+1))
figure
logical_span = Wavelength>Lpeak(LER)-0.5*FSR & Wavelength<Lpeak(LER)+0.5*FSR;
peak_span = Wavelength(logical_span);
%peak_mag = vq(logical_span);
peak_mag = Loss_norm(logical_span);
%%
inter = 7;
peak_span_q = peak_span(1):(peak_span(2)-peak_span(1))/inter:peak_span(end);
peak_mag_q = interp1(peak_span,peak_mag,peak_span_q,'spline');
%%
[value,index] = min(peak_mag_q);
lambda_0 = peak_span_q(index);
%peak_mag_q = peak_mag_q(index-50:index+50);
%peak_span_q = peak_span_q(index-50:index+50);
%%

plot(peak_span_q,peak_mag_q)

%%
normTo_0 = abs(peak_mag_q -max(peak_mag_q) + 3);
[Half_Max1, Half_Max_index1] = sort(normTo_0(1:ceil(length(normTo_0)/2)));
[Half_Max2, Half_Max_index2] = sort(normTo_0(ceil(length(normTo_0)/2):end));
Half_Max_index2 = Half_Max_index2 + ceil(length(normTo_0)/2);

Half_Max_WL = peak_span_q([Half_Max_index1(1) Half_Max_index2(1)]);
Delta_Lambda = abs(Half_Max_WL(2)-Half_Max_WL(1));
hold on
plot(Half_Max_WL,peak_mag_q([Half_Max_index1(1) Half_Max_index2(1)]),'ro')


%%

Lambda_0 = Lpeak(LER);

Max_ER = min(peak_mag) -max(peak_mag);

Q_loaded = Lambda_0/Delta_Lambda

Q_int = 2*Q_loaded/(1+(sqrt(-Max_ER))^-1)
Finesse = FSR/Delta_Lambda
n_g = (Lambda_0*10^-9)^2/(FSR*10^-9*l)
alpha_dB = 4.34*n_g*pi*(1+sqrt((10^(Max_ER/10))))/(Lambda_0*10^-7*Q_loaded)
% alpha_dB = 0.01*4.34*Lambda_0*10^-9/(Q_int*R*FSR*10^-9);

Coupling_Loss = Loss_max + alpha_dB*Bus_length - EDFA_power
xlabel('Wavelength[nm]','FontSize',20,'FontWeight','bold')
ylabel('dB','FontSize',20,'FontWeight','bold')
title({'10 \mum', ['\alpha = ' num2str(alpha_dB),' ; Q factor = ' num2str(Q_loaded)]})
grid on