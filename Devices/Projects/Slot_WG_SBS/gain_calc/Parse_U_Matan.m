%% Read U_All (in case the acoustic modes are saved in a single file)
folderName  = 'Data\Non-ideal_TM_SOI_400nm_gap_40nm_fin_100nm_delta_60nm';
destName    = 'Data\Non-ideal_TM_SOI_400nm_gap_40nm_fin_100nm_delta_60nm\All_modes';
fileName    = 'Uz_anti.txt';
writeXYZ    = 1;

T = readtable(fullfile(folderName, fileName));

U_table = T(2:end,4);
writetable(U_table, fullfile(destName, fileName));

if writeXYZ
    r_table = T(2:end,1:3);
    writetable(r_table, fullfile(destName, 'XYZ.txt'));
end
