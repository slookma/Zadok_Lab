function [ cleDrawDat ] = cleWire(width,style,points)
%cleWire    - Draw wire.
%
%   cleDrawDat = cleWire(width,points)
%       width       - Wire width.
%       style       - Wire style.
%		      'round', 'r' 
%		      'flat',  'f'
%		      'extended', 'e'
%       points      - Nx2 array of point coordinates [x y].
%
%       cleDrawDat  - Optional output structure for further editing.
%                     If not used, data is directly writen to CleWin.

global CleWin;

if (~isnumeric(points) | size(points,2)~=2 | ~isnumeric(width) | ~isstr(style) | length(width)~=1 )
    error('CleWin:cleWire:InputError', ...
          'Incorrect input parameter(s).');
end;


if ( ~strcmp(style,'r') & ~strcmp(style,'round') &...
     ~strcmp(style,'f') & ~strcmp(style,'flat') &...
     ~strcmp(style,'e') & ~strcmp(style,'extended') )
    error('CleWin:cleWire:InputError', ...
          'Incorrect style definition.');
end;


if (size(points,2)~=2)
 points=points';
end;

if (size(points,2)~=2)
 error('CleWin:cleWire:DimensionError', ...
       'Give wire points as a Nx2 array.');
end;

%------------------------------------------------------------
cleDrawDat=cleEmpty();
cleDrawDat.cleWire{1}.width=width;
cleDrawDat.cleWire{1}.style=style;
cleDrawDat.cleWire{1}.points=points;
cleDrawDat.cleWire{1}.layer=CleWin.layer;

if nargout < 1,
 cleDraw(cleDrawDat)
end;
%------------------------------------------------------------

