%% to calculate L_coupling for TM d = 300e-9 RIB WG
% close all
clear all


W = [330 400 500];
n_odd = [2.5414 2.5757 2.6185];
n_even = [2.5692 2.6014 2.6417];

L = 0:1e-6:100e-6;
lambda = 1550e-9;
k0 = 2*pi/lambda;
beta_odd = n_odd*k0;
beta_even = n_even*k0;
S = (beta_even - beta_odd)/2;
Lc = pi./(2*S);
for i = 1:length(W)
    kappa(i,:) = (sin((pi/2).*((L + 9.29e-6)./Lc(i)))).^2;
end
figure
plot(L*1e6, kappa);
title ('TM coupling analysis - RIB WG')
xlabel('L (coupling length) [\mum]');
ylabel(' \kappa (coupling coeff)');
legend('330','400','500')