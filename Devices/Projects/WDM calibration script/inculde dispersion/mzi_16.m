clear all

%16 channels WDM MZI filter
clear;clc
% ld = 0.028e-3-160e-9; % the old one
ld = 31.6*1e-6-160e-9;  % we got this number by trying like apes.
lc = 2*ld;
lb = 2*lc;
la = 2*lb;

Ei = [1;0];
N = 3501;

Lbmzi = 0;
Lmzi = 13.5e-6;
alpha = 3;
alpha_ChG = 0*1500;

phi_a = 0*pi+1*pi;
phi_b1 = 0*pi+1*pi;
phi_b2 = 0.5*pi+1*pi;
phi_c1 = 0.5*pi+1*pi;
phi_c2 = 1*pi+1*pi;
phi_c3 = 0.25*pi+1*pi;
phi_c4 = 0.75*pi+1*pi;
phi_d1 = 0.75*pi;
phi_d2 = 0.25*pi;
phi_d3 = 0.5*pi;
phi_d4 = 1*pi;
phi_d5 = 0.625*pi;
phi_d6 = 0.125*pi;
phi_d7 = 0.375*pi;
phi_d8 = 0.875*pi;

lbmzi_a = 0*1e-6;
lbmzi_b1 = 0*1e-6;
lbmzi_b2 = 0*1e-6;
lbmzi_c1 = 0*1e-6;
lbmzi_c2 = 0*1e-6;
lbmzi_c3 = 0*1e-6;
lbmzi_c4 = 0*1e-6;



lbmzi_d1 = 0*1e-6;
lbmzi_d2 = 0*1e-6;
lbmzi_d3 = 0*1e-6;
lbmzi_d4 = 0*1e-6;
lbmzi_d5 = 0*1e-6;
lbmzi_d6 = 0*1e-6;
lbmzi_d7 = 0*1e-6;
lbmzi_d8 = 0*1e-6;

%                - t_d1
%         - - t_c1
%         |      - t_d2
%  - - -t_b1
%  |      |      - t_d3       
%  |      - - t_c2
%  |             - t_d4
%t_a1         
%  |             - t_d5
%  |      - - t_c3
%  |      |      - t_d6
%  - - -t_b2
%         |      - t_d7
%         - - t_c4
%                - t_d8

input = 't_a1'; % MZI test port
input_E=1*ones(1,N);
ind = 15; %(output 1-16)

if input(3)~='d' && input(3)~='c' && input(3)~='b'
    [~,~,Eouta]=mat_mzi([input_E;0*ones(1,N)],N,0,Lmzi,Lbmzi,la,phi_a,lbmzi_a,1,alpha,alpha_ChG);
    input_E=0*ones(1,N);
else
    Eouta=0*ones(2,N);
end
if input(3)~='d' && input(3)~='c' 
    [~,~,Eoutb1]=mat_mzi([input_E;Eouta(1,:)],N,0,Lmzi,Lbmzi,lb,phi_b1,lbmzi_b1,1,alpha,alpha_ChG);
    [~,~,Eoutb2]=mat_mzi([Eouta(2,:);input_E],N,0,Lmzi,Lbmzi,lb,phi_b2,lbmzi_b2,1,alpha,alpha_ChG);
    input_E=0*ones(1,N);
else
    Eoutb1=0*ones(2,N);
    Eoutb2=0*ones(2,N);
end
if input(3)~='d'
    [~,~,Eoutc1]=mat_mzi([input_E;Eoutb1(1,:)],N,0,Lmzi,Lbmzi,lc,phi_c1,lbmzi_c1,1,alpha,alpha_ChG);
    [~,~,Eoutc2]=mat_mzi([Eoutb1(2,:);input_E],N,0,Lmzi,Lbmzi,lc,phi_c2,lbmzi_c2,1,alpha,alpha_ChG);
    [~,~,Eoutc3]=mat_mzi([input_E;Eoutb2(1,:)],N,0,Lmzi,Lbmzi,lc,phi_c3,lbmzi_c3,1,alpha,alpha_ChG);
    [~,~,Eoutc4]=mat_mzi([Eoutb2(2,:);input_E],N,0,Lmzi,Lbmzi,lc,phi_c4,lbmzi_c4,1,alpha,alpha_ChG);
    input_E=0*ones(1,N);
else
    Eoutc1=0*ones(2,N);
    Eoutc2=0*ones(2,N);
    Eoutc3=0*ones(2,N);
    Eoutc4=0*ones(2,N);
end

switch ceil(ind/2)
    case 1
        [Tdb,lambda,Eoutd1]=mat_mzi([input_E;Eoutc1(1,:)],N,0,Lmzi,Lbmzi,ld,phi_d1,lbmzi_d1,floor(ind./ceil(ind/2)),alpha,alpha_ChG); %1/2
    case 2
        [Tdb,lambda,Eoutd2]=mat_mzi([Eoutc1(2,:);input_E],N,0,Lmzi,Lbmzi,ld,phi_d2,lbmzi_d2,floor(ind./ceil(ind/2)),alpha,alpha_ChG);
    case 3
        [Tdb,lambda,Eoutd3]=mat_mzi([input_E;Eoutc2(1,:)],N,0,Lmzi,Lbmzi,ld,phi_d3,lbmzi_d3,floor(ind./ceil(ind/2)),alpha,alpha_ChG);
    case 4
        [Tdb,lambda,Eoutd4]=mat_mzi([Eoutc2(2,:);input_E],N,0,Lmzi,Lbmzi,ld,phi_d4,lbmzi_d4,floor(ind./ceil(ind/2)),alpha,alpha_ChG);
    case 5
        [Tdb,lambda,Eoutd5]=mat_mzi([input_E;Eoutc3(1,:)],N,0,Lmzi,Lbmzi,ld,phi_d5,lbmzi_d5,floor(ind./ceil(ind/2)),alpha,alpha_ChG);
    case 6
        [Tdb,lambda,Eoutd6]=mat_mzi([Eoutc3(2,:);input_E],N,0,Lmzi,Lbmzi,ld,phi_d6,lbmzi_d6,floor(ind./ceil(ind/2)),alpha,alpha_ChG);
    case 7
        [Tdb,lambda,Eoutd7]=mat_mzi([input_E;Eoutc4(1,:)],N,0,Lmzi,Lbmzi,ld,phi_d7,lbmzi_d7,floor(ind./ceil(ind/2)),alpha,alpha_ChG);
    case 8
        [Tdb,lambda,Eoutd8]=mat_mzi([Eoutc4(2,:);input_E],N,0,Lmzi,Lbmzi,ld,phi_d8,lbmzi_d8,floor(ind./ceil(ind/2)),alpha,alpha_ChG);
end


figure(900)
hold on
plotbrowser('on')
plot(lambda*1e9,Tdb-max(Tdb),'LineWidth',3);       %main plot
ylim([-25 0]);
ylabel('Transmission [dB]','fontsize',20);
xlabel('Wavelength [nm]','fontsize',20);
grid on
set(gca,'fontsize',20);
set(gca, 'FontName', 'Times New Roman');
hold off

