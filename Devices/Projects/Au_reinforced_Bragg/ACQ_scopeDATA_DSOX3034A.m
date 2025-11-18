scope = visadev('USB0::0x0957::0x17A4::MY54232198::0::INSTR');
idn = writeread(scope, "*IDN?");
%%
channels = [2 4];

% Set input buffer size and timeout
scope.InputBufferSize = 1000000;
scope.Timeout = 10;  % Increase timeout to allow full waveform read

% Open connection
fopen(scope);

% === Set acquisition mode to average (once, before loop) ===
fprintf(scope, ':ACQ:TYPE AVER');     % Averaging mode
fprintf(scope, ':ACQ:COUN 32');       % Averaging count (adjustable)

idx = 1;
for ch = channels

    % === Set channel as waveform source ===
    fprintf(scope, [':WAV:SOUR CHAN' num2str(ch)]);
    pause(0.2);  % Let the scope switch internally

    % % === Force acquisition and wait ===
    % fprintf(scope, ':RUN');          % Single-shot acquisition
    % pause(5);  % Let the scope switch internally
    % fprintf(scope, ':STOP');          % Single-shot acquisition
    % fprintf(scope, '*WAI');           % Wait until acquisition is done

    % pause(0.2);

    % === Set waveform data format and mode ===
    fprintf(scope, ':WAV:FORM BYTE');
    fprintf(scope, ':WAV:MODE RAW');

    pause(0.2);

    % === (Optional) Reduce points if needed ===
    % fprintf(scope, ':WAV:POINTS 10000');

    % === Read preamble to get scaling factors ===
    fprintf(scope, ':WAV:PRE?');
    preambleBlock = fscanf(scope);
    preamble = str2double(strsplit(preambleBlock, ','));

    x_increment = preamble(5);
    x_origin    = preamble(6);
    x_reference = preamble(7);
    y_increment = preamble(8);
    y_origin    = preamble(9);
    y_reference = preamble(10);

    pause(0.2);

    % === Request waveform data ===
    fprintf(scope, ':WAV:DATA?');
    rawData = fread(scope, scope.InputBufferSize, 'uint8');

    % === Parse waveform block header ===
    headerOffset = find(rawData == '#', 1);
    numDigits = str2double(char(rawData(headerOffset + 1)));
    numBytes = str2double(char(rawData(headerOffset + (2:1+numDigits)))');
    dataStart = headerOffset + 1 + numDigits;

    % === Check if enough data was read ===
    if length(rawData) < dataStart + numBytes - 1
        warning('Incomplete data read from scope for channel %d.', ch);
        continue;
    end

    waveformData = rawData(dataStart : dataStart + numBytes - 1);

    % === Convert to voltage ===
    voltage(:,idx) = (waveformData - y_reference) * y_increment + y_origin;

    % === Create time axis ===
    time(:,idx) = ((0:length(voltage)-1) - x_reference) * x_increment + x_origin;

    % === Plot waveform ===
    figure;
    plot(time(:,idx), voltage(:,idx));
    xlabel('Time (s)');
    ylabel('Voltage (V)');
    title(['Waveform from Channel ' num2str(ch) ' of DSOX3034A']);
    grid on;

    idx = idx + 1;
end


% % % %%
% % % 
% % % fprintf(scope, ":ACQuire:TYPE AVERage");
% % % fprintf(scope, ":ACQuire:COMPlete 100");
% % % fprintf(scope, ":ACQuire:COUNt 128");
% % % fprintf(scope, ":DIGitize CHANnel2");
% % % fprintf(scope, ":WAVeform:SOURce CHANnel2");
% % % fprintf(scope, ":WAVeform:FORMat BYTE");
% % % fprintf(scope, ":WAVeform:POINts 500");
% % % data = fscanf(scope, ":WAVeform:DATA?");
