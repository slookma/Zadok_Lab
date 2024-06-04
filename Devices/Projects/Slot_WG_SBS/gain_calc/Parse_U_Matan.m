%% Read U_All (in case the acoustic modes are saved in a single file)
folderName  = 'Data\Ideal_TM_40nm_gap_300nm_SOI_fin_150nm';
destName    = 'Data\Ideal_TM_40nm_gap_300nm_SOI_fin_150nm\All_modes';
fileName    = 'Uz_anti.txt';
writeXYZ    = 1;

T = readtable(fullfile(folderName, fileName));

U_table = T(2:end,4);
writetable(U_table, fullfile(destName, fileName));

if writeXYZ
    r_table = T(2:end,1:3);
    writetable(r_table, fullfile(destName, 'XYZ.txt'));
end
