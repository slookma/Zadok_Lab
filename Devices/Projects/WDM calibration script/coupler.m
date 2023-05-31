function[Eo]=coupler(Lc,L,Ei)

%kapa=(sin((pi*L)/(2*Lc)))^2;

c=cos((pi*L)/(2*Lc));
s=sin((pi*L)/(2*Lc));

C=[c,-1i*s;-1i*s,c];

Eo=C*Ei;

end
