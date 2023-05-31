function[Eo] = delay(lambda,n,dL,phi,Ei,alpha,s,delay)
% describes the delay accumulated, input alpha is in [dB/cm].
    alpha = 1e2*(1/4.343)*alpha; % calculate linear loss, in [1/m].
    m_lambda = [1.3e-6 1.32e-6]; 
    m_n = [2.8759 2.8634];
    m = (m_n(2)-m_n(1))/(m_lambda(2)-m_lambda(1));
    %ng = n - m*1.31e-6;
    k = (2*pi/lambda)*n;
    loss = exp(-alpha*dL/2);
    if s == 0
        C = [loss*(exp(1i*phi)*exp(1i*k*dL)),0;0,1];
    else
        z = sym('z');
        C = [loss*(exp(1i*phi)*z^-delay),0;0,1];
    end
    if dL == 0                  % if the input of length is 0, no delay.
        C = [1,0 ; 0,1];
    end
    Eo = C*Ei;
end