function GAMMA = SBS_GAIN_func_given_E_D_U_verification(Ex_i, Ey_i, Ez_i, Dx_i, Dy_i, Dz_i, Ux, Uy, Uz, Npoints, fac, neff, ng, diam)
%SBS_GAIN_func calculates gamma (acoustic gain coefficient [W^-1*m^-1]) given COMSOL simulation results 
%   INPUTS:
%       - filesNames: A struct containing the paths to the data files
%       - Ex_i:       X component of electric field [V*m^-1]
%       - Ey_i:       Y component of electric field [V*m^-1]
%       - Ez_i:       Z component of electric field [V*m^-1]
%       - Dx_i:       X component of electric displacement field [C*m^-2]
%       - Dy_i:       Y component of electric displacement field [C*m^-2]
%       - Dz_i:       Z component of electric displacement field [C*m^-2]
%       - Ux:         X component of mechanical displacement field [m]
%       - Uy:         Y component of mechanical displacement field [m]
%       - Uz:         Z component of mechanical displacement field [m]
%       - Npoints:    Number of points in each dimension after interpolating data
%       - fac:        Acoustic frequncy, drawn from the optical COMSOL simulation
%       - neff:       Effective refractive index, drawn from the optical COMSOL simulation
%       - ng:         Refractive index of the group, drawn from the optical COMSOL simulation
%   OUTPUTS:
%       - GAMMA:      Acoustic gain coefficient [W^-1*m^-1]

verbose = false; % true <=> generate plots
RibRidge = 1; % 0 = Ridge ; 1 = Rib

%% Default values
if nargin < 10
    Npoints = 5e3;
end
if nargin < 11
    fac = 9.8804e9;  % Capital omega detuning MECHANICAL WAVE FREQUENCY [s^-1]
end
if nargin < 12
    neff = 1.7294;
end
if nargin < 13
    ng = 3.96385;
end

%% Physical constants
% For TM 220nm (Ridge):
% neff = 1.7294;
% ng = 3.96385;

% For TM 400nm (Rib):
% neff = 2.8109;
% ng = 4.5677;

omega = 2*pi*fac;

e0   = 8.8e-12; % Vacuum permittivity  [F*m^-1]
L    = 1550e-9; % Optical wavelength   [m]
c    = 3e8;     % Speed of light       [m*s^-1]
k0   = 2*pi/L;  % Wave number          [m^-1]
w    = c*k0;    % Optical frequency    [s^-1]
beta = neff*k0; % Propagation constant [m^-1]

% Air
p11_air = 0; % Photoelasticity  [unitless]
p12_air = 0; % Photoelasticity  [unitless]
p44_air = 0; % Photoelasticity  [unitless]
n_air   = 1; % Refractive index [unitless]
rho_air = 0; % Mass density     [kg*m^-3]

% SiO2
p11_SiO2 = 0.121;  % Photoelasticity  [unitless]
p12_SiO2 = 0.27;   % Photoelasticity  [unitless]
p44_SiO2 = -0.075; % Photoelasticity  [unitless]
n_SiO2   = 1.45;   % Refractive index [unitless]
rho_SiO2 = 2648;   % Mass density     [kg*m^-3]

% Si
p11_Si = -0.09;  % Photoelasticity  [unitless]
p12_Si = 0.017;  % Photoelasticity  [unitless]
p44_Si = -0.051; % Photoelasticity  [unitless]
n_Si   = 3.5;    % Refractive index [unitless]
rho_Si = 2329;   % Mass density     [kg*m^-3]

%As2S3
%p11_As2S3 = 0.25;
%p12_As2S3 = 0.24;
%p44_As2S3 = 0.005;
%n_As2S3   = 2.35;

%SU8
%p11_SU8 = 0.121;
%p12_SU8 = 0.27;
%p44_SU8 = -0.075;
%n_SU8   = 1.6;

%% "world" of 62.5umX62.5um of size 5000x5000
rworld = 6.5e-6;
rWG = diam / 2 * 1e-9;
x = linspace(-rworld, rworld, 5e3);
y = linspace(-rworld, rworld, 5e3);
[X, Y] = meshgrid(x, y);

%% MASK OF MATERIAL PROPERTIES
dc = Npoints - mod(Npoints,2);

%Air
p11_m = p11_air * ones(size(Ez_i));
p12_m = p12_air * ones(size(Ez_i));
p44_m = p44_air * ones(size(Ez_i));
n_m   = n_air   * ones(size(Ez_i));
rho_m = rho_air * ones(size(Ez_i));


%SiO2
p11_m(X.^2 + Y.^2 <= rWG^2) = p11_SiO2;
p12_m(X.^2 + Y.^2 <= rWG^2) = p12_SiO2;
p44_m(X.^2 + Y.^2 <= rWG^2) = p44_SiO2;
n_m(X.^2 + Y.^2 <= rWG^2)   = n_SiO2;
rho_m(X.^2 + Y.^2 <= rWG^2) = rho_SiO2;


%% Zero fields wherever there is no material (appears due to interpolation in griddata)
nonZero = double(rho_m ~= 0);
% Ex_i = Ex_i .* nonZero;
% Ey_i = Ey_i .* nonZero;
% Ez_i = Ez_i .* nonZero;
% Dx_i = Dx_i .* nonZero;
% Dy_i = Dy_i .* nonZero;
% Dz_i = Dz_i .* nonZero;
% Ux   = Ux   .* nonZero;
% Uy   = Uy   .* nonZero;
% Uz   = Uz   .* nonZero;

%% Plot
if verbose
    figure
    imagesc(x,y,n_m);
    set(gca,'YDir','normal');
end

%% OPTICAL FORCES ES NO dev
Epx = Ex_i*1j;
Epy = Ey_i*1j;
Epz = Ez_i*1j;% *-1j

Dpx = Dx_i*1j;
Dpy = Dy_i*1j;
Dpz = Dz_i*1j;% *-1j

BF  = -1; % BSBS=-1        FSBS=1
BFQ = BF; % BSBS=-1        FSBS=1
BFD = BF; %-1=NO CONJ      FSBS=1

q=2*beta*((1-BFQ)/2);     %q=0 for FSBS
% A=0.5*e0*n.^4;
% a_ac=q/1000;

if BFD == 1
    Esx = BF*conj(Epx);
    Esy = 1*conj(Epy);
    Esz = BF*conj(Epz);
    
    Dsx = BF*conj(Dpx);
    Dsy = 1*conj(Dpy);
    Dsz = BF*conj(Dpz);
elseif BFD == -1
    Esx = BF*(Epx);
    Esy = 1*(Epy);
    Esz = BF*(Epz);
    
    Dsx = BF*(Dpx);
    Dsy = 1*(Dpy);
    Dsz = BF*(Dpz);
end

Sxx = -0.5 * e0 * n_m.^4 .* (p11_m.*(Epx.*Esx) + p12_m.*(Epy.*Esy) + p12_m.*(Epz.*Esz)); % Stress tensor element [N*m^-2]
Syy = -0.5 * e0 * n_m.^4 .* (p12_m.*(Epx.*Esx) + p11_m.*(Epy.*Esy) + p12_m.*(Epz.*Esz)); % Stress tensor element [N*m^-2]
Szz = -0.5 * e0 * n_m.^4 .* (p12_m.*(Epx.*Esx) + p12_m.*(Epy.*Esy) + p11_m.*(Epz.*Esz)); % Stress tensor element [N*m^-2]

Syz = -0.5 * e0 * n_m.^4 .* p44_m.*(Epy.*Esz + Epz.*Esy); % Stress tensor element [N*m^-2]
Sxz = -0.5 * e0 * n_m.^4 .* p44_m.*(Epx.*Esz + Epz.*Esx); % Stress tensor element [N*m^-2]
Sxy = -0.5 * e0 * n_m.^4 .* p44_m.*(Epx.*Esy + Epy.*Esx); % Stress tensor element [N*m^-2]

dx = x(2) - x(1); % m
dy = y(2) - y(1); % m

[divx_Sxx, ~]        = gradient(Sxx, dx, dy);
[~, divy_Syy]        = gradient(Syy, dx, dy);
[~, divy_Syz]        = gradient(Syz, dx, dy);
[divx_Sxz, ~]        = gradient(Sxz, dx, dy);
[divx_Sxy, divy_Sxy] = gradient(Sxy, dx, dy);
% [divx_Szz, divy_Szz] = gradient(Szz, dx, dy);

fx = 1i*q*Sxz - 1*divy_Sxy - 1*divx_Sxx; % Electrostrictive force [N*m^-3]
fy = 1i*q*Syz - 1*divx_Sxy - 1*divy_Syy; % Electrostrictive force [N*m^-3]
fz = 1i*q*Szz - 1*divx_Sxz - 1*divy_Syz; % Electrostrictive force [N*m^-3]

%% Radiation pressure
[divx_e,     divy_e]     = gradient(n_m.^2, dx, dy);
[divx_e_inv, divy_e_inv] = gradient(n_m.^-2, dx, dy);

Fx_RP = -0.5 * e0 * (Esy.*Epy + Esz.*Epz) .* divx_e + 0.5*(e0^-1) .* (Dsx.*Dpx) .* divx_e_inv; % Radiation pressure [N*m^-2]
Fy_RP = -0.5 * e0 * (Esx.*Epx + Esz.*Epz) .* divy_e + 0.5*(e0^-1) .* (Dsy.*Dpy) .* divy_e_inv; % Radiation pressure [N*m^-2]

%% Quiver plots
if verbose
    figure(11)
    subplot(2, 2, 1)
    roi=1800:1:3200;
    quiver(x(roi),y(roi),Fx_RP(roi,roi),Fy_RP(roi,roi),30);
    title('RP')
    axis equal tight
    
    subplot(2, 2, 2)
    roi=1800:5:3200;
    quiver(x(roi),y(roi),fx(roi,roi),fy(roi,roi),5);
    title('ES')
    axis equal tight
    
    subplot(2, 2, 3.5)
    quiver(x(roi),y(roi),real(Ux(roi,roi)),real(Uy(roi,roi)),1);
    title('UxUy')
    axis equal tight
end

% %%
% QTEST=trapz(y,trapz(x,abs(fx),2))*1e3   %pN/(mW*um)
% QTEST_RP=trapz(y,trapz(x,Fx_RP,2))*1e3   %pN/(mW*um)

%% Total forces
% % The reason we can add f [N*m^-3] and F_RP [N*m^-2] is that the RP term
% % is implicitly multiplied by a delta function of position (exists only
% % at the boundary), which adds another [m^-1] unit
% % % % FxT = fx + Fx_RP; % [N*m^-3]
% % % % FyT = fy + Fy_RP; % [N*m^-3]
% % % % FzT = fz;         % [N*m^-3]

% Save only boundary
FxT = Fx_RP; % [N*m^-3]
FyT = Fy_RP; % [N*m^-3]
FzT = 0;     % [N*m^-3]

%% OPTINAL: Plot the forces
if verbose
    f1 = figure('Position', [200 400 1200 400]);
    for i = 1:3
        switch i
            case 1
%                 field = FxT;
%                 fieldName = 'FxT';
                field = FxT.*cos(atan2(Y,X)) + FyT.*sin(atan2(Y,X));
                fieldName = 'FrT';
            case 2
%                 field = FyT;
%                 fieldName = 'FyT';
                field = -FxT.*sin(atan2(Y,X)) + FyT.*cos(atan2(Y,X));
                fieldName = 'FtT';
            case 3
                field = FzT;
                fieldName = 'FzT';
        end
        
        subplot(1,3,i)
        imagesc(x*1e9, x*1e9, real(field))
        hold on
        plot(275*cos(0:0.01:2*pi), 275*sin(0:0.01:2*pi), '--k', 'LineWidth', 0.3)
        xlim([-1 1]*3e2)
        ylim([-1 1]*3e2)
        title(fieldName)
        xlabel('x [nm]')
        ylabel('y [nm]')
        set(gca,'YDir','normal')
        axis equal
        caxis([-1 1] * 0.1 * max([abs(FxT(:)); abs(FyT(:)); abs(FzT(:))]))
        colorbar
    end
end

%% Normalization factors
%  TAKE REAL PART (NOT SURE ABOUT THIS!)
Ux = real(Ux);
Uy = real(Uy);
Uz = real(Uz);

FxT = real(FxT);
FyT = real(FyT);
FzT = real(FzT);

% Calculate normalization factors
PUacx = trapz(y, trapz(x, abs(Ux.*rho_m.*Ux), 2)); % Normalization factor: sum over U*rho*U [kg*m^-1] * m^2 from the integral
PUacy = trapz(y, trapz(x, abs(Uy.*rho_m.*Uy), 2)); % Normalization factor: sum over U*rho*U [kg*m^-1] * m^2 from the integral
PUacz = trapz(y, trapz(x, abs(Uz.*rho_m.*Uz), 2)); % Normalization factor: sum over U*rho*U [kg*m^-1] * m^2 from the integral
PUac  = PUacx + PUacy + PUacz;

PEx = trapz(y, trapz(x, abs(Epx.*(e0*n_m.^2).*Epx), 2)); % Normalization factor: sum over E*eps*E [N*m^-2] * m^2 from the integral
PEy = trapz(y, trapz(x, abs(Epy.*(e0*n_m.^2).*Epy), 2)); % Normalization factor: sum over E*eps*E [N*m^-2] * m^2 from the integral
PEz = trapz(y, trapz(x, abs(Epz.*(e0*n_m.^2).*Epz), 2)); % Normalization factor: sum over E*eps*E [N*m^-2] * m^2 from the integral
PE  = PEx + PEy + PEz;

%% Overlap integral
GAMMA = 0;
bestAng = 0;
for Ang = (0:5:180)
    
    Ux_rot =  imrotate(Ux, Ang, 'crop');
    Uy_rot =  imrotate(Uy, Ang, 'crop');
    Uz_rot =  imrotate(Uz, Ang, 'crop');
    
%     Qc = conj(Ux).*FxT + conj(Uy).*FyT + conj(Uz).*FzT;   % Integrand [N*m^-2]
    Qc = conj(Ux_rot).*FxT + conj(Uy_rot).*FyT + conj(Uz_rot).*FzT;   % Integrand [N*m^-2]
    Qc_I = trapz(y, trapz(x, Qc, 2)); % Sum Qc over dx dy [N]
    
    %% Gain factor
    % Qm = 1e3; % dvir and hagai
    Qm = 300 * (9e9 / fac)^2; % ERC
    [GAMMA, oldORnew] = max([GAMMA, (2 * w * Qm * abs(Qc_I)^2) / (omega^2 * (c/ng)^2 * PE^2 * PUac)]); % [m^-1*W^-1] (Eq. 10 from P. Rakich)
    if oldORnew == 2
        bestAng = Ang;
    end
end

end

