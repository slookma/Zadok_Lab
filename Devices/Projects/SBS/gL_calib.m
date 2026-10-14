Pp_Tap  = [7.3  , 4.3  , 1.3  , -1.7 , -4.7 ];
Ps_SMF  = [-2.25, -2.95, -3.24, -3.37, -3.46]; % 10.77
Ps_PS   = [-3.4 , -3.42, -3.44, -3.45, -3.48]; % 11.08
Ps_out  = [-3.57, -3.54, -3.5 , -3.5 , -3.53]; % 11.4
dPs_SMF = Ps_SMF - Ps_out;
dPs_PS  = Ps_PS  - Ps_out;

Pp_dB = 18.4 + Pp_Tap;
Pp_W = 10.^((Pp_dB-30)/10);

gL_SMF = dPs_SMF.*log(10)./(10*Pp_W);
gL_PS  = dPs_PS .*log(10)./(10*Pp_W);
gL_SMF_av = mean(gL_SMF);
gL_PS_av  = mean(gL_PS);

figure
plot(Pp_dB, gL_SMF)
hold on
yline(gL_SMF_av)
yline(gL_SMF_av + std(gL_SMF), 'k--')
yline(gL_SMF_av - std(gL_SMF), 'k--')
xlabel('P_{pump} [dB]')
ylabel('gL [W^{-1}')
title('SMF')


figure
plot(Pp_dB, gL_PS)
hold on
yline(gL_PS_av)
yline(gL_PS_av + std(gL_PS), 'k--')
yline(gL_PS_av - std(gL_PS), 'k--')
xlabel('P_{pump} [dB]')
ylabel('gL [W^{-1}')
title('PS Fiber')