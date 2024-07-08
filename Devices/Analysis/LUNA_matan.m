clear all
close all

% filepath = "\\madrid.eng.biu.ac.il\e2016\slookma\Desktop\cp_tlv\3\";
filename = ["cp_1_through" "cp_2_through" "cp_3_through" "cp_4_cross14" "cp_4_cross32" ... 
    "cp_4_through" "cp_4_through34" "cp_5_through" "cp_6_through" ...
    "cp_7_through" "cp_10_cross" "cp_10_through"];
ext = ".txt";

figure
hold on
plotbrowser('on')

for i=1:length(filename)
%     T = readtable(strcat(filepath,filename(i),ext));  
    T = readtable(strcat(filename(i),ext));
    Wavelength = T.(1);
    Wavelength = Wavelength(10:1:length(Wavelength)-10);
    Loss = T.(3) ;
    Loss = Loss(10:1:length(Loss)-10);
    filename_str = filename(i);
    plot(Wavelength,Loss-max(Loss),'DisplayName',filename_str)
end

% xlim([1540 1560])
hold off