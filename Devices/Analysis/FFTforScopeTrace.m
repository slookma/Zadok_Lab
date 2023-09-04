% filePath = '26_08\modeswar4.bin';
% filePath = '30_31_08_21\344_1.bin';%36_1 338_1 338_2 338_3 338_4 344_1 344_2 nolaser nopump
%36_1 - multimode comb ; 344_1 - only BSBS burst; 344_2 - Kerr comb
% v = getScopeDataBin(filePath, 'bin');
filePath = '68MHzLPF_PowerScan\68mhz346dbm.bin';% 329X2 330 331X2 332X2 333 336 340
[t,v] = importAgilentBin(filePath);

% v = double(Channel_2.Data)*Channel_2.YInc+Channel_2.YOrg;
% v = Channel_2.Data; 
% fs = 8e9;
% dt = 1/fs;
% t = 0:dt:(length(v)-1);
%%
dt = t(2)-t(1);
t = dt*(1:length(v));
% figure();plot(t,v')
fs = 1/dt;
NFFT = 2^nextpow2(length(t)/2);
ff = fs*linspace(-1/2,1/2,NFFT);

% Fv = abs(fftshift(fft(v-mean(v),NFFT)))';
% % figure();plot(1e-6*ff,10*log(Fv))
% figure();plot(1e-6*ff,(Fv))
% xlim([0 1e-6*fs/2]) 
% set(gca,'fontsize',16);
% xlabel('Frequency [MHz]','fontsize',16);
% % ylabel('FFT of temporal trace [dB]')
% ylabel('FFT of temporal trace')
%%
Nwind = 2*100000;%100000 for LPF data from 1_9
s = spectrogram(v-mean(v),Nwind);
f = linspace(0,fs/2,size(s,1));
min_f_ind = find (f>2205*1e6,1);
max_f_ind = find (f>2225*1e6,1);
ind_vec = min_f_ind:max_f_ind;
%%
% figure();imagesc((1:size(s,2))*dt*Nwind/2,1e-6*f,log10(abs(s)))
figure();imagesc((1:size(s,2))*dt*Nwind/2,1e-6*f(ind_vec),(abs(s(ind_vec,:))))
T = imgaussfilt((abs(s)),3);
figure();imagesc((1:size(s,2))*dt*Nwind/2,1e-6*f,10*log10(T))
% figure();imagesc((1:size(s,2))*dt*Nwind/2,1e-6*f,(T))
% figure();surf((1:size(s,2))*dt*Nwind/2,1e-6*f,10*log10(T),'edgecolor','none')
set(gca,'fontsize',12);
colormap jet
xlabel('Time [us]');
ylabel('Normalized voltage')
% ylim([200 500])
set(gca,'ydir','normal')

ylim([68.3 68.4])
ylim([67 70])
% ylim([168 170])
 
% caxis([-2 1])