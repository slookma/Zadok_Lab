%% Define variables
Npoints = 5e3;
Nmodes  = 1;
% fac     = 9.8804e9;  % Capital omega detuning MECHANICAL WAVE FREQUENCY [s^-1]

% % For TM 400nm Rib:
% neff = 2.8109;
% ng   = 4.5677;

% % For TM 220nm Ridge:
% neff = 1.7294;
% ng   = 3.96385;

% % For TE 220nm Ridge:
% neff = 2.7199;
% ng   = 3.67315;

% For TM 220nm Rib:
neff = 1.6813;
ng   = 2.9842;

%% Read electric fields + displacement fields once (save tons of time)
EDFieldsFolder = 'TE_220nm_Efields'; % 'verification\275nm_Efields'; % 'TM_220nm_rib_Efields'; % 'TM_400nm_rib_Efields'; % 'TE_220nm_Efields';
Ex = comsol2matlab_c(fullfile(EDFieldsFolder, 'Ex.txt'), Npoints, 1, 0); % Electric field [V*m^-1]
Ey = comsol2matlab_c(fullfile(EDFieldsFolder, 'Ey.txt'), Npoints, 1, 0); % Electric field [V*m^-1]
Ez = comsol2matlab_c(fullfile(EDFieldsFolder, 'Ez.txt'), Npoints, 1, 0); % Electric field [V*m^-1]

Dx = comsol2matlab_c(fullfile(EDFieldsFolder, 'Dx.txt'), Npoints, 1, 0); % Electric displacement field [C*m^-2]
Dy = comsol2matlab_c(fullfile(EDFieldsFolder, 'Dy.txt'), Npoints, 1, 0); % Electric displacement field [C*m^-2]
Dz = comsol2matlab_c(fullfile(EDFieldsFolder, 'Dz.txt'), Npoints, 1, 0); % Electric displacement field [C*m^-2]


%% Run SBS_GAIN_func in a loop (in case the acoustic modes are saved in multiple files)
tic
folderName = 'TE_220nm_ridge_thick'; % 'verification\275nm_Ufields'; % 'TM_220nm_rib_thick\New'; % 'TM_220nm_rib_thick'; % 'TM_400nm_rib';
fac = str2double(table2array(readtable(fullfile(folderName, 'All_modes', 'fac.txt'))));
r   = table2array(readtable(fullfile(folderName, 'All_modes', 'XYZ.txt')));
GAMMA = zeros(1, Nmodes);
[~, calcIdx] = mink(abs(imag(fac)), 20);
for i = 1:length(calcIdx)
    mode_i = calcIdx(i);
    disp(mode_i);
    Ux  = str2double(table2array(readtable(fullfile(folderName, 'All_modes', ['Ux' num2str(mode_i) '.txt']))));
    Uy  = str2double(table2array(readtable(fullfile(folderName, 'All_modes', ['Uy' num2str(mode_i) '.txt']))));
    Uz  = str2double(table2array(readtable(fullfile(folderName, 'All_modes', ['Uz' num2str(mode_i) '.txt']))));
    Ux  = convert_to_mat(r(:,1), r(:,2), r(:,3), Ux);
    Uy  = convert_to_mat(r(:,1), r(:,2), r(:,3), Uy);
    Uz  = convert_to_mat(r(:,1), r(:,2), r(:,3), Uz);
    GAMMA(mode_i) = SBS_GAIN_func_given_E_D_U(Ex, Ey, Ez, Dx, Dy, Dz, Ux, Uy, Uz, Npoints, real(fac(mode_i)), neff, ng);
end
toc

%% Sort & Plot GAMMA
[GAMMA_sorted, I_sorted] = sort(real(GAMMA));
figure
plot(real(GAMMA_sorted), '-o')
xticks(1:512)
xticklabels(num2str(I_sorted'))
xlim([0 513])
grid on
xlabel('Mode #', 'FontSize', 15)
ylabel('\Gamma [W^{-1} \cdot m^{-1}]', 'FontSize', 15)

%% Scatter plot acoustic modes
for mode_i = I_sorted(end-4:end)
    Ux  = str2double(table2array(readtable(fullfile(folderName, 'All_modes', ['Ux' num2str(mode_i) '.txt']))));
    Uy  = str2double(table2array(readtable(fullfile(folderName, 'All_modes', ['Uy' num2str(mode_i) '.txt']))));
    Uz  = str2double(table2array(readtable(fullfile(folderName, 'All_modes', ['Uz' num2str(mode_i) '.txt']))));
    
    figure
    subplot(2,2,1)
    scatter3(r(:,1), r(:,2), r(:,3), [], abs(Ux), 'filled')
    colorbar
    view([0 1 0])
    title('U_x')
    
    subplot(2,2,2)
    scatter3(r(:,1), r(:,2), r(:,3), [], abs(Uy), 'filled')
    colorbar
    view([0 1 0])
    title('U_y')
    
    subplot(2,2,3)
    scatter3(r(:,1), r(:,2), r(:,3), [], abs(Uz), 'filled')
    colorbar
    view([0 1 0])
    title('U_z')
    
    subplot(2,2,4)
    scatter3(r(:,1), r(:,2), r(:,3), [], sqrt(abs(Ux).^2 + abs(Uy).^2 + abs(Uz).^2), 'filled')
    colorbar
    view([0 1 0])
    title('U_{tot}')
    
    sgtitle({['mode ' num2str(mode_i)], ['f_{ac} = ' num2str(real(fac(mode_i)*1e-9)) ' GHz'], ['\Gamma = ' num2str(real(GAMMA(mode_i)))]})
end

