function [left,right,top] = busPortDraw2_CP(R,coordinates,width,W,L,W2,distance,countor)
%Draw ring resonator that is radius is R and coupler length is Coupler
%and it can be located by the coupler center or right coordinate 

% addpath(genpath('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Clewin\Draw scripts'));
coupler = sum(L);
taper=1;
L = L-1;
lngth = [coordinates(1)-2*R coordinates(2)+2*R coupler];

    QRindDraw(countor,coordinates(1),coordinates(2),R,'LU')
    next = QRindDraw(countor,coordinates(1)-R,coordinates(2)+R,R,'UL');
    for i=1:length(L)
        X = lngth(1);
        if i == 1
            Taper = clePolygon([lngth(1) lngth(1)-taper lngth(1)-taper lngth(1); lngth(2)+width/2 lngth(2)+W(1,i)/2 lngth(2)-W(1,i)/2 lngth(2)-width/2]);
%             figure
%             plot([1 2],[1 2])
        else
%             figure
%             plot([1 2],[2 1])
            X = next_taper(1);
            Taper = clePolygon([X X-taper X-taper X; lngth(2)+W(1,i-1)/2 lngth(2)+W(1,i)/2 lngth(2)-W(1,i)/2 lngth(2)-W(1,i-1)/2]);
        end
        cleDraw(Taper)
        lngth1 = [X-taper lngth(2) L(i)];
%         figure
%         plot([1 2],[1 2],'r')
        next_taper=busDraw(W(i),lngth1,'l');
%         figure
%         plot([1 2],[1 2],'g')
        if i == length(L)
%             figure
%             plot([1 2],[1 2],'b')
            X = next_taper(1);
%             figure
%             plot([1 2],[2 1])
            Taper = clePolygon([X X-taper X-taper X; lngth(2)+W(i)/2 lngth(2)+width/2 lngth(2)-width/2 lngth(2)-W(i)/2]);
            
            
            cleDraw(Taper)
%             figure
%             plot([1 2],[3 2])
                
        end
%         figure
%         plot([1 2],[1 2],'w')
        
    end
    top = [coordinates(1)-2*R-0.5*coupler coordinates(2)+2*R];
    QRindDraw(countor,top(1)-0.5*coupler,top(2),R,'LD');
    QRindDraw(countor,top(1)-R-0.5*coupler,top(2)-R,R,'DL');
    right = coordinates;
    left = [top(1)-0.5*coupler-2*R coordinates(2)];
    %% upper port
    next1 = QRindDraw(countor,next(1),next(2)+distance,R,'RU');
    next2 = QRindDraw(countor,next1(1),next1(2),R,'UR');
    lngth1 = [next(1) next(2)+distance coupler];
    for i=1:length(L)
        X = lngth(1);
        if i == 1
            Taper = clePolygon([lngth1(1) lngth1(1)-taper lngth1(1)-taper lngth1(1); lngth1(2)+width/2 lngth1(2)+W2(1,i)/2 lngth1(2)-W2(1,i)/2 lngth1(2)-width/2]);
%             figure
%             plot([1 2],[1 2])
        else
%             figure
%             plot([1 2],[2 1])
            X = next_taper(1);
            Taper = clePolygon([X X-taper X-taper X; lngth1(2)+W2(1,i-1)/2 lngth1(2)+W2(1,i)/2 lngth1(2)-W2(1,i)/2 lngth1(2)-W2(1,i-1)/2]);
        end
        cleDraw(Taper)
        lngth1 = [X-taper lngth1(2) L(i)];
%         figure
%         plot([1 2],[1 2],'r')
        next_taper=busDraw(W2(i),lngth1,'l');
%         figure
%         plot([1 2],[1 2],'g')
        if i == length(L)
%             figure
%             plot([1 2],[1 2],'b')
            X = next_taper(1);
%             figure
%             plot([1 2],[2 1])
            Taper = clePolygon([X X-taper X-taper X; lngth1(2)+W2(i)/2 lngth1(2)+width/2 lngth1(2)-width/2 lngth1(2)-W2(i)/2]);
            
            
            cleDraw(Taper)
%             figure
%             plot([1 2],[3 2])
                
        end
%         figure
%         plot([1 2],[1 2],'w')
%         
    end
    next4 = QRindDraw(countor,next_taper(1),next_taper(2),R,'LU');
    next5 = QRindDraw(countor,next4(1),next4(2),R,'UL');
    
    
    top = [coordinates(1)-2*R-0.5*coupler coordinates(2)+2*R+width+distance];
    right(2,:) =next2;
    left(2,:) =next5;
 end
% % 