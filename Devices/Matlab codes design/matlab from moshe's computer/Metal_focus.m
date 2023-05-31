cd('\\madrid.eng.biu.ac.il\e2012\katzmam\My Documents\PhD\Matlab_files');

%clearvars;

Font='Stencil';

P=1.4;
DC=35;
W=P*DC/100;

[x,yu,yl,xg,yg,str]=grating_m(P,-30,0);

%U=cleWire(2,'f',[x,yu]);
%U=cleConvert(U);
%U=cleMerge(U,U);

%L=cleWire(2,'f',[x,yl]);
%L=cleConvert(L);
%L=cleMerge(L,L);

for i=1:length(xg(1,:))
    G=cleWire(W,'f',[xg(:,i),yg(:,i)]);
    cleDraw(G);
end

%G=cleConvert(G);
%G=cleMerge(G,G);

%cleDraw(U);
%cleDraw(L);

str=[str,sprintf(' dc='),num2str(DC)];

TEXT=gphPolygonPrintf(x(1,:)+30,max(yg(1,:))+50,Font,9,'c',str);
cleDraw(TEXT);

setlayer('#95');
cleB=cleBox(0,0,63.5,63.5);
cleDraw(cleB);