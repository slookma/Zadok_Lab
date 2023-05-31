function attenuate (s,n)
switch n
    case 'on'
        set(s,'requesttosend','on')
        pause(0.5)
    case 'off'
        set(s,'requesttosend','off')
        pause(0.5)
    otherwise
        disp ('Attenuator did not move')
end