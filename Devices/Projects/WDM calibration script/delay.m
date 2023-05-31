function[Eo]=delay(lambda,n,dL,phi,Ei,alpha,s,delay)

%alpha=140;
%alpha=0;
%alpha=(4.34e2)*alpha;

alpha=1e2*(1/4.343)*alpha;

k=(2*pi/lambda)*n;

gamma=exp(-alpha*dL/2);

if s==0
    C=[gamma*(exp(1i*phi)*exp(1i*k*dL)),0;0,1];
else
    z=sym('z');
    C=[gamma*(exp(1i*phi)*z^-delay),0;0,1];
end

if dL==0
    C=[1,0;0,1];
end

Eo=C*Ei;

end