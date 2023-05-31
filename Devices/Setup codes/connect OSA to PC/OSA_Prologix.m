%=========================================================================
% OSA_Prologix.m runs and plots a single scan based on current settings of 
% the ANDO AQ6317B.
% Connection is based on the COM (USB Serial Port) identified in the 
% Prologix GPIB Configurator. See here:
% http://www.ke5fx.com/gpib/readme.htm#prologix
% Ensure your OSA and Prologix devices are set to the same GPIB address.
% TIP:
% Compile to standalone application for faster performance using:
% mcc -m OSA_Prologix
% Tested using Prologix GPIB-USB Controller 6.101.
% By Priyanth Mehta (18/04/2012)
%=========================================================================
clear all
clc
ABC='A';                                %Set trace here
delete(instrfindall)
obj1 = serial('COM9');                  %Set COM Port
status=get(obj1,'status');
if strcmp(status,'closed')
    g1 = serial('COM9');
else
    fclose(obj1);
    g1 = obj1;
end
g1.Terminator = 'CR/LF';
set(g1,'InputBufferSize',10*20001);     %Creates enough space for OSA data
set(g1,'Timeout',60);                   %Code times out if it exceeds 60secs
fopen(g1);                              %Opens connection to the OSA
idn=query(g1,'*IDN?');
disp(['Connected to: ' idn(1:4) ' ' idn(6:12)])
query(g1,'SGL');                    %Runs a single scan    
                                    %A pause(n) may be needed here if OSA runs too slow 
disp('Retreiving Wavelength...')
wave=str2num(query(g1,['WDAT' ABC ]));          %Acquires wavelength data
disp('Retreiving Level...')
value=str2num(query(g1,['LDAT' ABC ]));         %Acquires level data
wavelength=wave(2:end)';                        %Crops out relevant OSA data
level=value(2:end);
query(g1,'RPT');                                % Returns the scan to REPEAT mode
fclose(g1);                                     % Close connection to GPIB
set(g1,'InputBufferSize',512);                  % Resets InputBufferSize


figure(1)
hold on
plotbrowser('on')
% title('Raw Data')
plot(wavelength,level,'LineWidth',2)
ylim([-86 -6])
xlim([1549.41 1550.91])
grid on

% figure(2)
% hold on
% plotbrowser('on')
% plot(wavelength,level-max(level),'LineWidth',2)
% ylim([-25 0])
% xlim([1285 1330])
% grid on
% % this part aligns the graph
% level = movmean(level,100);
% % [Mpeak,Lpeak,W,ER] = findpeaks(level,wavelength,'MinPeakDistance',10);
% % vq = interp1(Lpeak,Mpeak,wavelength,'cubic');
% 
% % figure(3)
% % hold on
% % plotbrowser('on')
% % title('Smooth Data')
% % ylim([-25 1])
% % plot(wavelength,level-vq','LineWidth',2)
% % ylim([-25 1])
% % xlim([1285 1330])
% % grid on
% % hold off





