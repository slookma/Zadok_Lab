%% DC sup
DC = visa('agilent','USB0::0x2A8D::0x8F01::CN61450126::0::INSTR');
fopen(DC)
fprintf(DC, '%s\n', '*IDN?');
idn = fscanf(DC)

%% ILX
ilx = visa('agilent','USB0::0x1FDE::0x0005::82201716::0::INSTR');
fopen(ilx)
fprintf(ilx, '%s\n', '*IDN?');
idn = fscanf(ilx)

%% OSA
osa = visa('agilent','ASRL4::INSTR');
fopen(osa)
fprintf(osa, '%s\n', '*IDN?');
idn = fscanf(osa)

% fprintf(osa, '%s\n', ':SENSe:WAVelength:STOP?');
fprintf(osa, '%s\n', 'SGL'); % takes a single trace in the OSA

OSA_POW = (fscanf(osa));
fprintf(osa, '%s\n', ['WDAT' 'A']); % Acquires wavelength data
OSA_WL = (fscanf(osa));
fprintf(osa, '%s\n', ['LDAT' 'A']); % Acquires level data
OSA_POW = (fscanf(osa));

% fprintf(osa, '%s\n', ':SYSTem:RUNning:STOP');
% fprintf(osa, '%s\n', ':FORMat:DATA ASCII'); % Set format to ASCII
% fprintf(osa, '%s\n', ':TRACe:Y:DATa?');    % Request Y data (amplitude levels)
% OSA_POW = fscanf(osa);                       % Read the power levels
% fprintf(osa, '%s\n', ':TRACe:X:DATa?');    % Request X data (wavelengths)
% OSA_WL = fscanf(osa);                       % Read the wavelengths

%% DMM
Keithley = visa('agilent','USB0::0x05E6::0x2100::1242728::0::INSTR'); %Port_#0003.Hub_#0001
fopen(Keithley)
fprintf(Keithley, '%s\n', '*IDN?');
idn = fscanf(Keithley)
% fprintf(Keithley,'%s\n','SENSe:VOLTage:DC:NPLCycles 10')
% V_Dmm = str2double(query(Keithley,'MEASure:VOLTage:DC?'));


%% Loop
fprintf(DC, '%s\n', 'INSTrument CH1');
fprintf(DC, '%s\n', 'CURR 5');
fprintf(DC, '%s\n', 'VOLT 0');
fprintf(DC, '%s\n', 'OUTPut:STATe ON');
fprintf(Keithley,'%s\n','SENSe:CURRent:DC:NPLCycles 10');
I_Dmm = str2double(query(Keithley,'MEASure:CURRent:DC?'));


Responsivity = 1.1;
VoltStart = 0;
VoltEnd   = 6;
VoltN     = 150;
Voltages  = linspace(VoltStart, VoltEnd, VoltN);
ILX_Read = zeros(size(Voltages));
Keithley_read=zeros(size(Voltages));
WB = waitbar(0,'Please wait...');

for i = 1:length(Voltages)
    fprintf(DC, '%s\n', ['VOLT ' num2str(Voltages(i))]);
    pause(0.1) % Don't touch
    fprintf(ilx, '%s\n', 'POWer?');
    fprintf(Keithley,'%s\n','SENSe:CURRent:DC:NPLCycles 10');
    ILX_Read(i) = double(string((fscanf(ilx))));
    Keithley_read(i)=str2double(query(Keithley,'MEASure:CURRent:DC?'));
    pause(0.2)
    
    waitbar(i / length(Voltages), WB, ['Please Hold, ' num2str(i / length(Voltages) * 100, '%.2f') '% completed']);
end
close(WB)

% fprintf(DC, '%s\n', 'OUTPut:STATe OFF');
Keithley_Read = 10*log10(abs(Keithley_read)*1000/Responsivity); % chnage DC current to power in dBm.


figure
hold on
grid on
plot(Voltages, ILX_Read, '-*')
plot(Voltages, Keithley_Read, '--')
xlabel('TEC Voltage [V]')
ylabel('Transmission [dBm]')
legend('ILX','Detector')
% xlim([1.55 2.4])
hold off




%% Calibration
Volt(1)  = 0;
Volt(2)  = 0.2;
Volt(3)  = 0.4;
Volt(4)  = 0.6;
Volt(5)  = 0.8;
Volt(6)  = 1;
Volt(7)  = 1.2;
Volt(8)  = 1.4;
Volt(9)  = 1.6;
Volt(10) = 1.8;
Volt(11) = 2;
Volt(12) = 2.2;
Volt(13) = 2.4;
Volt(14) = 2.6;

Res(1)  = 11.08;
Res(2)  = 10.832;
Res(3)  = 10.582;
Res(4)  = 10.347;
Res(5)  = 10.112;
Res(6)  = 9.915;
Res(7)  = 9.689;
Res(8)  = 9.441;
Res(9)  = 9.195;
Res(10) = 8.990;
Res(11) = 8.780;
Res(12) = 8.430;
Res(13) = 8.220;
Res(14) = 7.930;

Temp(1)  = 22.7;
Temp(2)  = 23.3;
Temp(3)  = 23.8;
Temp(4)  = 24.3;
Temp(5)  = 24.8;
Temp(6)  = 25.1;
Temp(7)  = 25.8;
Temp(8)  = 26.3;
Temp(9)  = 27;
Temp(10) = 27.5;
Temp(11) = 28;
Temp(12) = 29;
Temp(13) = 29.5;
Temp(14) = 30.3;

WL(1)  = 1549.575;
WL(2)  = 1549.6225;
WL(3)  = 1549.67;
WL(4)  = 1549.7233;
WL(5)  = 1549.7730;
WL(6)  = 1549.8259;
WL(7)  = 1549.8795;
WL(8)  = 1549.9294;
WL(9)  = 1549.9769;
WL(10) = 1550.0332;
WL(11) = 1550.0980;
WL(12) = 1550.1750;
WL(13) = 1550.2390;
WL(14) = 1550.2695;

Temperatures = interp1(Volt, Temp, Voltages);
Wavelengths  = interp1(Volt, WL, Voltages);

%%
figure
hold on
grid on
plot(Temperatures, ILX_Read, '-*')
plot(Voltages, Keithley_Read, '--')
xlabel('TEC Temperature [C]')
ylabel('Transmission (ILX Read) [dB]')
hold off

%%
figure
hold on
grid on
plot(Wavelengths, ILX_Read, '-*')
plot(Voltages, Keithley_Read, '--')
xlabel('\lambda [nm]')
ylabel('Transmission (ILX Read) [dB]')
hold off