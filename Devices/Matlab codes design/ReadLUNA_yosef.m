clc

clear all
close all

%%
filepath = 'C:\Users\leroy\Desktop\Vshape\Vshape_sample8\15.6.23 - before gold\';
filename = 'ring32.txt';
%%
[Wavelength Frequency Loss Time Time_Domain_Amplitude] = textread([filepath,filename], '%f %f %f %f %f', 'headerlines', 8);

%%
% figure(89)
% ROI= (1:3:length(Loss));
% plot(Wavelength(ROI),Loss(ROI))
ROI2 = (1:3:length(Loss));
Loss_max = max(Loss(ROI2));
%Loss_max = 0;
Loss_norm = Loss(ROI2) - Loss_max; 
W_start = 1540;
W_end = 1560;
Wavelength = Wavelength(ROI2);
span  = Wavelength > W_start & Wavelength < W_end;
% R = 50e-6;
l = 500e-6%2*pi*R+80e-6*2;
%l  = 1.3*10^-2;
Bus_length = 0.3;%[cm]
EDFA_power = 16;%[dBm]

%%%%%%%%%%%%%%%%% added can get rid of
Loss_max = max(Loss_norm(span));
Loss_norm = Loss_norm(span) - Loss_max; 
%%%%%%%%%%%%%%%%% added can get rid of

% Loss_norm = Loss_norm(span);
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



% vq = interp1(Wavelength_q,Loss_norm_q,Wavelength,'cubic');
%[Mpeak,Lpeak,W,ER] = findpeaks(-vq,Wavelength,'MinPeakDistance',0.9);
[Mpeak,Lpeak,W,ER] = findpeaks(-Loss_norm,Wavelength,'MinPeakDistance',1);
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

plot(peak_span_q,peak_mag_q+0.5)
% plot(peak_span_q,peak_mag_q)

%%
normTo_0 = abs(peak_mag_q -max(peak_mag_q)+3.9);
[Half_Max1, Half_Max_index1] = sort(normTo_0(1:ceil(length(normTo_0)/2)));
[Half_Max2, Half_Max_index2] = sort(normTo_0(ceil(length(normTo_0)/2):end));
Half_Max_index2 = Half_Max_index2 + ceil(length(normTo_0)/2);
% figure(89)
% plot(normTo_0)
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
n_g = (Lambda_0*10^-9)^2/((FSR*10^-9)*l)
alpha_dB = 4.34*n_g*pi*(1+sqrt((10^(Max_ER/10))))/(Lambda_0*10^-7*Q_loaded)

Coupling_Loss = Loss_max + alpha_dB*Bus_length - EDFA_power
xlabel('Wavelength[nm]','FontSize',20,'FontWeight','bold')
ylabel('dB','FontSize',20,'FontWeight','bold')
%title({'\alpha = ' num2str(alpha_dB),'Q factor = ' num2str(Q_loaded)})
