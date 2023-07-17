close all
clear all
clc
warning('off','all')

% this code is based on this paper: doi: 10.1109/LPT.2016.2556713.
filepath = 'Lend_19_um_06072023\cp\';

% parameters
W_start = 1530;                                     % starting wavelength
W_end = 1570;                                       % ending wavelength
deltaL = 170e-6;                                    % path imbalance of MZI
alphaLin = 0.23*1400;                               % standard loss in our waveguides 14[dB/cm]
theta = 0:pi/10000:pi/2;                            % rad axis

% the following term is considering identical couplers
ER_fit = ((exp(-alphaLin*deltaL)+tan(theta).^2)./(exp(-alphaLin*deltaL)-tan(theta).^2)).^2; % eq. 4 from paper

if filepath(length(filepath)-1) == 'p'
    flag = 16;
else
    flag = 12;
end

figure(1)
hold on
if flag == 16
    sgtitle('Coupling Coefficient vs \lambda - CP');
else
    sgtitle('Coupling Coefficient vs \lambda - Ref');
end
for i = 1:15
    %% this part is to call the text files and read them
    filename = [num2str(i) '.txt'];
    A = readtable([filepath,filename]);
    Wavelength = A.XAxis_Wavelength_nm_;
    Loss = A.InsertionLoss_dB_;

    %%
    Loss_norm = Loss - max(Loss);                                   % normalize
    span  = Wavelength > W_start & Wavelength < W_end;              % establishing region of interest (ROI)
    Loss_norm = Loss_norm(span);                                    % taking ROI for both vectors
    Wavelength = Wavelength(span);

    %%
    % this part is in order to find the best fit kappa by finding max ER
    Wavelength_q = Wavelength(1:3:end);
    Loss_norm_q = Loss_norm(1:3:end);
    vq = interp1(Wavelength_q,Loss_norm_q,Wavelength,'pchip'); %'cubic'
    [Mpeak,Lpeak,W,ER] = findpeaks(-Loss_norm,Wavelength,'MinPeakDistance',2);  % [value of peak,location of peaks,width,ER vector]
    len = length(Lpeak);
    % [mER,LER] = max(ER);                                                        % finds max ER and the index of it
    % % FSR1 = diff(Lpeak);                                                         % vector of FSR dispesrion
    subplot(3,5,i)
    for j = 1:length(ER)
        if j == length(Lpeak)
            FSR = abs(Lpeak(j)-Lpeak(j-1)); % if it's the last one, diff to the previous
        else
            FSR = abs(Lpeak(j)-Lpeak(j+1)); % otherwise, diff from the next
        end

        logical_span = Wavelength>Lpeak(j)-0.5*FSR & Wavelength<Lpeak(j)+0.5*FSR;     % this part create the single ER region
        peak_span = Wavelength(logical_span);
        peak_mag = Loss_norm(logical_span);
        % plot(peak_span,peak_mag) % see the peak itself
        ER_Lin = db2pow(ER(j));                               % move from dB to linear
        ER_sort = abs(ER_fit - ER_Lin);

        % the following regards the mixup of not knowing if k=0.1 or k=0.9
        if i<=flag 
            [ER_fittest, ER_fittest_index] = sort(ER_sort(1:ceil(length(ER_sort)/2)));
        else
            [ER_fittest, ER_fittest_index] = sort(ER_sort(ceil(length(ER_sort)/2):end));
            ER_fittest_index = ER_fittest_index + ceil(length(ER_sort)/2);
        end

        ER_fittest_index_tot(i,j) = ER_fittest_index(1);
        Theta = theta(ER_fittest_index(1));

        kappa1(i,j) = (1-cos(Theta)^2);                         % full matrix of all kappas
        ER_fittest_tot(i,j) = ER_fit(ER_fittest_index(1));

        
        %     plot(Wavelength, Loss_norm)

        
    end
    kappa = nonzeros(kappa1(i,:));
    
    % this part is in order to interpolate kappa 
    Lpeak_q = linspace(Lpeak(1),Lpeak(end),100);    % the # of pts I want
    viq = interp1(Lpeak,kappa,Lpeak_q,'spline');    % creating it - smoothe kappa
    kappa_new(i,:) = viq;                           % saving alll new kappas
    wavelength_new(i,:) = Lpeak_q;                  % saving all lambdas
    if flag == 16
        plot(Lpeak_q.',viq,'b','LineWidth',2)%kappa
        legend('CP');
    else
        plot(Lpeak_q.',viq,'r','LineWidth',2)%kappa
        legend('Ref');
    end
    ylim([0 1])
    xlim([1538 1562])
    grid on
    xlabel('\lambda [nm]')
    ylabel('Loss [dB]')
    title({['\DeltaW = ' num2str(-70+(i-1)*10) ' nm ']});
    
end

widths = linspace(-70,70,15);
delta_lambda = wavelength_new(1,2)-wavelength_new(1,1);

figure(2)
hold on
grid on
if flag == 16
    title('Coupling Coefficient Color Map - CP');
else
    title('Coupling Coefficient Color Map - Ref');
end
imagesc(kappa_new)
caxis([0 1]);
colorbar
ylabel('\DeltaW [nm]');
xlabel('Wavelength [\mum]');
yticks(1:15);
yticklabels(widths.');
xticks(0:10:99);
xticklabels(1e-3*(wavelength_new(1,1):delta_lambda*10:wavelength_new(1,end)));
xlim([20 80])    % just to remove the edges
ylim([1 15])
hold off

