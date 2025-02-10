ilx = visa('NI','USB0::0x1FDE::0x0005::82201716::0::INSTR');
%ilx = visa('NI', 'ILX');
fopen(ilx)
fprintf(ilx, '%s\n', '*IDN?');
idn = fscanf(ilx)
fprintf(ilx, '%s\n', 'POWer?');
fscanf(ilx)
% fclose(ilx)
