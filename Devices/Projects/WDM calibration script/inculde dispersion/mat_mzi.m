function[Tdb,lambda,Eoutt] = mat_mzi(Ei,N,plot_i,Lmzi,Lbmzi,l,ph_mzi,lbmzi,ind,alpha,alpha_ChG)
% outputs the transmission in dB
    lambda_i=[1.28e-6,1.34e-6];
    lambda=linspace(lambda_i(1),lambda_i(2),N);
    lambda1=[1.300e-6,1.320e-6];    %1300nm

    %1300nm_ridge
%     n = [3.044,2.9551];%n10=2.899867; %chalco
%     nb = [2.9387,2.8761];%n10=2.72; %air
    n = [2.9997,2.9915];%n10=2.899867; %chalco
    nb = [2.8759,2.8634];%n10=2.72; %air
    n = lambda*((n(2)-n(1))/(lambda1(2)-lambda1(1)))+((n(1)*lambda1(2))-(n(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
    nb = lambda*((nb(2)-nb(1))/(lambda1(2)-lambda1(1)))+((nb(1)*lambda1(2))-(nb(2)*lambda1(1)))/(lambda1(2)-lambda1(1));

    %1300nm_ridge chg
    neven_chg = [2.800154,2.790908];
    nodd_chg = [2.773582,2.76308];

    neven_chg = lambda*((neven_chg(2)-neven_chg(1))/(lambda1(2)-lambda1(1)))+((neven_chg(1)*lambda1(2))-(neven_chg(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
    nodd_chg = lambda*((nodd_chg(2)-nodd_chg(1))/(lambda1(2)-lambda1(1)))+((nodd_chg(1)*lambda1(2))-(nodd_chg(2)*lambda1(1)))/(lambda1(2)-lambda1(1));

    %1300nm_ridge air
    neven_air = [2.751704,2.740207];
    nodd_air = [2.728037,2.715355];
    neven_air = lambda*((neven_air(2)-neven_air(1))/(lambda1(2)-lambda1(1)))+((neven_air(1)*lambda1(2))-(neven_air(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
    nodd_air = lambda*((nodd_air(2)-nodd_air(1))/(lambda1(2)-lambda1(1)))+((nodd_air(1)*lambda1(2))-(nodd_air(2)*lambda1(1)))/(lambda1(2)-lambda1(1));
    Eo = zeros(2,N);

    for i=1:N
        Lc=lambda(i)/(2*(neven_chg(i)-nodd_chg(i)));
        Lcb=lambda(i)/(2*(neven_air(i)-nodd_air(i)));
        Lc=Lcb;                                                                    % no ChG on couplers
        E1=coupler(Lc,Lmzi-Lbmzi,Ei(:,i));                                         % basic coupler
        E2=coupler(Lcb,Lbmzi,E1);                                                  % burn coupler
        E3=delay(lambda(i),n(i),l-lbmzi,ph_mzi,E2,1*alpha+alpha_ChG,0,1);          % basic delay
        E4=delay(lambda(i),nb(i),lbmzi,0,E3,alpha,0,1);                            % burn delay
        E6=coupler(Lc,Lmzi,E4);                                                    % basic coupler
        Eo(:,i)=(abs(E6)).^2;
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