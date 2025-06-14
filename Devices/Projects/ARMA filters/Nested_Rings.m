figure

N      = 100000;
alpha  = 1*100; % [dB/m]
n      = 4.2; % [Si eff index (Matan)]
c      = 299792458; % [m*s^-1]
L1     = 2*pi*100e-6; % [m]

% for L2 = 2*pi*1e-6*linspace(50,100,1000)

L2     = 2*pi*100e-6; % [m]
L3     = 2*pi*100e-6; % [m]
T1     = L1*n/c; % [s]
T2     = L2*n/c; % [s]
T3     = L3*n/c; % [s]
gamma1 = 10^(-alpha*L1/20);
gamma2 = 10^(-alpha*L2/20);
gamma3 = 10^(-alpha*L3/20);

for c2 = linspace(gamma2,1,60)

    % c2     = gamma2;      % critical coupling for nested rings
    c1     = gamma1; % critical coupling for nested rings
    s1     = sqrt(1-c1^2);
    s2     = sqrt(1-c2^2);
    phi1   = 0;
    phi2   = 0;
    lambda = linspace(1548*1e-9, 1552*1e-9, N); % [m]
    k      = 2*pi./lambda; % [rad*m^-1]
    FSR1   = lambda(end/2)^2/(lambda(end/2) + n*L1); %[m]
    FSR2   = lambda(end/2)^2/(lambda(end/2) + n*L2); %[m]


    TF_tot = c1 - (s1^2*gamma1*exp(-1i*(phi1 + n*k*L1)))./(1 - c1*c2*gamma1*exp(-1i*(phi1 + n*k*L1))) .* (c2 - (s2^2*gamma2*exp(-1i*(phi2 + n*k*L2)))./(1 - c2*gamma2*exp(-1i*(phi2 + n*k*L2))));
    TF_cascade = (c1 - (s1^2*gamma1*exp(-1i*(phi1 + n*k*L1)))./(1 - c1*gamma1*exp(-1i*(phi1 + n*k*L1)))) .* (c2 - (s2^2*gamma2*exp(-1i*(phi2 + n*k*L2)))./(1 - c2*gamma2*exp(-1i*(phi2 + n*k*L2))));
    
    ylims = [min([abs(TF_tot).^2, abs(TF_cascade).^2]), max([abs(TF_tot).^2, abs(TF_cascade).^2])];

    subplot(2,1,1)
    semilogy(lambda*1e9, abs(TF_tot).^2);
    xlim([1548 1552])
    ylim(ylims)

    subplot(2,1,2)
    semilogy(lambda*1e9, abs(TF_cascade).^2);
    xlim([1548 1552])
    ylim(ylims)

    sgtitle(['c2 = ' num2str(c2,'%.4f') ' ; L2 = 2*pi*' num2str(L2*1e6/(2*pi), '%.1f'), ' um'])
    drawnow
    pause(0.2)
end