function[x,y,xsaw1,ysaw1,xsaw2,ysaw2,str]=RING_RACETRACK_cle2_N_taps_W3(Lc,d,R,x0,y0,Lt,NTAPS,filt,loss_fix,ss)

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
loss=6.5;                %dB/mm acoustic losses
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
% W=W/max(W);

%phase taps (summation of all shifts)
Dt(1)=0;    %no phase in first tap
for i=2:length(Dt)
    Dtt(i)=Dt(i)-(Dt(i-1));
end

Dt=Dtt+1*dR;
Dt(1)=0;

if NTAPS==2
    Dt=0*Dt;
end

N=200;      %number of points per curve
Ws=150;     %length of tap segment

if NTAPS>2
    dy=10;      %extension for first and last taps
else
    dy=0;
end

a=zeros(1,NTAPS);

lr=(((NTAPS-1)*2-6)*R-Lc)/2;

[x2,y2]=straight_cle(x0,y0,Lc);     %coupler length
[x3,y3]=curve_cle(x2(end),y2(end),1.5*pi,2*pi,R,N);

if NTAPS>2
    
    [x4,y4]=curve_cle(x3(end),y3(end),-1*pi,-1.5*pi,R,N);
    [x5,y5]=straight_cle(x4(end),y4(end),lr);
    [x6,y6]=curve_cle(x5(end),y5(end),-0.5*pi,0*pi,R,N);
    x0N=x6(end);
    y0N=y6(end);
else
    x4=[];y4=[];x5=[];y5=[];x6=[];y6=[];
    x0N=x3(end);
    y0N=y3(end);
end


%loop of TAPS
xN=[];yN=[];
xsaw1=zeros(1,NTAPS);xsaw2=zeros(1,NTAPS);
ysaw1=zeros(1,NTAPS);ysaw2=zeros(1,NTAPS);
xt=zeros(1,NTAPS);yt=zeros(1,NTAPS);

for n=1:NTAPS    
    np=sign(-mod(n,2)+0.5);
    
    if n==1
        [xN1,yN1]=line_cleN(x0N,y0N,[0,0],[0 dy]);
    else
        [xN1,yN1]=curve_cle(x0N,y0N,np*0.5*pi,np*pi,R,N);
    end
    
    [xN2,yN2,x1i,y1i,x2i,y2i,Wm(n),a(n)]=curve_SAW3(W(n),-np*Ws,xN1(end),yN1(end),ss);
    if np==-1
        xsaw1(n)=x2i;ysaw1(n)=y2i;
        xsaw2(n)=x1i;ysaw2(n)=y1i;
        xt(n)=xN2(end);yt(n)=yN2(end);
    elseif np==1
        xsaw2(n)=x2i;ysaw2(n)=y2i;
        xsaw1(n)=x1i;ysaw1(n)=y1i;
        xt(n)=xN2(1);yt(n)=yN2(1);
    end
        
    if n==NTAPS
        [xN3,yN3]=line_cleN(xN2(end),yN2(end),[0,0],[0 -dy]);
        xN4=[];yN4=[];
    else
        [xN3,yN3]=curve_cle(xN2(end),yN2(end),0*pi,-np*pi/2,R,N);
        [xN4,yN4]=straight_cle(xN3(end),yN3(end),-Dt(n+1));
    end
        
    xNn=[xN1;xN2;xN3;xN4];
    yNn=[yN1;yN2;yN3;yN4];
    x0N=xNn(end);
    y0N=yNn(end);
    
    xN=[xN;xNn];
    yN=[yN;yNn];
    n
end

x7=xN;
y7=yN;

if NTAPS>2
    [x8,y8]=curve_cle(x7(end),y7(end),1*pi,1.5*pi,R,N);
    [x9,y9]=straight_cle(x8(end),y8(end),lr+sum(Dt));
    [x10,y10]=curve_cle(x9(end),y9(end),0.5*pi,0*pi,R,N);
else
    x8=[];y8=[];x9=[];y9=[];x10=x7(end);y10=y7(end);
end

if Lc==0
    [x11,y11]=curve_cle(x10(end),y10(end),1*pi,1.6*pi,R,N);
else
    [x11,y11]=curve_cle(x10(end),y10(end),1*pi,1.5*pi,R,N);
end

x=[x2;x3;x4;x5;x6;x7;x8;x9;x10;x11];
y=[y2;y3;y4;y5;y6;y7;y8;y9;y10;y11];    

xsaw1=xsaw1';
xsaw2=xsaw2';
ysaw1=ysaw1';
ysaw2=ysaw2';

if fig_flag(1)==1
    figure(1)
    plot(x,y,'r');hold on
    axis equal
    plot(xt,yt,'*');
    hold on
end
%

delay_l=sum(sqrt((diff(x)).^2+(diff(y)).^2));

% d_saw=0;
% 
% d_saw=sum(sqrt((diff(x7)).^2+(diff(y7)).^2));
% d_saw=d_saw+sum(sqrt((diff(x10)).^2+(diff(y10)).^2));
% d_saw=d_saw+sum(sqrt((diff(x13)).^2+(diff(y13)).^2));
% d_saw=d_saw+sum(sqrt((diff(x16)).^2+(diff(y16)).^2));
% d_saw=d_saw+sum(sqrt((diff(x19)).^2+(diff(y19)).^2));
% d_saw=d_saw+sum(sqrt((diff(x22)).^2+(diff(y22)).^2))

if filt==1
    str=sprintf('LPF: Lc=%.2f um dL= %.2f um R=%.2f um Loss_f=%.0f um',Lc,delay_l,R,loss_fix);
elseif filt==2
    str=sprintf('HPF: Lc=%.2f um dL= %.2f um R=%.2f um Loss_f=%.0f um W2=%.2f',Lc,delay_l,R,loss_fix,W(2));
elseif filt==3
    str=sprintf('LPF_W: Lc=%.2f um dL= %.2f um R=%.2f um Loss_f=%.0f um',Lc,delay_l,R,loss_fix);
elseif filt==4
    str=sprintf('LPF_1-11-1-11: Lc=%.2f um dL= %.2f um R=%.2f um Loss_f=%.0f um',Lc,delay_l,R,loss_fix);
end
str_a=sprintf('%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f',a);
str=[str ' width ' str_a];

%saw calib
ng=3.72;
c=3e8;

for i=2:NTAPS
    I1=find(x==xt(1) & y==yt(1));
    I2=find(x==xt(i) & y==yt(i));
    I1=min(I1);I2=min(I2);
    delay_opt(i)=sum(sqrt((diff(x(I1:I2))).^2+(diff(y(I1:I2))).^2));
    delay_ac(i)=abs(x(I2)-x(I1));
    %delay_ac=0*delay_ac;    %for angled lines
    t_opt(i)=1*(delay_opt(i)*1e-6)/(c/ng);
    t_ac(i)=(delay_ac(i)*1e-6)/v150-((i-1)*Li*1e-6)/v150;
    phase(i)=t_opt(i)+t_ac(i);
end

phase(1)=0;
phase=(v150/(Lsaw*1e-6))*phase;

%%frequancy response
f=2e9:500e3:3e9;
Q=20e3;
% dn_n=1e-6/3.5;
% pm2am=dn_n*(d_saw/delay_l)*Q

% W_loss=ones(size(W_loss));      %no loss

%phase=[0 phase];
for n=1:NTAPS
        bw(n,:)=Wm(n)*W_loss(n)*exp(1i*2*pi*f*(((Li*1e-6)/v150)*n)+1*1i*2*pi*phase(n));
end
hw=(1/2)*sum(bw);

if fig_flag(2)==1
    if sum(fig_flag)>1
        figure(2)
    end
    plot(f*1e-9,mag2db(abs(hw/max(hw)))-0,'LineWidth',3);
    %plot(f*1e-9,mag2db(abs(hw*pm2am)),'LineWidth',3);
    ylim([-30 0]);
    xlim([2.2 2.6]);
    hold on

    xlabel('frequency [GHz]');
    ylabel('Magnitude (dB)');
    set(gca,'fontsize',20);

end

%%impulse reponse
if fig_flag(3)==1
    figure(3)
    imp=Wm.*W_loss.*exp(1i*2*pi*[phase]);
    t_imp=0:T:T*(length(imp)-1);
    stem(t_imp*1e9,real(imp));

    xlabel('Time[ns]');
    %ylabel('Magnitude (dB)');
    set(gca,'fontsize',20);

    hold on
end
str
end




