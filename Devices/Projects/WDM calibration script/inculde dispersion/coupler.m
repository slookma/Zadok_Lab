function[Eo] = coupler(Lc,L,Ei)
% describes the field mutiplied by the coupler matrix.
    c = cos((pi*L)/(2*Lc));     % defenition of an argument.
    s = sin((pi*L)/(2*Lc));     % defenition of an argument.
    C = [c,-1i*s ; -1i*s,c];    % coupler transfer matrix.
    Eo = C*Ei;
end
