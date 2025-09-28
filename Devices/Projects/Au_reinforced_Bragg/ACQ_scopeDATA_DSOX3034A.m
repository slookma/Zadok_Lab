scope = visadev('USB0::0x0957::0x17A4::MY54232198::0::INSTR');
idn = writeread(scope, "*IDN?");
%%
% Set input buffer size for waveform data
scope.InputBufferSize = 100000;

% Open connection
fopen(scope);

% Set data source to channel 4
fprintf(scope, ':WAV:SOUR CHAN4');

% Set waveform format to BYTE (1 byte per point)
fprintf(scope, ':WAV:FORM BYTE');

% Set waveform mode to RAW (all points, not just screen)
fprintf(scope, ':WAV:MODE RAW');

% Set number of points to retrieve (optional; adjust as needed)
% fprintf(scope, ':WAV:POINTS 10000');

% Query preamble to get waveform format
fprintf(scope, ':WAV:PRE?');
preambleBlock = fscanf(scope);

% Parse preamble
preamble = str2double(strsplit(preambleBlock, ','));
% Preamble format:
% [format, type, points, count, x_increment, x_origin, x_reference, y_increment, y_origin, y_reference]

x_increment = preamble(5);
x_origin    = preamble(6);
x_reference = preamble(7);
y_increment = preamble(8);
y_origin    = preamble(9);
y_reference = preamble(10);

% Request waveform data
fprintf(scope, ':WAV:DATA?');

% Read back header and waveform data
rawData = fread(scope, scope.InputBufferSize, 'uint8');

% Parse the returned waveform data
% Skip header: find start of data (# character)
headerOffset = find(rawData == '#', 1);
numDigits = str2double(char(rawData(headerOffset + 1)));
numBytes = str2double(char(rawData(headerOffset + (2:1+numDigits)))');
dataStart = headerOffset + 1 + numDigits;
waveformData = rawData(dataStart : dataStart + numBytes - 1);

% Convert to voltage values
voltage = (waveformData - y_reference) * y_increment + y_origin;

% Time axis
time = ((0:length(voltage)-1) - x_reference) * x_increment + x_origin;

% Plot waveform
figure;
plot(time, voltage);
xlabel('Time (s)');
ylabel('Voltage (V)');
title('Waveform from Channel 4 of DSOX3034A');
grid on;

