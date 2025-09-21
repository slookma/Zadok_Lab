function [t,probe,t_sect,probe_sect] = read_scope_data(path,Norm,bound,CH)
%read_scope_data Summary of this function goes here
%   Detailed explanation goes here


Data = readtable(path);
t = Data.Var1(3:end);
if CH == 2
    probe = Data.Var3(3:end);
elseif CH == 3
    probe = Data.Var2(3:end);
end

if Norm
    % probe = probe/(max(probe) - min(probe));
    probe = probe-mean(probe);
end

[~, locs_top] = findpeaks(probe,"MinPeakProminence",0.5*(max(probe) - min(probe)));
[~, locs_bot] = findpeaks(-probe,"MinPeakProminence",0.5*(max(probe) - min(probe)));

% Choose section of graph
if bound == 1
    sect_start = min(locs_top(t(locs_top)>0));
    sect_stop  = find(t > t(sect_start) + 1.5*1e-6, 1);
elseif bound == 2
    sect_start = min(locs_bot(t(locs_bot)>0));
    sect_stop  = find(t > t(sect_start) + 1.5*1e-6, 1);
else
    sect_start = 1;
    sect_stop  = length(t);
end

t_sect   = t(sect_start:sect_stop);
probe_sect = probe(sect_start:sect_stop);

if Norm
    % probe_sect = probe_sect/(max(probe_sect) - min(probe_sect));
    probe_sect = probe_sect-probe_sect(end);
end


end