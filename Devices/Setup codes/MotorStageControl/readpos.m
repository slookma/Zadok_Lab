function [Q] = readpos(s) %
%n=micron2ustep(len); 
%x=['1pr',int2str(n)];

fprintf(s,'1tp?');
pause(0.1)
fscanf(s);
pause(0.1)
T=ans;
Q=str2num(T(5:end));

end