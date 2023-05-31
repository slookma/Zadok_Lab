function [left,right,top] = LowerBusDraw_CP(R,coordinates,width,W,L)
% Draw the upper port of composite pulses coupler
% R - radius of curve parts
% coordinates - coordinates of position
% width - waveguide width outside of coupling region
% W - a vector with width values for coupling length sections
% L - a vector with length values for coupling length sections
% Return values of left,right and top end of the polygon 

% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
coupler = sum(L);
taper=1;
L = L-1;
lngth = [coordinates(1)-2*R coordinates(2)+2*R coupler];

    QRindDraw(width,coordinates(1),coordinates(2),R,'LU')
    next = QRindDraw(width,coordinates(1)-R,coordinates(2)+R,R,'UL');
    for i=1:length(L)
        X = lngth(1);
        if i == 1
            Taper = clePolygon([lngth(1)-0.049 lngth(1)-taper lngth(1)-taper lngth(1)-0.049; lngth(2)+width/2 lngth(2)+W(1,i)/2 lngth(2)-W(1,i)/2 lngth(2)-width/2]);
        else
            X = next_taper(1);
            Taper = clePolygon([X X-taper X-taper X; lngth(2)+W(1,i-1)/2 lngth(2)+W(1,i)/2 lngth(2)-W(1,i)/2 lngth(2)-W(1,i-1)/2]);
        end
        cleDraw(Taper)
        lngth1 = [X-taper lngth(2) L(i)];
        next_taper=busDraw(W(i),lngth1,'l');
            if i == length(L)
                X = next_taper(1);
                Taper = clePolygon([X X-taper X-taper X; lngth(2)+W(i)/2 lngth(2)+width/2 lngth(2)-width/2 lngth(2)-W(i)/2]);
                 cleDraw(Taper)
            end  
    end
    
    top = [coordinates(1)-2*R-0.5*coupler-1.2 coordinates(2)+2*R];
    QRindDraw(width,top(1)-0.5*coupler,top(2),R,'LD');
    QRindDraw(width,top(1)-R-0.5*coupler,top(2)-R,R,'DL');
    right = coordinates;
    left = [top(1)-0.5*coupler-2*R coordinates(2)];
    top = next;
%     %% upper port
% %     next1 = QRindDraw(countor,next(1)+0.22,next(2)+distance,R,'RU');
%     next1 = QRindDraw(countor,next(1)+0.18,next(2)+distance,R,'RU');
%     next2 = QRindDraw(countor,next1(1),next1(2),R,'UR');
% %     next2 = QRindDraw(countor,next1(1),next1(2)+0.19,R,'UR');
%     lngth1 = [next(1) next(2)+distance coupler];
%     for i=1:length(L)
%         next_taper=busDraw(W2(i),lngth1,'l');
%         X = lngth(1);
%         if i == 1
% %             Taper = clePolygon([lngth1(1) lngth1(1)-taper-0.12 lngth1(1)-taper-0.12 lngth1(1); lngth1(2)+width/2 lngth1(2)+W2(1,i)/2 lngth1(2)-W2(1,i)/2 lngth1(2)-width/2]);
%             Taper = clePolygon([lngth1(1)-0.02 lngth1(1)-taper lngth1(1)-taper lngth1(1)-0.015; lngth1(2)+width/2 lngth1(2)+W2(1,i)/2 lngth1(2)-W2(1,i)/2 lngth1(2)-width/2]);
% 
% %             figure
% %             plot([1 2],[1 2])
%         else
% %             figure
% %             plot([1 2],[2 1])
%             X = next_taper(1);
%             Taper = clePolygon([X X-taper X-taper X; lngth1(2)+W2(1,i-1)/2 lngth1(2)+W2(1,i)/2 lngth1(2)-W2(1,i)/2 lngth1(2)-W2(1,i-1)/2]);
%         end
%         cleDraw(Taper)
%         lngth1 = [X-taper lngth1(2) L(i)];
% %         figure
% %         plot([1 2],[1 2],'r')
%         next_taper=busDraw(W2(i),lngth1,'l');
% %         figure
% %         plot([1 2],[1 2],'g')
%         if i == length(L)
% %             figure
% %             plot([1 2],[1 2],'b')
%             X = next_taper(1);
% %             figure
% %             plot([1 2],[2 1])
%             Taper = clePolygon([X X-taper X-taper X; lngth1(2)+W2(i)/2 lngth1(2)+width/2 lngth1(2)-width/2 lngth1(2)-W2(i)/2]);
%             
%             
%             cleDraw(Taper)
% %             figure
% %             plot([1 2],[3 2])
%                 
%         end
% %         figure
% %         plot([1 2],[1 2],'w')
% %         
%     end
%     next4 = QRindDraw(countor,next_taper(1)-1,next_taper(2),R,'LU');
%     next5 = QRindDraw(countor,next4(1),next4(2),R,'UL');
%     
% 
%     top = [coordinates(1)-2*R-0.5*coupler coordinates(2)+2*R+width+distance];
%     right(2,:) =next2;
%     left(2,:) =next5;

 end
% % 
