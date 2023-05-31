function mov(s,len) %Move in microns. Smallest move is 0.01um
%Speed is autometacly decided depending on len.
n=micron2ustep(len); 

x=['1pr',int2str(n)];
fprintf(s,x)

%pause(0.1+3*abs(len)/1000)  %1mm=3sec, 0.1sec minimum 


end
