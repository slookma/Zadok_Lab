# LN 15
# 12/6/2018 - Boris Desiatov - Harvard
# LN Mg doped- 300nm 
# rib 120nm
#
import os
import numpy as np
import gdspy
import math
from scipy import special

exportname = "LN15"

bendR=100
chipW=4000
chipH=6000
diceL=9000
diceW=4000
layerE=5


ringNum=10

rad_array=[50,80,80,80]
wgW_array=[0.6,0.8,1,1.5]
gap_start_array=[0.3,0.3,0.7,0.7]
gap_end_array=[0.8,0.8,1.7,1.7]
pullAng_array=[10,10,0,0]
ringW_array=wgW_array

def aligmentMarkLW(x0=0,y0=0,L=100,W=1,layer=1):
	alig = gdspy.Cell('aligMarkLW')
	sline1 = gdspy.Path(W, (x0-L*0.5, y0))
	sline1.segment(L,direction='+x', final_width=W,layer=layer) 
	sline2 = gdspy.Path(W, (x0, y0-L*0.5))
	sline2.segment(L,direction='+y', final_width=W,layer=layer) 
	rr = gdspy.Round((x0+L/4, y0+L/4), 2,layer=layer)
	alig.add([sline1,sline2,rr])
	return	alig
def a2r(ang):  # angle to radian
	return np.pi/180*ang


def ring(cell,path1,x0=0,y0=0,coupleGap=0.5,ringR=10,wgW=0.8,ringW=0.8,pullAng=60,ringUp=-1,layer = 1):
	rad=(ringR+	coupleGap+wgW/2)
	ringX=x0+2*np.cos(np.pi/2-a2r(pullAng/2))*rad
	ringY=y0+(1-2* (1-np.cos(a2r(pullAng/2)))) *(rad*ringUp)
	cell.add(gdspy.Round((ringX,ringY),radius=ringR,inner_radius=ringR-ringW,number_of_points=1080,layer=layer))
	if pullAng==0:
		path1.segment(ringR*2,direction='+x',layer=layer) 	#wg after bend
	else:
		path1.turn(rad,angle=a2r(-pullAng/2*ringUp),layer=layer,number_of_points=100)		# bend
		path1.turn(rad,angle=a2r(pullAng*ringUp),layer=layer,number_of_points=100)		# bend
		path1.turn(rad,angle=a2r(-pullAng/2*ringUp),layer=layer,number_of_points=100)		# bend


def deviceRing(cell,x0=0,y0=0,shiftOffset=3000,ringX=500,coupleGap=0.5,shiftL=100,taperW=0.8,taperL=100,bendR=100,ringR=10,wgW=0.8,ringW=0.8,pullAng=60,num='',ringUp=1,layer = 1):
	#### wg with ring
	

	path1 = gdspy.Path(taperW, (x0, y0))

	textY=15

	cell.add(gdspy.Text(num, 10, (path1.x+200,path1.y+textY), layer=layer))

	path1.segment(taperL,direction='+x', final_width=wgW,layer=layer) # taper
	if ringX<shiftOffset:
		ringPosX=ringX-path1.x
		path1.segment(ringPosX,direction='+x',layer=layer)	# wg to the right			
		ring(cell,path1,x0=path1.x,y0=path1.y,coupleGap=coupleGap,ringR=ringR,wgW=wgW,ringW=ringW,ringUp=ringUp,pullAng=pullAng,layer = layer)

	L1=shiftOffset-path1.x
	path1.segment(L1,direction='+x',layer=layer)	# wg to the right			
	path1.turn(bendR,angle=np.pi/2,layer=layer,number_of_points=100)		# bend
	path1.segment(shiftL,direction='+y',layer=layer) 	#wg after bend
	path1.turn(bendR,angle=-np.pi/2,layer=layer,number_of_points=100)		# bend
	if ringX>shiftOffset:
		ringPosX=ringX-path1.x
		path1.segment(ringPosX,direction='+x',layer=layer)	# wg to the right			
		ring(cell,path1,x0=path1.x,y0=path1.y,coupleGap=coupleGap,ringR=ringR,wgW=wgW,ringW=ringW,ringUp=ringUp,pullAng=pullAng,layer = layer)

	path1.segment(chipW-path1.x-taperL,direction='+x',layer=layer) 	# wg after bend
	path1.segment(chipW-path1.x,direction='+x', final_width=taperW,layer=layer) 	# wg after bend
	cell.add(gdspy.Text('w '+str(round(wgW,1) ) + '  r'+str(ringW)  + '  g'+str(round(coupleGap,2)) , 10,  (path1.x-300,path1.y+textY), layer=layer))

	cell.add(gdspy.Text(num, 10, (path1.x-100,path1.y+textY), layer=layer))
	cell.add(path1) 
	return	cell





## main routine
chipCell = gdspy.Cell("chip")
wgS=50
shiftL=100;
blochYShift=(wgS)*(ringNum+3)+shiftL+bendR*2
# drawRings
for k in range(len(wgW_array)):
	gap_array=np.linspace(gap_start_array[k],gap_end_array[k],ringNum)
	for i in range(ringNum):
		x0=0
		y0=i*wgS+blochYShift*k
		wgW=wgW_array[k]
		ringW=ringW_array[k]
		radius=rad_array[k]
		gap=gap_array[i]
		shiftOffset=chipW-(500+i*radius*4 + i%2*radius*2)
		ringX= shiftOffset-(bendR*1+radius*1)*(i%2*(-2)+1) + (radius*2)*((i)%2)
		ringUp=1+i%2*(-2)
		pullAng=pullAng_array[k]
		deviceRing(chipCell,x0=x0,y0=y0,shiftOffset=shiftOffset,ringX=ringX,coupleGap=gap,ringUp=ringUp,taperW=1,shiftL=shiftL,taperL=100,bendR=bendR,ringR=radius,pullAng=pullAng,wgW=wgW,ringW=ringW,num=str(i),layer = 1)


# # marks
y1=-300
y2=4000


markLW=aligmentMarkLW(L=200,W=1)
for i in range(3):
	chipCell.add(gdspy.CellReference(markLW, ((i)*2000+400,y1)))
	chipCell.add(gdspy.CellReference(markLW, ((i)*2000+400,y2)))


#chipname
chipCell.add(gdspy.Text(exportname, 80, (3300,y1) , layer=1))
chipCell.add(gdspy.Text(exportname, 80, (3300,y2) , layer=1))



## ------------------------------------------------------------------ ##
##  OUTPUT                                                            ##
## ------------------------------------------------------------------ ##

## Output the layout to a GDSII file (default to all created cells).
gdspy.write_gds(exportname+'.gds', unit=1.0e-6, precision=1.0e-9)
# faltten_cell=top_cell.flatten()
faltten_cell=chipCell.flatten()

gdspy.write_gds(exportname+'_flattened.gds', cells=[faltten_cell], unit=1.0e-6, precision=1.0e-9)
# print('Using gdspy module version ' + gdspy.__version__)


#Cell area
textarea = 'Area = %d um^2' % (chipCell.area()) 
exptime=(chipCell.area()*0.00008961209);
exptime1=(chipCell.area()*0.000256);
print(textarea + ' ZEP exposure time :'+ str(round(exptime)) +' min, HSQ exposure time:'+str(round(exptime1))+' min')


## ------------------------------------------------------------------ ##
##  VIEWER                                                            ##
## ------------------------------------------------------------------ ##

## View the layout using a GUI.  Full description of the controls can
## be found in the online help at http://gdspy.sourceforge.net/
#gdspy.LayoutViewer() 

# gdspy.LayoutViewer()


