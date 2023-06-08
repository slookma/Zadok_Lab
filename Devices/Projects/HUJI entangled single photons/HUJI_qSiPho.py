# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 18:22:29 2023

@author: slookma
"""

import nazca as nd
# import numpy
# import gdspy


WG_width = 3
Gap = 1-WG_width
WG_radius = 100
bus1 = 10
bus2 = 100
Lc = [22,22.1,22.2,22.3,22.4,22.5]
GC_gap = 127
ld = 250 #55



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

def shit(X,Y,Lc):
    # from here I'm building the block
    with nd.Cell(name='SHIT') as kak:
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
    
    return kak


for i in range(len(Lc)):
    shit(0,0,Lc[i]).put(0,i*GC_gap*6)
    nd.strt(length=300,width=WG_width,layer=ld).put(-(350+(250-GC_gap+Gap+WG_width)/2),i*GC_gap*6-2*GC_gap+50+(250-GC_gap+Gap+WG_width)/2)
    nd.bend(angle=-180,radius=GC_gap/2,width=WG_width,layer=ld).put()
    nd.strt(length=300,width=WG_width,layer=ld).put()
    f = nd.Font('cousine')
    f.text('L = '+str(Lc[i])+' um',layer=ld).put(3*WG_radius,i*GC_gap*6,90)   
    
nd.strt(length=300,width=WG_width,layer=ld).put(-(350+(250-GC_gap+Gap+WG_width)/2),-142+GC_gap*len(Lc)*6)
nd.bend(angle=-180,radius=GC_gap/2,width=WG_width,layer=ld).put()
nd.strt(length=300,width=WG_width,layer=ld).put()
f.text('Gap = '+str(GC_gap)+' um',layer=ld).put(-(250+(250-GC_gap+Gap+WG_width)/4),-GC_gap*3)   

# do another export in a different layer and file to substract
nd.export_gds(filename="coupler_sweep.gds")
























