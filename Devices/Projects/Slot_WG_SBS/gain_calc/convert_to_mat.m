function Power = convert_to_mat(Xin, Yin, Zin, Pin)

% figure
% scatter3(Xin, Yin, Zin, [], abs(Pin), 'filled')
% view(2)

Xin = Xin(logical(Zin > max(Zin)-0.01) & logical(Zin < max(Zin)+0.01));  %3D to 2D
Yin = Yin(logical(Zin > max(Zin)-0.01) & logical(Zin < max(Zin)+0.01));  %3D to 2D
Pin = Pin(logical(Zin > max(Zin)-0.01) & logical(Zin < max(Zin)+0.01));  %3D to 2D

rclad = 5e3/2;
ep = 1;
x = -rclad:ep:rclad;
[X, Y] = meshgrid(x);

Power = griddata(Xin,Yin,Pin,X,Y, 'cubic');
Power(isnan(Power)) = 0;

% figure
% surf(X,Y,abs(Power), 'EdgeColor', 'none')
% view(2)

end