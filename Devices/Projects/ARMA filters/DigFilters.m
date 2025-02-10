[z,p,k] = ellip(4,0.1,30,0.1);
[b,a] = zp2tf(z,p,k);


figure
zplane(z,p)
grid
title('4th-Order Elliptic Lowpass Digital Filter')

[hw,fw] = zerophase(b,a,1024,"whole");

z = roots(b);
p = roots(a);

figure
plot3(cos(fw),sin(fw),hw)
hold on
plot3(cos(fw),sin(fw),zeros(size(fw)),'--')
plot3(real(z),imag(z),zeros(size(z)),'o')
plot3(real(p),imag(p),zeros(size(p)),'x')
hold off
xlabel("Real")
ylabel("Imaginary")
view(35,40)
grid

figure
freqz(b,a,10000)