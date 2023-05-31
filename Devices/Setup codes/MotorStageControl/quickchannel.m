function [CH]=quickchannel (s1,c)
t=0.15; %pause time ~0.15
switch c
    case 'x'
        
        err=1;
        F=1;
        while F==1
            pause(t)
            fprintf(s1,'1mx1'); %select piezo
            pause(t) 
            fprintf(s1,'1mx?');
            CH=fscanf(s1);
            if length(CH)~=8 %if some timeout error occurd
                disp(['Channel Switching Problem ' num2str(err)])
                err=err+1;
            else
                if str2num(CH(6))~=1
                    disp(['Wrong Channel Selected ' num2str(err)])
                    err=err+1;
                else
                    F=0;
                end
            end
        end
        
    case 'y'
        err=1;
        F=1;
        while F==1
            pause(t)
            fprintf(s1,'1mx2'); %select piezo
            pause(t) %~0.15
            fprintf(s1,'1mx?');
            CH=fscanf(s1);
            if length(CH)~=8 %if some timeout error occurd
                disp(['Channel Switching Problem ' num2str(err)])
                err=err+1;
            else
                if str2num(CH(6))~=2
                    disp(['Wrong Channel Selected ' num2str(err)])
                    err=err+1;
                else
                    F=0;
                end
            end
        end
        
    case 'z'
        err=1;
        F=1;
        while F==1
            pause(t)
            fprintf(s1,'1mx3'); %select piezo
            pause(t) %~0.15
            fprintf(s1,'1mx?');
            CH=fscanf(s1);
            if length(CH)~=8 %if some timeout error occurd
                disp(['Channel Switching Problem ' num2str(err)])
                err=err+1;
            else
                if str2num(CH(6))~=3
                    disp(['Wrong Channel Selected ' num2str(err)])
                    err=err+1;
                else
                    F=0;
                end
            end
        end
        
end



CH=str2double(CH(6));



end