function[Wf]=TapWeightCalc (R,Lsaw,NTAPS,filt,loss_fix,loss)

%Global parameters
% NTAPS=2;               %number of taps NTAPS>2
Lsaw=1.4;               %um acoustic wavelength
Li=R*2;                 %delay length (in space)
v150=Lsaw*1e-6*2.675e9; %m/s  saw velocity
%T=(Lsaw*1e-6)/v150;     %sec  delay length (in time)--- 
T=(Li*1e-6)/v150;     %sec  delay length (in time)--- 
% filt=1;                 %type of filter
% loss_fix=0;             %losses cancelations
fig_flag=[1 1 1];       %figs flags
%loss=7;                %dB/mm acoustic losses 13 dB/mm don't work
%
if NTAPS>2
    dR=Lsaw*1+(Lsaw-mod(Li,Lsaw)); %addtion in order to get integer number of wavelengths within delay
    Li=Li+dR;
else
    dR=0;
end

%losses cancelation
W_loss=db2pow(-loss*(0:Li*1e-3:Li*1e-3*(NTAPS-1)));
if loss_fix==1
    W_gain=fliplr(W_loss);
else
    W_gain=ones(size(W_loss));
end
%

%taps weights 
if filt==1
    %LPF
    W=ones(1,NTAPS);
%     W=[1 0.1];
elseif filt==2
    %HPF
    W=((0:(NTAPS/2-1))/(NTAPS/2-1)).^4;
    W=[-W fliplr(W)];
elseif filt==3
    %LPF_W
    Ti=6e-1;
    W=sinc(-(NTAPS/2-0.5)*Ti:Ti:(NTAPS/2-0.5)*Ti);
    %W(1)=1*sign(W(1));
elseif filt==4
    %LPF_SHIFT
    W=ones(1,NTAPS);
    W(2:2:end)=-W(2:2:end);
end
%

Dt=(Lsaw)*0.50*((1-sign(W))/2);     %phase of each tap into shift

W=abs(W);
W=W.*W_gain;

for i=1:NTAPS
    Ww=0.7:0.001:4;
    load('p_w3new.mat');
    Wsim=polyval(p,Ww*1e3)-26e-3;
    [ww,iw]=min(abs(Wsim-W(i)));
    Wf(i)=Ww(iw);
end
end




