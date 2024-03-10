# -*- coding: utf-8 -*-
"""
Created on Sat Mar 9 19:04:20 2024

@author: matan slook
"""

import nazca as nd
# this part is for the composite part
flag = 1 # if composite 1 if normal 0
taper = 1
W = [
      [0.7,0.60,0.83],
      [0.7,0.62,0.85],
      [0.7,0.64,0.87],
      [0.7,0.66,0.89],
      [0.7,0.68,0.91],
      [0.7,0.70,0.93],
      [0.7,0.72,0.95]
      ]
# W = [0.7,0.66,0.89]
L = [1,24.39,21.83]

cycles = 10

WG_width = 0.7
Gap = 1-WG_width
WG_radius = 100
bus1 = 10
bus2 = 100
Lc = [8.9,9,9.06,9.1,9.2,9.3,9.4] # Lc is 31.6 um - might be 20 um
GC_gap = 127
ld = 250 #55  layer numberr



def coupler(Width,gap,Length,Radius,positionX,positionY,busLength1,busLength2):
    """
    Directional Coupler.
    width           : width of the waveguides
    gap             : gap between the center of the waveguides
    Length          : length the waveguide travel together
    Radius         : radius of the circle of the transition regions
    position        : coupler position (feed point)
    busLength1,2    : length of the bus before/after the coupler
    """
    with nd.Cell(name='Directional Coupler') as dc:
        elm1 = nd.strt(length=busLength1,width=Width,layer=ld).put(positionX,positionY)
        nd.bend(angle=90,radius=Radius,width=Width,layer=ld).put()
        nd.strt(length=75,width=Width,layer=ld).put()
        nd.bend(angle=-90,radius=Radius,width=Width,layer=ld).put()
        nd.strt(length=Length,width=Width,layer=ld).put()
        nd.bend(angle=-90,radius=Radius,width=Width,layer=ld).put()
        elm2 = nd.strt(length=busLength2,width=Width,layer=ld).put()    
                
        positionY += 4*float(Radius)+float(Width+gap)+150
        elm3 = nd.strt(length=busLength1,width=Width,layer=ld).put(positionX,positionY)
        nd.bend(angle=-90,radius=Radius,width=Width,layer=ld).put()
        nd.strt(length=75,width=Width,layer=ld).put()
        nd.bend(angle=90,radius=Radius,width=Width,layer=ld).put()
        nd.strt(length=Length,width=Width,layer=ld).put()
        nd.bend(angle=90,radius=Radius,width=Width,layer=ld).put()
        elm4 = nd.strt(length=busLength2,width=Width,layer=ld).put()
        
        nd.Pin('a0', pin=elm1.pin['a0']).put()
        nd.Pin('b0', pin=elm2.pin['b0']).put()
        nd.Pin('a1', pin=elm3.pin['a0']).put()
        nd.Pin('b1', pin=elm4.pin['b0']).put()
        
    return dc

def normal_coupler(X,Y,Lc):
    # from here I'm building the block
    with nd.Cell(name='SHIT') as uniform_coupler:
        cp1 = coupler(WG_width,Gap,Lc,50,X,Y,bus1,bus2).put()
    
        nd.bend(angle=-90,radius=WG_radius,width=WG_width,layer=ld).put(cp1.pin['b0'])
        nd.sinebend(width=WG_width,distance=400+bus1+Lc+(250-GC_gap+Gap+WG_width)/2,offset=GC_gap-125-(250-GC_gap+Gap+WG_width)/2,layer=ld).put()
    
        nd.bend(angle=90,radius=WG_radius,width=WG_width,layer=ld).put(cp1.pin['b1'])
        nd.sinebend(width=WG_width,distance=400+bus1+Lc+(250-GC_gap+Gap+WG_width)/2,offset=-GC_gap+125+(250-GC_gap+Gap+WG_width)/2,layer=ld).put()
    
        nd.bend(angle=-90,radius=50,width=WG_width,layer=ld).put(cp1.pin['a0'])
        nd.bend(angle=90,radius=(250-GC_gap+Gap+WG_width)/2,width=WG_width,layer=ld).put()
        nd.strt(length=300,width=WG_width,layer=ld).put()
    
        nd.bend(angle=90,radius=50,width=WG_width,layer=ld).put(cp1.pin['a1'])
        nd.bend(angle=-90,radius=(250-GC_gap+Gap+WG_width)/2,width=WG_width,layer=ld).put()
        nd.strt(length=300,width=WG_width,layer=ld).put()
    
    return uniform_coupler


def compositecoupler(Width,gap,Length,Radius,positionX,positionY,busLength1,busLength2,W):
    """
    Directional Coupler.
    width           : width of the waveguides
    gap             : gap between the center of the waveguides
    Length          : length the waveguide travel together
    Radius         : radius of the circle of the transition regions
    position        : coupler position (feed point)
    busLength1,2    : length of the bus before/after the coupler
    """
    with nd.Cell(name='Composite Directional Coupler') as cp:
        elm1 = nd.strt(length=busLength1,width=Width,layer=ld).put(positionX,positionY)
        nd.bend(angle=90,radius=Radius,width=Width,layer=ld).put()
        nd.strt(length=75,width=Width,layer=ld).put()
        nd.bend(angle=-90,radius=Radius,width=Width,layer=ld).put()
        nd.strt(length=(sum(L)+L[0])*cycles+L[0],width=Width,layer=ld).put()
        nd.bend(angle=-90,radius=Radius,width=Width,layer=ld).put()
        elm2 = nd.strt(length=busLength2,width=Width,layer=ld).put()    
                
        positionY += 4*float(Radius)+float(Width+gap)+150
        elm3 = nd.strt(length=busLength1,width=Width,layer=ld).put(positionX,positionY)
        nd.bend(angle=-90,radius=Radius,width=Width,layer=ld).put()
        nd.strt(length=75,width=Width,layer=ld).put()
        nd.bend(angle=90,radius=Radius,width=Width,layer=ld).put()
        
        # this part does the variations to widths
        nd.taper(length=L[0],width1=W[0],width2=W[1],layer=ld).put()
        for j in range(cycles):
            nd.strt(length=L[1],width=W[1],layer=ld).put()
            nd.taper(length=L[0],width1=W[1],width2=W[2],layer=ld).put()
            nd.strt(length=L[2],width=W[2],layer=ld).put()
            if j == cycles-1:
                nd.taper(length=L[0],width1=W[2],width2=W[0],layer=ld).put()
            else:
                nd.taper(length=L[0],width1=W[2],width2=W[1],layer=ld).put()


        
        nd.bend(angle=90,radius=Radius,width=Width,layer=ld).put()
        elm4 = nd.strt(length=busLength2,width=Width,layer=ld).put()
        
        nd.Pin('a0', pin=elm1.pin['a0']).put()
        nd.Pin('b0', pin=elm2.pin['b0']).put()
        nd.Pin('a1', pin=elm3.pin['a0']).put()
        nd.Pin('b1', pin=elm4.pin['b0']).put()
        
    return cp

def composite(X,Y,Lc,W):
    # from here I'm building the block
    with nd.Cell(name='CP') as composite_coupler:
        cp1 = compositecoupler(WG_width,Gap,Lc,50,X,Y,bus1,bus2,W).put()
        nd.bend(angle=-90,radius=WG_radius,width=WG_width,layer=ld).put(cp1.pin['b0'])
        nd.sinebend(width=WG_width,distance=(sum(L))*cycles+L[0]+W[2]+400+bus1+Lc+(250-GC_gap+Gap+WG_width)/2,offset=GC_gap-125-(250-GC_gap+Gap+WG_width)/2,layer=ld).put()
    
        nd.bend(angle=90,radius=WG_radius,width=WG_width,layer=ld).put(cp1.pin['b1'])
        nd.sinebend(width=WG_width,distance=(sum(L))*cycles+L[0]+W[2]+400+bus1+Lc+(250-GC_gap+Gap+WG_width)/2,offset=-GC_gap+125+(250-GC_gap+Gap+WG_width)/2,layer=ld).put()
    
        nd.bend(angle=-90,radius=50,width=WG_width,layer=ld).put(cp1.pin['a0'])
        nd.bend(angle=90,radius=(250-GC_gap+Gap+WG_width)/2,width=WG_width,layer=ld).put()
        nd.strt(length=300,width=WG_width,layer=ld).put()
    
        nd.bend(angle=90,radius=50,width=WG_width,layer=ld).put(cp1.pin['a1'])
        nd.bend(angle=-90,radius=(250-GC_gap+Gap+WG_width)/2,width=WG_width,layer=ld).put()
        nd.strt(length=300,width=WG_width,layer=ld).put()

    
    return composite_coupler



for i in range(len(Lc)):
    # these are the coplers
    if flag == 1:
        composite(0,0,Lc[i],W[i]).put(0,i*GC_gap*6)
    else:
        normal_coupler(0,0,Lc[i]).put(0,i*GC_gap*6)
    
    # these are the u shape alignments
    nd.strt(length=300,width=WG_width,layer=ld).put(-(350+(250-GC_gap+Gap+WG_width)/2),i*GC_gap*6-2*GC_gap+50+(250-GC_gap+Gap+WG_width)/2)
    nd.bend(angle=-180,radius=GC_gap/2,width=WG_width,layer=ld).put()
    nd.strt(length=300,width=WG_width,layer=ld).put()
    
    # this part is for the text on the sides
    f = nd.Font('cousine')
    if flag == 1:
        f.text('W1 = '+str(W[i][1])+' um',layer=ld).put(sum(L)*cycles+bus1+4*WG_radius+Lc[i],i*GC_gap*6,90)
        f.text('W2 = '+str(W[i][2])+' um',layer=ld).put(sum(L)*cycles+bus1+5*WG_radius+Lc[i],i*GC_gap*6,90)
    else:
        f.text('L = '+str(Lc[i])+' um',layer=ld).put(bus1+3*WG_radius+Lc[i],i*GC_gap*6,90)   
        
    
    
    
    
# this part is for the text in the bottom
nd.strt(length=300,width=WG_width,layer=ld).put(-(350+(250-GC_gap+Gap+WG_width)/2),-142+GC_gap*len(Lc)*6)
nd.bend(angle=-180,radius=GC_gap/2,width=WG_width,layer=ld).put()
nd.strt(length=300,width=WG_width,layer=ld).put()
if flag == 1:
    f.text('Gap = '+str(GC_gap)+' um',layer=ld).put(-(250+(250-GC_gap+Gap+WG_width)/4),-GC_gap*3)   
    f.text('L_tot = '+str((L[1]+L[2])*cycles)+' um',layer=ld).put(-300+sum(L)*cycles+bus1+3*WG_radius+Lc[i],-GC_gap*3)
else:
    f.text('Gap = '+str(GC_gap)+' um',layer=ld).put(-(250+(250-GC_gap+Gap+WG_width)/4),-GC_gap*3)   

# do another export in a different layer and file to substract
nd.export_gds(filename="composite_coupler_sweep.gds")
