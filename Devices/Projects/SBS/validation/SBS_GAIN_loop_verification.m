%% Define variables
Npoints = 5e3;
saveData = 1;
for diam = [550 700 1100 1400] % [nm]
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

% % For TM 220nm Rib:
% neff = 1.6813;
% ng   = 2.9842;

switch diam
    case 550
        % For Tapered Fiber 0.55um diameter:
        neff = 1.0134928813322828;
        ng   = 1.114563646;
    case 700
        % For Tapered Fiber 0.7um diameter:
        neff = 1.0572345323420131;
        neff_1550 = neff;
        neff_1560 = 1.055559589025231;
        ng = neff_1550 - 1550 * (neff_1560 - neff_1550) / (1560 - 1550);
    case 1100
        % For Tapered Fiber 1.1um diameter:
        neff = 1.20990593345389;
        neff_1550 = neff;
        neff_1560 = 1.20770518958267;
        ng = neff_1550 - 1550 * (neff_1560 - neff_1550) / (1560 - 1550);
    case 1400
        % For Tapered Fiber 1.4um diameter:
        neff = 1.283742797398921;
        neff_1550 = neff;
        neff_1560 = 1.2820183379079115;
        ng = neff_1550 - 1550 * (neff_1560 - neff_1550) / (1560 - 1550);
end

folderName = [num2str(diam/2) 'nm_Ufields'];
fac = table2array(readtable(fullfile(folderName, 'All_modes', 'fac.txt')));
Nmodes = length(fac);

%% Read electric fields + displacement fields once (save tons of time)
EDFieldsFolder = [num2str(diam/2) 'nm_Efields']; % 'TM_220nm_rib_Efields'; % 'TM_400nm_rib_Efields'; % 'TE_220nm_Efields'; % 'TE_220nm_Efields';
% Ex = comsol2matlab_c_verification(fullfile(EDFieldsFolder, 'Ex.txt'), Npoints, 1, 0, 'cubic', diam); % Electric field [V*m^-1]
% Ey = comsol2matlab_c_verification(fullfile(EDFieldsFolder, 'Ey.txt'), Npoints, 1, 0, 'cubic', diam); % Electric field [V*m^-1]
% Ez = comsol2matlab_c_verification(fullfile(EDFieldsFolder, 'Ez.txt'), Npoints, 1, 0, 'cubic', diam); % Electric field [V*m^-1]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Treat Ex, Ey, Ez separately to maintain continuity in the transverse
% direction
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
TX = readtable(fullfile(EDFieldsFolder, 'Ex.txt'), 'Delimiter', '\t');
xComs = str2double(split(table2array(TX(9,1))));
yComs = str2double(split(table2array(TX(11,1))));
if diam == 550
    PComsX = str2double(split(table2array(TX(15,1))));
else
    PComsX = str2double(split(table2array(TX(13,1))));
end

TY = readtable(fullfile(EDFieldsFolder, 'Ey.txt'), 'Delimiter', '\t');
if diam == 550
    PComsY = str2double(split(table2array(TY(15,1))));
else
    PComsY = str2double(split(table2array(TY(13,1))));
end

TZ = readtable(fullfile(EDFieldsFolder, 'Ez.txt'), 'Delimiter', '\t');
if diam == 550
    PComsZ = str2double(split(table2array(TZ(15,1))));
else
    PComsZ = str2double(split(table2array(TZ(13,1))));
end

rclad = max(xComs);
x = linspace(-rclad, rclad, 5e3);
[X, Y] = meshgrid(x);

r_WG = diam*1e-9 / 2;
logical_WG_grid   = (X.^2 + Y.^2 <= r_WG^2);
logical_WG_nogrid = (xComs.^2 + yComs.^2 <= r_WG^2);

E_in_r  = griddata(xComs, yComs, (PComsX.*cos(atan2(yComs, xComs)) + PComsY.*sin(atan2(yComs, xComs))).*logical_WG_nogrid,    X, Y);
E_out_r = griddata(xComs, yComs, (PComsX.*cos(atan2(yComs, xComs)) + PComsY.*sin(atan2(yComs, xComs))).*(~logical_WG_nogrid), X, Y);

E_r = E_in_r.*logical_WG_grid + E_out_r.*(~logical_WG_grid);
E_r(isnan(E_r)) = 0;

E_t = griddata(xComs, yComs, -PComsX.*sin(atan2(yComs, xComs)) + PComsY.*cos(atan2(yComs, xComs)), X, Y);
E_t(isnan(E_t)) = 0;


xComs = str2double(split(table2array(TZ(9,1))));
yComs = str2double(split(table2array(TZ(11,1))));
Ez = griddata(xComs, yComs, PComsZ, X, Y);
Ez(isnan(Ez)) = 0;

Ex = E_r.*cos(atan2(Y,X)) - E_t.*sin(atan2(Y,X));
Ey = E_r.*sin(atan2(Y,X)) + E_t.*cos(atan2(Y,X));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


Dx = comsol2matlab_c_verification(fullfile(EDFieldsFolder, 'Dx.txt'), Npoints, 1, 0, 'cubic', diam); % Electric displacement field [C*m^-2]
Dy = comsol2matlab_c_verification(fullfile(EDFieldsFolder, 'Dy.txt'), Npoints, 1, 0, 'cubic', diam); % Electric displacement field [C*m^-2]
Dz = comsol2matlab_c_verification(fullfile(EDFieldsFolder, 'Dz.txt'), Npoints, 1, 0, 'cubic', diam); % Electric displacement field [C*m^-2]

%% Plot E fields

rworld = 6.5e-6;
rWG = diam / 2 * 1e-3;
x = linspace(-rworld, rworld, 5e3);
y = linspace(-rworld, rworld, 5e3);
[X, Y] = meshgrid(x, y);

verbose = 1;
if verbose
    f1 = figure('Position', [300 400 1000 500]);
    for i = 1:6
        switch i
            case 1
%                 field = Ex;
%                 fieldName = 'Ex';
                field = Ex.*cos(atan2(Y,X)) + Ey.*sin(atan2(Y,X));
                fieldName = 'Er';
            case 2
%                 field = Ey;
%                 fieldName = 'Ey';
                field = -Ex.*sin(atan2(Y,X)) + Ey.*cos(atan2(Y,X));
                fieldName = 'Et';
            case 3
                field = Ez;
                fieldName = 'Ez';
            case 4
%                 field = Dx;
%                 fieldName = 'Dx';
                field = Dx.*cos(atan2(Y,X)) + Dy.*sin(atan2(Y,X));
                fieldName = 'Dr';
            case 5
%                 field = Dy;
%                 fieldName = 'Dy';
                field = Dx.*cos(atan2(Y,X)) + Dy.*sin(atan2(Y,X));
                fieldName = 'Dy';
            case 6
                field = Dz;
                fieldName = 'Dz';
        end
        subplot(2,3,i)
        imagesc(x*1e9, y*1e9, real(field))
        xlim([-1 1]*8e2)
        ylim([-1 1]*8e2)
        title(fieldName)
        xlabel('x [nm]')
        ylabel('y [nm]')
        set(gca,'YDir','normal')
        axis equal
    end
    sgtitle(['Diameter = ' num2str(diam) 'nm'], 'FontSize', 13)
    drawnow
end

%% Run SBS_GAIN_func in a loop (in case the acoustic modes are saved in multiple files)
tic
folderName = [num2str(diam/2) 'nm_Ufields']; % 'TM_220nm_rib_thick\New'; % 'TM_220nm_rib_thick'; % 'TM_400nm_rib'; % 'TE_220nm_ridge_thick'; % 'TE_220nm_ridge_thick';
fac = table2array(readtable(fullfile(folderName, 'All_modes', 'fac.txt')));
r   = table2array(readtable(fullfile(folderName, 'All_modes', 'XYZ.txt')));
GAMMA = zeros(1, Nmodes);
[~, calcIdx] = mink(abs(imag(fac)), 20);
for i = 1:length(calcIdx)
    mode_i = calcIdx(i);
    disp(mode_i);
    Ux  = table2array(readtable(fullfile(folderName, 'All_modes', ['Ux' num2str(mode_i) '.txt'])));
    Uy  = table2array(readtable(fullfile(folderName, 'All_modes', ['Uy' num2str(mode_i) '.txt'])));
    Uz  = table2array(readtable(fullfile(folderName, 'All_modes', ['Uz' num2str(mode_i) '.txt'])));
    Ux  = convert_to_mat_verification(r(:,1), r(:,3), r(:,2), str2double(Ux));
    Uy  = convert_to_mat_verification(r(:,1), r(:,3), r(:,2), str2double(Uy));
    Uz  = convert_to_mat_verification(r(:,1), r(:,3), r(:,2), str2double(Uz));
    GAMMA(mode_i) = SBS_GAIN_func_given_E_D_U_verification(Ex, Ey, Ez, Dx, Dy, Dz, Ux, Uy, Uz, Npoints, real(fac(mode_i)), neff, ng, diam);
end
GAMMA = reshape(GAMMA, length(GAMMA), 1);
if saveData
    save(fullfile('taperedFiber_results_MB_real', ['GAMMA_' num2str(diam) 'nm.mat']), 'GAMMA', 'fac');
end
toc

%% OPTIONAL: Plot Displacement modes
verbose = 0;
if verbose
    f1 = figure('Position', [300 400 1000 500]);
    for i = 1:3
        switch i
            case 1
%                 field = Ux;
%                 fieldName = 'Ux';
                field = Ux.*cos(atan2(Y,X)) + Uy.*sin(atan2(Y,X));
                fieldName = 'Ur';
            case 2
%                 field = Uy;
%                 fieldName = 'Uy';
                field = -Ux.*sin(atan2(Y,X)) + Uy.*cos(atan2(Y,X));
                fieldName = 'Ut';
            case 3
                field = Uz;
                fieldName = 'Uz';
        end
        
        subplot(1,3,i)
        imagesc(x*1e9, x*1e9, real(field))
        hold on
        plot(diam/2*cos(0:0.01:2*pi), diam/2*sin(0:0.01:2*pi), 'k')
        xlim([-1 1]*(diam/2)*1.1)
        ylim([-1 1]*(diam/2)*1.1)
        title(fieldName)
        xlabel('x [nm]')
        ylabel('y [nm]')
        set(gca,'YDir','normal')
        axis equal
    end
    sgtitle(['Diameter = ' num2str(diam) 'nm'], 'FontSize', 13)
    drawnow
end

%% Sort & Plot GAMMA
[GAMMA_sorted, I_sorted] = sort(real(GAMMA));
verbose = 0;
if verbose
    figure
    plot(real(GAMMA_sorted), '-o')
    xticks(1:Nmodes)
    xticklabels(num2str(I_sorted'))
    xlim([0 Nmodes+1])
    grid on
    xlabel('Mode #', 'FontSize', 15)
    ylabel('$\Gamma [W^{-1} \cdot m^{-1}]$', 'Interpreter', 'latex', 'FontSize', 15)
    drawnow
end

%% Scatter plot acoustic modes
verbose = 0;
if verbose
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
    drawnow
end

end