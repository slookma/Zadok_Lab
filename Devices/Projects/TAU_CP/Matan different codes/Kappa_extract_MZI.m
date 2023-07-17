% close all
clear all
clc

%%
openfig('REF2_TLV.fig');
num = 15;
Name = [];
Check = [];
Flag_plot = 1;
for i = 1:15

h = findobj(gca,'Type','line');
Wavelength = h(i).XData;
Loss = h(i).YData;
Name = [Name ,str2double(h(i).DisplayName)];
Loss_max = max(Loss(1:2:end));
Loss_norm = Loss(1:2:end) - Loss_max; 
W_start = 1540;
W_end = 1560;
Wavelength = Wavelength(1:2:end);
span  = Wavelength > W_start & Wavelength < W_end;
% R = 75e-6;
% l = 2*pi*R;
% Bus_length = 0.1;%[cm]
% EDFA_power = 18;%[dBm]
Loss_norm = Loss_norm(span);
Wavelength = Wavelength(span);
if Flag_plot==1
    figure
    plot(Wavelength,Loss_norm)
end
hold on
xlabel('Wavelength[nm]')
ylabel('Normalaized Insertion Loss[dB]')
xlim([Wavelength(1) Wavelength(end)])
hold off

%%


%Wavelength_q = linspace(W_start,W_end,5*length(span));
Wavelength_q = Wavelength(1:3:end);
Loss_norm_q = Loss_norm(1:3:end);



vq = interp1(Wavelength_q,Loss_norm_q,Wavelength,'cubic');
%[Mpeak,Lpeak,W,ER] = findpeaks(-vq,Wavelength,'MinPeakDistance',0.9);
[Mpeak,Lpeak,W,ER] = findpeaks(-Loss_norm,Wavelength,'MinPeakDistance',2.5);
%plot(Wavelength,-vq);

if Flag_plot==1
    figure
    plot(Wavelength,-Loss_norm);
    hold on
    plot(Wavelength,-Loss_norm,'r')
    plot(Lpeak,Mpeak,'go')
    
    
    plot(Lpeak(LER),Mpeak(LER),'b+')
    figure
    plot(Lpeak,ER)
end
[mER,LER] = max(ER);

%FSR = mean(diff(Lpeak))
if LER == length(Lpeak)
    FSR = abs(Lpeak(LER)-Lpeak(LER-1));
else
    FSR = abs(Lpeak(LER)-Lpeak(LER+1));
end

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
if Flag_plot==1;
    figure
    plot(peak_span_q,peak_mag_q)
end

%%
normTo_0 = abs(peak_mag_q -max(peak_mag_q) + 3);



%%

Lambda_0 = Lpeak(LER);

Max_ER = min(peak_mag) -max(peak_mag);
ER_tot(i) = Max_ER;
ER_Lin = db2pow(-Max_ER);
ER_tot_Lin(i) = ER_Lin;
R = 30e-6;
deltaL = 171e-6;%pi*R;
alphaLin = 0.23*6e-2;
theta = 0:pi/10000:pi/2;
ER_fit = ((exp(-alphaLin*deltaL)+tan(theta).^2)./(exp(-alphaLin*deltaL)-tan(theta).^2)).^2;

ER_sort   = abs(ER_fit - ER_Lin);
if i<=3 
    [ER_fittest, ER_fittest_index] = sort(ER_sort(1:ceil(length(ER_sort)/2)));
else
    [ER_fittest, ER_fittest_index] = sort(ER_sort(ceil(length(ER_sort)/2):end));
    ER_fittest_index = ER_fittest_index+ ceil(length(ER_sort)/2);
end
ER_fittest_index_tot(i) = ER_fittest_index(1);
Theta = theta(ER_fittest_index(1));
xlabel('Wavelength[nm]','FontSize',20,'FontWeight','bold')
ylabel('dB','FontSize',20,'FontWeight','bold')

kappa(i) = (1-cos(Theta)^2);
ER_fittest_tot(i) = ER_fit(ER_fittest_index(1));
Check = [Check,kappa(i)];

    

   



hold off

end
% hold on
% figure(100)
% plot((num-1)*2,kappa)
% hold off
% figure(200)
% hold on
% plot((num-1)*2,ER_tot)
% hold off
% figure(300)
% hold on
% plot((num-1)*2,ER_fittest_tot)
% plot((num-1)*2,ER_tot_Lin)


% Name
Check
close all
