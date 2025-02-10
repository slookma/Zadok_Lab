%%Elliptical Filter%%%%
%------1----------2-----
%---------3--------4-----
clear all
m_air = -6.15E5; %[RIU/m]
m_chg = -4.5E5; %[RIU/m]
input1 = 1;
input2 = 0;
lambda = 1549E-9:0.001E-9:1550E-9; %[m]
lambda_cent = 1550E-9;
n_lambda_cent = 1.564% for silicon2.7201;
n_group = n_lambda_cent-m_air*lambda_cent;
% fsr = (lambda_cent)^2/(n_group*dz);
m_si_air = -6.15E5; % dn/dl\ambda: coefficient for slop of streight line [RIU/m]
%2.7236

E_through = ones(1,length(lambda));

for i = 1:length(lambda)
n_air =  m_si_air.*(lambda(i)-lambda(1))+ 2.7236;
n_chg = m_chg.*(lambda(i)-lambda(1))+2.842;
n =n_air;
L = 0.0040451; % [m] ring length 1,3 655 um
L2= 0.0040451; % [m] ring length 2,4
Ld=5e-6;
c = 3E8; % [m/sec]
%lc = 1E-3; %coupling length [m]
%z_coupler = 0.5.*lc;
lc = 3E-3.*ones(1,length(lambda));                                           
z_coupler = 0.5.*lc; %coupler length [m]
%%%%%%%%%%%%%%%%%%%for ring %%%%%
a1=0.997; %loss in ring 1,3 
a2=0.997; %lloss in ring 2,4
k1=0.489; %couplin eoeff of ring 1
t1=sqrt(1-k1*k1);
k2=0.943; %couplin eoeff of ring 2
t2=sqrt(1-k2*k2);
k3=k1; %couplin eoeff of ring 3
t3=sqrt(1-k3*k3);
k4=k2; %couplin eoeff of ring 4
t4=sqrt(1-k4*k4);

ep1=86.1096*pi/180;  
ep2=-98.7306*pi/180;
%add this extra phase in eq of E2
ep3=-ep1;
ep4=-ep2;
th =2*pi*n*L/lambda(i); %phase of ring 1,3
th2s=2*pi*n*L2/lambda(i); %phase of ring 2,4
E3=-k1/(1-a1*t1*exp(1j*th+1*j*ep1));
E2=t1+(a1*k1*E3*exp(1j*th+1*j*ep1)); % only for ring 1 'E2'
E3s=-k3/(1-a1*t3*exp(1j*th+1*j*ep3));
E2s=t3+(a1*k3*E3s*exp(1j*th+1*j*ep3)); % only for ring 3 'E2s'
E3ss=-(k2*E2*exp(1j*Ld))/(1-a2*t2*exp(1j*th2s+1*j*ep2));
E2ss=(t2*E2*exp(1j*Ld))+(a2*k2*E3ss*exp(1j*th2s+1*j*ep2)); %for k2 and k1 combined 'E2ss'
E3ls=-(k4*E2s*exp(1j*Ld))/(1-a2*t4*exp(1j*th2s+1*j*ep4));
E2ls= (t4*E2s*exp(1j*Ld))+(a2*k4*E3ls*exp(1j*th2s+1*j*ep4)); % k3 and k4 combined 'E21s'
E3r=-k2/(1-a2*t2*exp(1j*th2s+1*j*ep2)); 
E2r=t2+(a1*k2*E3r*exp(1j*th2s+1*j*ep2)); %only for ring 2 'E2r'
E34=-k4/(1-a2*t4*exp(1j*th+1*j*ep4));
E44=t4+(a2*k4*E34*exp(1j*th+1*j*ep4)); %for k1, only ring 4 'E44'
 %combined output of mrr 1 and 3
%%%%%%%%%%%%%%%%%%% coupler%%%%%%%%%
th1 = (pi*z_coupler(i))./(2*lc(i)); %rad /kaapaL
th2 = (pi*z_coupler(i))./(2*lc(i)); %rad
kair = (2*pi*n_air)./lambda(i); %[m^-1]
kchg = (2*pi*n_chg)./lambda(i); %[m^-1]
coupler1 = [cos(th1),-1j*sin(th1);-1j*sin(th1), cos(th1)];
coupler2 = [cos(th2),-1j*sin(th2);-1j*sin(th2), cos(th2)];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
dz_air =1000e-6; %[m]; %mz arm length [m]
dz_chg = 0.0*L;
phi =54.5716*pi/180; %additional phase for MZ by chalco patch
phi2=-54.5716*pi/18;
% ring through transmition:
delay = [E2ss*exp(1j*kair*dz_air+1j*phi2),0;0,E2ls*exp(1j*kair*dz_air+1j*phi)]; %arma delay
delay2= [exp(1j*kair*dz_air),0;0,exp(1j*kair*dz_air+1j*phi)]; %mzi delay without rings

Pr(:,i)=E2r; %ring reso tran
Pr2(:,i)=E2r; %ring reso tran
output1(:,i) = coupler2*delay*coupler1*[input1;input2];
output2(:,i) = coupler2*delay2*coupler1*[input1;input2];%not sure 
through1 = output1(1,:); %through ouput
through2 = output2(1,:); %only for mzi no rings
cross1 = output1(2,:);  %cross output
end
Pt=Pr.*conj(Pr);
IPt=10*log10(Pt); %ring 1/4 trans
Pt2=Pr2.*conj(Pr2);
IPt2=10*log10(Pt2); %ring 3/2 trans
I_through2 = (abs(through2)).^2; %only mzi output
I_dB_through2 = 10*log10(I_through2); %lin to log scale only mzi output
I_cross1 = (abs(cross1)).^2; %E to P
I_dB_cross1 = 10*log10(I_cross1); %lin to log scale cross output

figure(159)
plot(lambda.*1e9,IPt,'r')
hold on
xlim([1545,1555]);
plot(lambda.*1e9,IPt2,'b')
legend('ring 1','ring 2')
%plot(lambda,I_dB_through2)
I_through1 = (abs(through1)).^2; %arma output
I_dB_through1 = 10*log10(I_through1); %lin to log scale through output
figure(216)
plot(lambda.*1e9,I_dB_through1,'r')
hold on
plot(lambda.*1e9,I_dB_cross1,'b');
%xlim([1545,1555]);
legend('through','cross')
alpha=(1/(0.23*L*100))*log(a1*a1)
