clc
clear all
close all
%% Time Domain

Index = 1:1:801;
SamplingRate = 1e6;
T = 1/(SamplingRate);
Time = Index*T;
alpha = linspace(-pi/4,pi/4,100); 
x = linspace(0,2,100);

N = 12;
TimeDomain = zeros(1,801);
filter = TimeDomain;
filter(ceil(Index(end)/2):1:ceil(Index(end)/2)+99) = cos(alpha).*exp(x);
TimeDomain(ceil(Index(end)/2):10:(ceil(Index(end)/2)+N*10)) = 1;
TimeDomain = TimeDomain.*filter;
figure
plot(Time,TimeDomain)

frequancy = fftshift(ifft(fftshift(TimeDomain)));
figure
plot(SamplingRate*Index,abs(frequancy))

%%