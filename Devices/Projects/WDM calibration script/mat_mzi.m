function[Tdb,lambda,Eoutt]=mat_mzi(Ei,N,plot_i,Lmzi,Lbmzi,l,ph_mzi,lbmzi,ind,alpha,alpha_ChG)

%Lc - full coupling length
%Lmzi - mzi coupler length
%Lbmzi - mzi coupler burn length
%l - mzi delay length
%lbmzi - mzi delay burn length
%ind - port number

ldelay=l;

%N=1e4;
%lambda_i=[1e-6,2e-6];
%lambda_i=[1.5499e-6,1.5501e-6];
lambda_i=[1.28e-6,1.32e-6];
%lambda_i=[1.54e-6,1.545e-6];    %TM_full_etch

lambda=linspace(lambda_i(1),lambda_i(2),N);

%n=linspace(2.730914,2.718785,N);n10=2.724845; %no burn. wg dispersion. air
%n=linspace(2.746148,2.734317,N);n10=2.740228; %no burn. wg dispersion. air+sio2
%n=linspace(2.783897,2.774012,N);n10=2.778943; %no burn. wg dispersion. chalco+sio2
%nb=linspace(2.746212,2.734383,N);n20=2.740293; %max burn MT

%Lc=linspace(3.345934906e-5,3.225406277e-5,N); %Lc air 300nm space
%Lc=linspace(2.944438071e-5,2.846299810e-5,N); %Lc chalco+sio2 300nm space
%Lc=linspace(2.12297e-5,2.06191e-5,N); %Lc sio2 200nm space
%Lcb=linspace(2.687046343e-5,2.591534321e-5,N); %Lcb chalco+sio2 300nm

%
lambda1=[1.200e-6,1.300e-6];    %1300nm
%lambda1=[1.54e-6,1.545e-6];     %TM full etch

%n=[2.726,2.713];n10=2.72; %no burn. wg dispersion. only air
%n=[2.90352,2.896273];n10=2.899867; %no wg dispersion. chalco
%nb=[2.726,2.713];n10=2.72; %no burn. wg dispersion. air
%nb=[2.740016,2.727956];n10=2.733928; %no burn. wg dispersion. air+sio2
%n=[2.787174,2.777355];n10=2.782253; %no burn. wg dispersion. chalco+sio2
%nb=[2.746212,2.734383];n20=2.740293; %max burn MT
%n=[2.1,2.1];n10=2.1; %dvir chalco WG

%n=[1.6957,1.6877];  %   TM full etch (1540-1545)

%1300nm_ridge
n=[3.044,2.9551];%n10=2.899867; %chalco
nb=[2.9387,2.8761];%n10=2.72; %air
%
%
n=lambda*((n(2)-n(1))/(lambda1(2)-lambda1(1)))+((n(1)*lambda1(2))-(n(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
nb=lambda*((nb(2)-nb(1))/(lambda1(2)-lambda1(1)))+((nb(1)*lambda1(2))-(nb(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
%

%Lc=[3.345934906e-5,3.225406277e-5]; %Lc air 300nm space
%Lc=[2.944438071e-5,2.846299810e-5]; %Lc chalco+sio2 300nm A1Se9
%Lc=[2.69495e-5,2.61727e-5]; %Lc chalco+sio2 300nm A2Se3
%Lc=[2.12297e-5,2.06191e-5]; %Lc sio2 200nm space
%Lcb=[2.687046343e-5,2.591534321e-5]; %Lcb chalco+sio2 300nm 

%1300nm_ridge chg
neven_chg=[2.800154,2.790908];
nodd_chg=[2.773582,2.76308];
%
%neven_chg=[2.800154,2.790908];
%nodd_chg=[2.773582,2.76308];
%neven_chg=[2.701,2.6887];  %%coupler full etch TE 200nm
%nodd_chg=[2.6929,2.6798];  %%coupler full etch TE 200nm
%neven_chg=[2.5457,2.5313];  %%coupler full etch TE 300nm width500nm
%nodd_chg=[2.5306,2.5145];  %%coupler full etch TE 300nm width500nm
%neven_chg=[2.5505,2.5363];  %%coupler full etch TE 200nm width500nm
%nodd_chg=[2.5233,2.5066];  %%coupler full etch TE 200nm width500nm

neven_chg=lambda*((neven_chg(2)-neven_chg(1))/(lambda1(2)-lambda1(1)))+((neven_chg(1)*lambda1(2))-(neven_chg(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
nodd_chg=lambda*((nodd_chg(2)-nodd_chg(1))/(lambda1(2)-lambda1(1)))+((nodd_chg(1)*lambda1(2))-(nodd_chg(2)*lambda1(1)))/(lambda1(2)-lambda1(1));

%1300nm_ridge air
neven_air=[2.751704,2.740207];
nodd_air=[2.728037,2.715355];
%

%neven_air=[2.751704,2.740207];
%nodd_air=[2.728037,2.715355];
%neven_air=[2.0726,2.0726];  %dvir chg wg
%nodd_air=[2.0596,2.0596];   %dvir chg wg
%neven_air=[2.6444,2.6287];  %%coupler full etch TE 200nm
%nodd_air=[2.6405,2.6244];   %%coupler full etch TE 200nm
%neven_air=[2.4415,2.4196];  %%coupler full etch TE 300nm width500nm
%nodd_air=[2.4358,2.4132];   %%coupler full etch TE 300nm width500nm
%neven_air=[2.4472,2.4259];  %%coupler full etch TE 200nm width500nm
%nodd_air=[2.4324,2.4096];   %%coupler full etch TE 200nm width500nm

%neven_air=[1.7195,1.7119];  %TM full etch
%nodd_air=[1.6746,1.666];   %TM full etch

neven_air=lambda*((neven_air(2)-neven_air(1))/(lambda1(2)-lambda1(1)))+((neven_air(1)*lambda1(2))-(neven_air(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
nodd_air=lambda*((nodd_air(2)-nodd_air(1))/(lambda1(2)-lambda1(1)))+((nodd_air(1)*lambda1(2))-(nodd_air(2)*lambda1(1)))/(lambda1(2)-lambda1(1));

%
%Lc chalco+sio2 300nm A1Se9
%Lc=[2.89779e-5,2.8130410e-5]; 
%Lcb=[3.253475e-5,3.138580e-5]; %no chalco
%Lc=[28e-6,28e-6];
%

%
%Lc=lambda*((Lc(2)-Lc(1))/(lambda1(2)-lambda1(1)))+((Lc(1)*lambda1(2))-(Lc(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
%Lcb=lambda*((Lcb(2)-Lcb(1))/(lambda1(2)-lambda1(1)))+((Lcb(1)*lambda1(2))-(Lcb(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
%

%n=ones(1,N)*n10;
%nb=ones(1,N)*n20;

%Ei=[1;0];
Eo=zeros(2,N);

%[p0 i0]=min(abs(lambda-1.55e-6));

%[r,t]=bragg(N,n,lambda_i(1),lambda_i(2),284.925e-9,1000);

for i=1:N
    
    Lc=lambda(i)/(2*(neven_chg(i)-nodd_chg(i)));
    Lcb=lambda(i)/(2*(neven_air(i)-nodd_air(i)));
    
    Lc=Lcb;                                 %no ChG on couplers
    
                                                                   
       %Lmzi=0.5*(Lc);                    %max Ex mzi;                                             
    
    %ph_mzi=0*pi;
    
    E1=coupler(Lc,Lmzi-Lbmzi,Ei(:,i));                                              %basic coupler
    E2=coupler(Lcb,Lbmzi,E1);                                                  %burn coupler
    
    E3=delay(lambda(i),n(i),l-lbmzi,ph_mzi,E2,1*alpha+alpha_ChG,0,1);                            %basic delay
    E4=delay(lambda(i),nb(i),lbmzi,0,E3,alpha,0,1);                                    %burn delay
 
    E6=coupler(Lc,Lmzi,E4);                                                    %basic coupler
    
    Eo(:,i)=(abs(E6)).^2;
%     Eo(:,i)=(abs(E5)).^2;       %ring drop
    Eoutt(:,i)=E6;
end

Eout=Eoutt(ind,:);
Tdb=0.5*mag2db(Eo(ind,:));
if plot_i==1
    

    cind=de2bi(ind,3);

    plot(lambda*1e9,Tdb,'LineWidth',2);       %main plot
    axis([lambda_i(1)*1e9 lambda_i(2)*1e9 -40 5]);

    ylabel('transmission[dB]','fontsize',35);
    xlabel('\lambda[nm]','fontsize',35);
    grid on
    set(gca,'fontsize',20);
end
end