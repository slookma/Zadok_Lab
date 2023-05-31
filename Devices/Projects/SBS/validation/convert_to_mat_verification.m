function Power = convert_to_mat_verification(Xin, Yin, Zin, Pin)

% Xin = Xin(Yin > 0);  %3D to 2D
% Zin = Zin(Yin > 0);  %3D to 2D
% Pin = Pin(Yin > 0);  %3D to 2D
Xin = Xin(Yin == max(Yin));  %3D to 2D
Zin = Zin(Yin == max(Yin));  %3D to 2D
Pin = Pin(Yin == max(Yin));  %3D to 2D

rclad = 6.5e-6;
x = linspace(-rclad, rclad, 5e3);
[X, Y] = meshgrid(x);

% % % % rclad = 5e3/2;
% % % % ep = 1;
% % % % x = -rclad:ep:rclad;
% % % % [X, Y] = meshgrid(x);

Power = griddata(Xin*1e-9,Zin*1e-9,Pin,X,Y);
Power(isnan(Power)) = 0;

end