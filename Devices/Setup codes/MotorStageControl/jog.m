function jog (s,dis,spd) %jog distance dis[um]at speed spd.
jogspd=[3.2 16 80 1500 2000 10000 48000];
%dis=dis*100; %distance in usteps.(old factor 1.2)
dis=micron2ustep(dis);
time=abs(dis)/jogspd(abs(spd));

x=['1ja',int2str(spd*sign(dis))];
fprintf(s,x)
pause(time)
fprintf(s,'1st')
pause(0.1); %0.05 %0.08
end
