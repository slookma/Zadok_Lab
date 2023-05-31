%% LIA connection
% LIA = visa('agilent','TCPIP0::192.168.2.4::inst0::INSTR');
LIA = visa('agilent','USB0::0xB506::0x2000::003969::0::INSTR');
fopen(LIA);
fprintf(LIA, '%s\n', '*IDN?');
idn_LIA = fscanf(LIA)
%% LIA take data
fprintf(LIA, '%s\n',  'SNAP? 2,3,15');
powerStr = fscanf(LIA);
commaP = find(powerStr==',');
powerR = str2double(powerStr(1:(commaP-1)));
%% RS connection
RS = visa('agilent','USB::0x0AAD::0x01dd::105528::INSTR');
% RS = visa('agilent','TCPIP0::192.171.2.115::inst0::INSTR');
fopen(RS);
%% RS take data
RS_SetFreq = @(freq)(['FREQ ' num2str(freq) ' KHz']);
fprintf(RS,RS_SetFreq(F));