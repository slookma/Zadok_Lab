%% LIA/ILX GUI
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Device = 1; % LIA=0 ; ILX=1 %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if exist("p", 'var')
    clear p
end

if Device == 1
    % Connect to Prologix
    p = serialport("COM4", 115200);

    % Configure Prologix
    writeline(p, "++mode 1");
    writeline(p, "++addr 1");
    writeline(p, "++auto 1");
    writeline(p, "++eoi 1");

    % Configure FPM-8210 and read power
    writeline(p, "RAD DEC");
end

xaxis = 1:10000;
R = zeros(size(xaxis));
figure

for idx = xaxis

    if Device == 0
        fprintf(LIA, '%s\n',  'SNAP? 2,0,1');
        powerStr = fscanf(LIA);
        powerStr_split = split(powerStr, ',');
        R(idx) = double(string((powerStr_split(1))));
        
        semilogy(xaxis,R*1e6)
        % ylim([10, 200])
        % yticks(10:10:200)
        % yticklabels({'10', '20', '30', '40', '50', '60', '70', '80', '90', '100'})
        ylabel('\muV', 'FontSize', 15)
    
    elseif Device == 1
        writeline(p, "POWer?");
        R(idx) = str2double(strtrim(readline(p)));

        plot(xaxis,R)
        ylim([-40, 0])
        yticks(-40:10:0)
        yticklabels({'-40', '-30', '-20', '-10', '0'})
        ylabel('dBm', 'FontSize', 15)
        text((max([0, idx-100]) + idx)/2, -35, num2str(R(idx), '%.2f'), 'FontSize', 30, 'FontWeight', 'bold', 'HorizontalAlignment', 'center')
    end
    
    grid on
    xlim([max([0, idx-100]), idx])
    ax = gca;
    ax.YAxis.FontSize = 20;
    drawnow
    
    pause(0.1)
end


