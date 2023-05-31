function [y]=micron2ustep(x)
    y=x*100; %1ustep=10nm
    y=round(y);
end
