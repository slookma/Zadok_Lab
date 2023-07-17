close all
clear all
clc
warning('off','all')

% this code is based on this paper: doi: 10.1109/LPT.2016.2556713.
filepath = '\\madrid.eng.biu.ac.il\e2016\slookma\Desktop\cp-tlv-analysis\Lend_19_um_06072023\ref\';

if filepath(length(filepath)-1) == 'p'
    flag = 16;
else
    flag = 12;
end

figure(1)
for i = 1:15
%% this part is to call the text files and read them
filename = [num2str(i) '.txt'];
A = readtable([filepath,filename]);
Wavelength = A.XAxis_Wavelength_nm_;
Loss = A.InsertionLoss_dB_;

%%
Loss_norm = Loss - max(Loss);                                   % normalize
W_start = 1532;                                                 % starting wavelength
W_end = 1568;                                                   % ending wavelength
span  = Wavelength > W_start & Wavelength < W_end;              % establishing region of interest (ROI)
Loss_norm = Loss_norm(span);                                    % taking ROI for both vectors
Wavelength = Wavelength(span);

%%
% this part is in order to find the best fit kappa by finding max ER
Wavelength_q = Wavelength(1:3:end);
Loss_norm_q = Loss_norm(1:3:end);
vq = interp1(Wavelength_q,Loss_norm_q,Wavelength,'pchip'); %'cubic'
[Mpeak,Lpeak,W,ER] = findpeaks(-Loss_norm,Wavelength,'MinPeakDistance',2);  % [value of peak,location of peaks,width,ER vector]
[mER,LER] = max(ER);                                                        % finds max ER and the index of it
FSR1 = diff(Lpeak);                                                         % vector of FSR dispesrion
if LER == length(Lpeak)
    FSR = abs(Lpeak(LER)-Lpeak(LER-1)); % if it's the last one, diff to the previous
else
    FSR = abs(Lpeak(LER)-Lpeak(LER+1)); % otherwise, diff from the next
end

%%
% this part create the single max ER region
logical_span = Wavelength>Lpeak(LER)-0.5*FSR & Wavelength<Lpeak(LER)+0.5*FSR;
peak_span = Wavelength(logical_span);
peak_mag = Loss_norm(logical_span);
% plot(peak_span,peak_mag) % see the peak itself


%%
ER_tot(i) = -mER;                                   % this is to save all of the ER in dB
ER_Lin = db2pow(mER);                               % move from dB to linear
ER_tot_Lin(i) = ER_Lin;                             % this is to save all of the ER in linear

deltaL = 170e-6;                                    % path imbalance of MZI
alphaLin = 0.23*1400;                               % standard loss in our waveguides 14[dB/cm]
theta = 0:pi/10000:pi/2;                            % rad axis

% the following term is considering identical couplers
ER_fit = ((exp(-alphaLin*deltaL)+tan(theta).^2)./(exp(-alphaLin*deltaL)-tan(theta).^2)).^2; % eq. 4 from paper

ER_sort = abs(ER_fit - ER_Lin);

% the following regards the mixup of not knowing if k=0.1 or k=0.9
  if i<=flag 
  [ER_fittest, ER_fittest_index] = sort(ER_sort(1:ceil(length(ER_sort)/2)));
  else
    [ER_fittest, ER_fittest_index] = sort(ER_sort(ceil(length(ER_sort)/2):end));
    ER_fittest_index = ER_fittest_index+ ceil(length(ER_sort)/2);
  end
  
ER_fittest_index_tot(i) = ER_fittest_index(1);
Theta = theta(ER_fittest_index(1));

kappa(i) = (1-cos(Theta)^2);
ER_fittest_tot(i) = ER_fit(ER_fittest_index(1));


subplot(3,5,i)
plot(Wavelength, Loss_norm)
grid on
xlabel('\lambda [nm]')
ylabel('Loss [dB]')
ylim([-20 0])
title({['Width = ' num2str(-70+(i-1)*10) ' \mum'], ['\kappa = ' num2str(kappa(i))]})


end

figure(2)
width = -70:10:70;
plot(width,kappa)







%%
% % this part interpolates the max ER region
% inter = 7;
% peak_span_q = peak_span(1):(peak_span(2)-peak_span(1))/inter:peak_span(end);
% peak_mag_q = interp1(peak_span,peak_mag,peak_span_q,'spline');
% % plot(peak_span_q,peak_mag_q) % see the peak itself

%%
% [value,index] = min(peak_mag_q);                    % find min and index
% lambda_0 = peak_span_q(index);                      % find the resonance
