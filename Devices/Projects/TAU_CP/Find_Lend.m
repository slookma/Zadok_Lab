%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
lambda0 = 1550; % Optical wavelength [nm]
waveguideWidth = 700; % [nm]
R = 50e3; % Radius of curvature of the approaching waveguides [nm]
y0 = 50.49e3; % Separation between circles' center / 2 [nm]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

D = dir(['G:\users\Shai\Coupler_Lend_' num2str(lambda0) 'nm\neff*']);
d_vec  = zeros(length(D),1); % coupled waveguides separation [nm]
n_even = zeros(length(D),1); % Even modes' effective indices
n_odd  = zeros(length(D),1); % Odd  modes' effective indices

% Read d vector from files' names
for i = 1:length(D)
    temp = D(i).name;
    d_vec(i) = str2num(temp(10:end-2));
end
d_vec = sort(d_vec);

% Read even & odd effective indices from the files
for i = 1:length(d_vec)
    temp = readtable(fullfile('G:', 'users', 'Shai', ['Coupler_Lend_' num2str(lambda0) 'nm'], ['neff_vs_d' num2str(d_vec(i)) 'nm']));
    n_even(i) = table2array(temp(1,3));
    n_odd(i)  = table2array(temp(1,4));
end

d_vec = d_vec + waveguideWidth; % Convert from distance between facets of the waveguides to distance between the centers

% Compute Lc
beta_even = 2*pi*n_even / lambda0; % Propagation constants vector for even modes [nm^-1]
beta_odd  = 2*pi*n_odd  / lambda0; % Propagation constants vector for odd  modes [nm^-1]
S = abs(beta_even - beta_odd)/2; % Auxiliary variable [nm^-1]
Lc = pi./(2*S); % Effective coupling length [nm]


% Extrapolate
dd = d_vec(2) - d_vec(1);
f = fit(d_vec, Lc, 'exp1');
d_vec_ext = [d_vec; ((d_vec(end) + dd) : dd : 45e3)'];
Lc_ext = f.a * exp(f.b * d_vec_ext);


% Compute coupling coefficient over the entire "end" section:
%%%% Notice that if d_vec is not equally spaced, one should define the "dd" correctly
theta1 = pi/2 * sum(1./Lc .* (y0-d_vec/2) ./ (2*sqrt(R^2 - (y0 - d_vec/2).^2))) * dd;
theta1_ext = pi/2 * sum(1./Lc_ext .* (y0-d_vec_ext/2) ./ (2*sqrt(R^2 - (y0 - d_vec_ext/2).^2))) * dd;

T21 = sin(theta1)^2; % Reflection of power (based on simulated data only)
T21_ext = sin(theta1_ext)^2; % Reflection of power (based on extrapolation from simulated data)

Ll = 2 * Lc(1)/pi * (pi/4 - 2*theta1); % Required length of straight section (based on simulated data only) [nm]
Ll_ext = 2 * Lc_ext(1)/pi * (pi/4 - 2*theta1_ext); % Required length of straight section (based on extrapolation from simulated data) [nm]
% In case n_even and n_odd of the stright section are different (and given):
ne = 2.6021; % Data from Inbar
no = 2.5764; % Data from Inbar
Ll_ext = lambda0 / (ne - no) * (1/4 - 2*theta1_ext/pi); % Required length of straight section (based on extrapolation from simulated data) [nm]


