%% Read U_All (in case the acoustic modes are saved in a single file)
Nmodes = 8;
folderName = 'verification\700nm_Ufields'; % 'TM_220nm_rib_thick\New'; % 'TM_220nm_rib_thick'; % 'TM_220nm_ridge_thick'; %'TM_400nm_rib';
T = readtable(fullfile(folderName, 'U_all.txt'));
T1 = table2array(T(16:end,1));
% T1 = table2array(T);

r = zeros(length(T1), 3);
U_all = zeros(length(T1), Nmodes*4);

WB = waitbar(0,'Please wait...');
%%
tic
for i = 1:size(U_all,1)
    waitbar(i/size(U_all,1), WB, [num2str(i/size(U_all,1) * 100, '%.2f') '% Completed']);
    
    temp = T1(i,1);
    temp2 = split(temp);
    r(i,:) = str2double(temp2(1:3).');
    for j = 1:size(U_all,2)
        U_all(i,j) = str2double(temp2(j+3));
    end
end
toc

close(WB)

%% Parse to multiple files
axisNames = {'x', 'y', 'z'};
WB = waitbar(0,'Please wait...');
for mode_i = 1:Nmodes
    waitbar(mode_i/Nmodes, WB, [num2str(mode_i/Nmodes * 100, '%.2f') '% Completed']);
    for axis_i = 1:3
        T_i = array2table(U_all(:, 4*(mode_i-1) + axis_i));
        writetable(T_i, fullfile(folderName, 'All_modes', ['U' char(axisNames{axis_i}) num2str(mode_i) '.txt']));
    end
end
close(WB)

%% Write a file with acoustic frequencies
fac = U_all(1, 4:4:end)';
T = array2table(fac);
writetable(T, fullfile(folderName, 'All_modes', 'fac.txt'));

%% Write a file with x,y,z coordinates
T = array2table(r);
writetable(T, fullfile(folderName, 'All_modes', 'XYZ.txt'));
