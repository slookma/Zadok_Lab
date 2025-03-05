k1 = 0.942; %(Matan) % 0.1035; %(Madsen) %0.489; %(Saawan)
k2 = 0.942; %(Matan) % 0.1035; %(Madsen) %0.489; %(Saawan)
k3 = 0.484; %(Matan) % 0.3551; %(Madsen) %0.943; %(Saawan)
k4 = 0.484; %(Matan) % 0.3551; %(Madsen) %0.943; %(Saawan)

alpha  = 1*100; % [dB/m]
n      = 4.2; % [Si eff index (Matan)] % 1.9963; % [SiN refractive index]
c      = 299792458; % [m*s^-1]
L      = 2*pi*100e-6; % [m]
T      = L*n/c; % [s]
N      = 1000;
lambda = linspace(1548*1e-9, 1552*1e-9, N); % [m]
k      = 2*pi./lambda; % [rad*m^-1]
gamma  = 10^(-alpha*L/20);
FSR    = lambda(end/2)^2/(lambda(end/2) + n*L);
DC_vec = linspace(20,60,100);


f1 = figure('Position', [100,70,1100,550]);
idx = 1;
for DC = DC_vec
    phi1 =  DC/100 * pi;
    phi2 = -DC/100 * pi;
    phi3 = -DC/100 * pi;
    phi4 =  DC/100 * pi;
    phit =  DC/100 * pi;
    
    T1 = (sqrt(1-k1) - gamma*exp(-1j*n*k*L-1j*phi1))./(1 - sqrt(1-k1)*gamma*exp(-1j*n*k*L-1j*phi1));
    T2 = (sqrt(1-k2) - gamma*exp(-1j*n*k*L-1j*phi2))./(1 - sqrt(1-k2)*gamma*exp(-1j*n*k*L-1j*phi2));
    T3 = (sqrt(1-k3) - gamma*exp(-1j*n*k*L-1j*phi3))./(1 - sqrt(1-k3)*gamma*exp(-1j*n*k*L-1j*phi3));
    T4 = (sqrt(1-k4) - gamma*exp(-1j*n*k*L-1j*phi4))./(1 - sqrt(1-k4)*gamma*exp(-1j*n*k*L-1j*phi4));
    
    H11 = 1/2  *(T1.*T3  - T2.*T4*exp(-1j*phit));
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    Loss = 10*log10(abs(H11).^2);
    Loss = Loss - max(Loss);
    
    a = zeros(1,5);
    b = zeros(1,5);
    z = zeros(4,1);
    p = zeros(4,1);
    
    z(1) = gamma / sqrt(1-k1) * exp(-1j*phi1);
    z(2) = gamma / sqrt(1-k2) * exp(-1j*phi2);
    z(3) = gamma / sqrt(1-k3) * exp(-1j*phi3);
    z(4) = gamma / sqrt(1-k4) * exp(-1j*phi4);
    p(1) = gamma * sqrt(1-k1) * exp(-1j*phi1);
    p(2) = gamma * sqrt(1-k2) * exp(-1j*phi2);
    p(3) = gamma * sqrt(1-k3) * exp(-1j*phi3);
    p(4) = gamma * sqrt(1-k4) * exp(-1j*phi4);
    
    a(1) = 2;
    a(2) = -2*sum(p);
    a(3) = 2*(p(1)*p(2) + p(1)*p(3) + p(1)*p(4) + p(2)*p(3) + p(2)*p(4) + p(3)*p(4));
    a(4) = -2*(p(1)*p(2)*p(3) + p(1)*p(2)*p(4) + p(1)*p(3)*p(4) + p(2)*p(3)*p(4));
    a(5) = 2*prod(p);
    
    b(1) = 1 - exp(-1j*phit);
    b(2) = -(z(1)+p(2)+z(3)+p(4) - exp(-1j*phit) * (p(1)+z(2)+p(3)+z(4)));
    b(3) = z(1)*p(2) + z(3)*p(4) + z(1)*z(3) + z(1)*p(4) + p(2)*z(3) + p(2)*p(4) - exp(-1j*phit) * (p(1)*z(2) + p(3)*z(4) + p(1)*p(3) + p(1)*z(4) + z(2)*p(3) + z(2)*z(4));
    b(4) = -(z(1)*p(2)*z(3) + z(1)*p(2)*p(4) + z(1)*z(3)*p(4) + p(2)*z(3)*p(4) - exp(-1j*phit) * (p(1)*z(2)*p(3) + p(1)*z(2)*z(4) + p(1)*p(3)*z(4) + z(2)*p(3)*z(4)));
    b(5) = z(1)*p(2)*z(3)*p(4) - exp(-1j*phit) * (p(1)*z(2)*p(3)*z(4));
    
    subplot(1,2,1)
    zplane(b,a)
    legend('Zeros', 'Poles')
    grid on
    % Design the figure a bit better
    ax = gca;
    datasets = ax.Children;
    datasets(1).LineWidth = 1.5;
    datasets(2).LineWidth = 1.5;
    datasets(3).LineWidth = 1.5;
    datasets(2).Color = [0 0.4470 0.7410];
    datasets(3).Color = [0.8500 0.3250 0.0980];
    hold on
    plot([-1,1]*5, [0,0]*5, 'k', 'LineWidth', 1.2)
    plot([0,0]*5, [-1,1]*5, 'k', 'LineWidth', 1.2)
    legend('Zeros', 'Poles')
    xlim([-1,1]*1.2)
    ylim([-1,1]*1.2)
    set(gca,'fontsize',14)
    hold off
    
    subplot(1,2,2)
    plot(lambda*1e9, Loss)
    xlim([lambda(1) lambda(end)]*1e9)
    ylim([-50 5])
    grid on
    set(gca,'fontsize',14)
    title(['Duty Cycle = ' num2str(DC, '%.2f') '%'], 'FontSize', 20)
    xlabel('\lambda [nm]', 'FontSize', 20)
    ylabel('Normalized PSD [dB]', 'FontSize', 20)
    drawnow
    F(idx) = getframe(gcf);
    idx = idx + 1;
end


% create the video writer with 1 fps
writerObj = VideoWriter('myVideo.avi');
writerObj.FrameRate = 5;
% set the seconds per image
% open the video writer
open(writerObj);
% write the frames to the video
for i=1:length(F)
    % convert the image to a frame
    frame = F(i) ;
    writeVideo(writerObj, frame);
end
% close the writer object
close(writerObj);


