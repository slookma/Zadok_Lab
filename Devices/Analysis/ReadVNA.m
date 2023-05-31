clc
close all
clear all
%%
path = '\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\SAW\Mirit\12012021\GeS2_35';
%format = {'REAL','IMAG','PHASE','LINMAG'};
format = {'Real','Imag','Phase','LinMag'};
%numberList = [8 8];
for ii = 1:1;
    %number = num2str(numberList(ii));
    number = num2str(ii);
for i = 1:4
    %fileName = [path,number,'\',format{i},'.prn'];
   
   fileName = [path,'\',format{i},'.prn'];
    S = importdata(fileName);
    frequancy = S.data(:,1);
    
    
    if i == 1;
        Real = S.data(:,2);
    elseif i == 2;
        Imag = S.data(:,2);
    elseif i == 3;
        Phase = S.data(:,2);
    elseif i == 4;
        LinMag = S.data(:,2);
        LinMag_norm = LinMag/max(LinMag);
    elseif i == 5;
        LogMag = S.data(:,2);
            
    end
        
end




Time = (1:1:length(frequancy))*1e-9;
ifMat = exp(1j*2*pi*frequancy*Time);

signal = (Real+j*Imag).'*ifMat;


%TimeDomain = fftshift(ifft(fftshift(Real+j*Imag)));
% [pks,locs,widths,proms] = findpeaks(abs(TimeDomain(400:801))/max(abs(TimeDomain(400:801))),400:length(Time),'Threshold',0.1);
figure
hold on
subplot(2,1,1);
plot(frequancy/1e9,20*log(LinMag_norm))
hold off
subplot(2,1,2);
hold on
[m pl] = max((abs(signal(360:370))));
%plot(Time(600:801),[abs(TimeDomain(650:801)); abs(TimeDomain(1:50))]/max(abs(TimeDomain(650:801))))
plot((Time)*1e9-(pl+360),abs(signal)/max(abs(signal)))
% plot(Time(locs),pks,'or')
hold off

figure (500)
hold on
%plot(frequancy,LinMag_norm)
plot(frequancy,LinMag/max(LinMag))
hold off
end
%%
figure(400)
 hold on
 NormTD = abs(TimeDomain)/max(abs(TimeDomain));
 [pks,Im] =  max(abs(TimeDomain(600:605)));
  if ii == 1
      normal = max(NormTD(60:620));
  end
 plot((Time(590:620))*1e9,NormTD(590:620)/normal) 
 hold off
Weight(ii) = max(NormTD(590:620)/normal);
% figure(100)
%  hold on
%  NormTD = abs(TimeDomain(590:625))/max(abs(TimeDomain(590:625)));
%  [pks,Im] =  max(abs(TimeDomain(590:625)));
%   if ii == 1
%       normal = max(NormTD);
%   end
%  plot((Time(590:625) - Time(Im+590))*1e6,NormTD/normal) 
%  hold off



Width  = [700 1100 1270 1430 1580 1720 1860 2120];
