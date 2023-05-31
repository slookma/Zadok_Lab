%% LIA connection
% LIA = visa('agilent','TCPIP0::192.168.2.4::inst0::INSTR');
LIA = visa('agilent','USB0::0xB506::0x2000::003969::0::INSTR');
fopen(LIA);
fprintf(LIA, '%s\n', '*IDN?');
idn_LIA = fscanf(LIA)
%% LIA take data
dt = 0.1; % [s]
for i = 1:100
    t(i) = now;
    pause(max([(dt - (t(i)-t(max([i,2])-1))*24*60*60) , 0]))
    fprintf(LIA, '%s\n',  'SNAP? 2,3');
    powerStr = fscanf(LIA);
    % PERFORM THESE OUTSIDE THE LOOP:
    commaP = find(powerStr==',');
    powerR(i) = str2double(powerStr(1:(commaP-1)));
    powerT(i) = str2double(powerStr(commaP:end));
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end
treal = (t - t(1))*24*60*60;

%%
T1 = now;
pause(3);
T2 = now;
(T2-T1)*24*60*60