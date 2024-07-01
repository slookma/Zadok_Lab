# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:42:43 2024

@author: slookma

Note: All lengths/widths written here are in MICRONS, otherwise specified
"""

import nazca as nd

taper_start_width = 0.7     # Width of the starting taper region
taper_length = 100           # Length of the taper region
small_taper_length = 50     # small taper length
layer_number = 101          # Example layer number
layer_clad = 201            # Example clad layer number
length = 4400 - 2*(taper_length+small_taper_length)
clad_width = 4.7
SOI = 400                   # SOI device layer thickness in nm 
space = 250                 # spacing between the WGs in Y axis
gaps =  [0.04,  0.04,   0.04,   0.04,   0.04,   0.04,   0.04,   0.04,   0.06,   0.06,   0.1,    0.1,    0.04,   0.04,   0.1,    0.1,    0.05,   0.05,   0.1,   0.1]
L =     [0.05,  0.05,   0.07,   0.07,   0.1,    0.1,    0.1,    0.1,    0.1,    0.1,    0.1,    0.1,    0.125,  0.125,  0.125,  0.125,  0.15,   0.15,   0.15,  0.15]
R =     [0.13,  0.13,   0.13,   0.13,   0.13,   0.13,   0.1,    0.1,    0.1,    0.1,    0.1,    0.1,    0.125,  0.125,  0.125,  0.125,  0.15,   0.15,   0.15,  0.15]
f = nd.Font('cousine')

# calling the GC
GC =  nd.load_gds("GCs.gds" , cellname="gratings")
GC2 = nd.load_gds("‏‏GCs2.GDS", cellname="gratings")
MS = nd.load_gds("my_logo.gds", cellname="logo5.PNG")
Ring = nd.load_gds("Ring.gds", cellname="resonator")
MZI = nd.load_gds("400nm_SOI_MZI.gds", cellname="MZM")

def create_slot_waveguide_with_tapers(gap, slab_width, taper_start_width, taper_length, small_taper_length, layer_number, length):
    """
    Slot Waveguide.
    gap                : seperation of the slabs
    slab_width         : width of the slabs
    taper_start_width  : starting width of taper
    taper_length       : length of taper region
    small_taper_length : small taper length
    layer_number       : # of layer for the gds
    length             : length of the waveguide
    """
    with nd.Cell(name='SLOT_WG') as slot:
        # Define parameters
        width_total = 2*slab_width + 2*gap
        width_half = width_total/2
        # start taper from slab WG to slot 
        nd.taper(length=taper_length,width1=taper_start_width,width2=width_total,layer=layer_number).put(0,0) 
        # tapers splitting for slot
        nd.taper(length=small_taper_length,width1=width_half,width2=slab_width,layer=layer_number).put(taper_length,gap/2+slab_width/2) 
        nd.taper(length=small_taper_length,width1=width_half,width2=slab_width,layer=layer_number).put(taper_length,-gap/2-slab_width/2) 
        # straight slot waveguide
        nd.strt(length=length,width=slab_width,layer=layer_number).put(small_taper_length+taper_length,gap/2+slab_width/2)
        nd.strt(length=length,width=slab_width,layer=layer_number).put(small_taper_length+taper_length,-gap/2-slab_width/2)
        # tpaers for combining slot to slab WG
        nd.taper(length=small_taper_length,width1=slab_width,width2=width_half,layer=layer_number).put(small_taper_length+taper_length+length,gap/2+slab_width/2) 
        nd.taper(length=small_taper_length,width1=slab_width,width2=width_half,layer=layer_number).put(small_taper_length+taper_length+length,-gap/2-slab_width/2)
        #taper from slot to slab WG
        nd.taper(length=taper_length,width1=width_total,width2=taper_start_width,layer=layer_number).put(2*small_taper_length+taper_length+length) 

    return slot


def create_ne_slot_waveguide_with_tapers(gap, left_width, right_width, taper_start_width, taper_length, small_taper_length, layer_number, length):
    """
    Slot Waveguide.
    gap                : seperation of the slabs
    left_width         : width of the left slab
    right_width         : width of the right slab
    taper_start_width  : starting width of taper
    taper_length       : length of taper region
    small_taper_length : small taper length
    layer_number       : # of layer for the gds
    length             : length of the waveguide
    """
    with nd.Cell(name='NE_SLOT_WG') as ne_slot:
        # Define parameters
        width_total = left_width + right_width + 2*gap 
        width_half = width_total/2
        # start taper from slab WG to ne slot 
        nd.taper(length=taper_length,width1=taper_start_width,width2=width_total,layer=layer_number).put(0,0) 
        # tapers splitting for slot
        nd.taper(length=small_taper_length,width1=width_half,width2=left_width,layer=layer_number).put(taper_length , width_half/2) 
        nd.taper(length=small_taper_length,width1=width_half,width2=right_width,layer=layer_number).put(taper_length , -width_half/2) 
        # straight slot waveguide
        nd.strt(length=length,width=left_width,layer=layer_number).put(small_taper_length+taper_length,gap+left_width/2)
        nd.strt(length=length,width=right_width,layer=layer_number).put(small_taper_length+taper_length,-right_width/2)
        
        
        ############################ 
        ###   doing the bending  ###
        ############################
        
        nd.bend(angle=180,radius=rad+left_width+gap/2,width=left_width,layer=layer_number).put(small_taper_length+taper_length+length,gap+left_width/2)
        nd.bend(angle=180,radius=rad+gap/2+right_width+left_width,width=right_width,layer=layer_number).put(small_taper_length+taper_length+length,-right_width/2)

        # backward straight slot waveguide
        nd.strt(length=-(length),width=left_width,layer=layer_number).put(small_taper_length+taper_length+length,2*(rad+left_width+gap/2)+gap+left_width/2)
        nd.strt(length=-(length),width=right_width,layer=layer_number).put(small_taper_length+taper_length+length,2*(rad+gap/2+right_width+left_width)-right_width/2)
        
        # tapers
        nd.taper(length=-small_taper_length,width1=left_width,width2=width_half,layer=layer_number).put(small_taper_length+taper_length,2*(rad+left_width+gap/2)+gap+left_width/2) 
        nd.taper(length=-small_taper_length,width1=right_width,width2=width_half,layer=layer_number).put(small_taper_length+taper_length,2*(rad+gap/2+right_width+left_width)-right_width/2)

        # start taper from ne slot to slabWG
        nd.taper(length=-taper_length,width1=width_total,width2=taper_start_width,layer=layer_number).put(taper_length,2*rad+width_total+gap/4) 


        ############################
        
        # # tpaers for combining slot to slab WG
        # nd.taper(length=small_taper_length,width1=left_width,width2=width_half,layer=layer_number).put(small_taper_length+taper_length+length,gap+left_width/2) 
        # nd.taper(length=small_taper_length,width1=right_width,width2=width_half,layer=layer_number).put(small_taper_length+taper_length+length,-right_width/2)
        # #taper from slot to slab WG
        # nd.taper(length=taper_length,width1=width_total,width2=taper_start_width,layer=layer_number).put(2*small_taper_length+taper_length+length) 

    return ne_slot


def slot_WG(gap, left_width, right_width, taper_start_width, taper_length, small_taper_length, layer_number, length):
    """
    Slot Waveguide.
    gap                : seperation of the slabs
    left_width         : width of the left slab
    right_width         : width of the right slab
    taper_start_width  : starting width of taper
    taper_length       : length of taper region
    small_taper_length : small taper length
    layer_number       : # of layer for the gds
    length             : length of the waveguide
    """
    with nd.Cell(name='SLOT_WG_BEND') as bent_slot:
        ############################ 
        ###   doing the tapers   ###
        ############################
        width_total = left_width + right_width + 2*gap 
        width_half = width_total/2
        # start taper from slab WG to ne slot 
        nd.taper(length=taper_length,width1=taper_start_width,width2=width_total,layer=layer_number).put(0,0) 
        # tapers splitting for slot
        nd.taper(length=small_taper_length,width1=width_half,width2=left_width,layer=layer_number).put(taper_length , width_half/2) 
        nd.taper(length=small_taper_length,width1=width_half,width2=right_width,layer=layer_number).put(taper_length , -width_half/2) 
        # straight slot waveguide
        nd.strt(length=length/2,width=left_width,layer=layer_number).put(small_taper_length+taper_length,width_half/2)
        nd.strt(length=length/2,width=right_width,layer=layer_number).put(small_taper_length+taper_length, -width_half/2)
          
        ############################ 
        ###   doing the bending  ###
        ############################
        rad_L = 50
        rad_R = 50+gap+left_width/2+right_width/2
        nd.bend(angle= 90 , radius=rad_L , width=left_width , layer=layer_number).put(small_taper_length+taper_length+length/2,width_half/2)
        nd.bend(angle=-90 , radius=rad_R , width=left_width , layer=layer_number).put()
        nd.bend(angle= 90 , radius=rad_R , width=right_width , layer=layer_number).put(small_taper_length+taper_length+length/2,-width_half/2)
        nd.bend(angle=-90 , radius=rad_L , width=right_width , layer=layer_number).put()
        
        # straight slot waveguide
        nd.strt(length=length/2 , width=left_width , layer=layer_number).put(rad_R+rad_L+small_taper_length+taper_length+length/2 , rad_R+rad_L+width_half/2)
        nd.strt(length=length/2 , width=right_width , layer=layer_number).put(rad_R+rad_L+small_taper_length+taper_length+length/2 , rad_L+rad_R-width_half/2)

        
        ############################ 
        ###   doing the tapers   ###
        ############################
        nd.taper(length=small_taper_length , width1=left_width , width2=width_half , layer=layer_number).put(rad_R+rad_L+small_taper_length+taper_length+length , rad_R+rad_L+width_half/2)
        nd.taper(length=small_taper_length , width1=right_width , width2=width_half , layer=layer_number).put(rad_R+rad_L+small_taper_length+taper_length+length , rad_L+rad_R-width_half/2)
        # start taper from ne slot to slabWG
        nd.taper(length=taper_length , width1=width_total , width2=taper_start_width , layer=layer_number).put(rad_R+rad_L+2*small_taper_length+taper_length+length , rad_R+rad_L)
        ############################
    return bent_slot



##########################################################
##############  This is the main part  ###################
##########################################################

for i in range(len(gaps)):
    
    rad_L = 50
    rad_R = 50+gaps[i]+L[i]/2+R[i]/2
    
    # creating the slot
    slot_WG(gaps[i], L[i], R[i], taper_start_width, taper_length, small_taper_length, layer_number, length).put(0,i*space)
    nd.strt(length=small_taper_length+taper_length+length/2 , width=clad_width , layer=layer_clad).put()
    nd.bend(angle=90 , radius=50 , width=clad_width , layer=layer_clad).put()
    nd.bend(angle=-90 , radius=50+gaps[i]+L[i]/2+R[i]/2 , width=clad_width , layer=layer_clad).put()
    nd.strt(length=small_taper_length+taper_length+length/2 , width=clad_width , layer=layer_clad).put()
    # text
    if L[i]==R[i]:
            f.text('slot: g/W = '+str(int(gaps[i]*1000))+'/'+str(int(L[i]*1000))+' nm',layer=layer_number).put(100,50+i*space)
            nd.strt(length=720,width=100,layer=layer_clad).put(90,i*space + 80)
    else:
            f.text('ne slot: g/L/R = '+str(int(gaps[i]*1000))+'/'+str(int(L[i]*1000))+'/'+str(int(R[i]*1000))+' nm',layer=layer_number).put(100,50+i*space)
            nd.strt(length=970,width=100,layer=layer_clad).put(90,i*space + 80)
    
    
    # numbering
    f.text(str(i+1),layer=layer_number).put(-250,i*space)
    f.text(str(i+1),layer=layer_number).put(rad_L+rad_R+2*small_taper_length+2*taper_length+length+220,rad_L+rad_R+i*space)
    if i+1 >= 10:
        nd.strt(length=100,width=80,layer=layer_clad).put(-270,25+i*space)
        nd.strt(length=100,width=80,layer=layer_clad).put(rad_L+rad_R+2*small_taper_length+2*taper_length+length+200,rad_L+rad_R+25+i*space)
    else:
        nd.strt(length=80,width=80,layer=layer_clad).put(-270,25+i*space)
        nd.strt(length=80,width=80,layer=layer_clad).put(rad_L+rad_R+2*small_taper_length+2*taper_length+length+200,rad_L+rad_R+25+i*space)

     
for i in range(int(0.5*(len(gaps)))):
    rad_L = 50
    rad_R = 50+gaps[2*i]+L[2*i]/2+R[2*i]/2
    GC.put(0,i*2*space)
    GC2.put(rad_L+rad_R+2*small_taper_length+2*taper_length+length,rad_R+rad_L+i*2*space,flop=True)
    

# labels        
# MS.put(-500,-500) 
# nd.strt(length=250,width=100,layer=layer_clad).put(-620,-470)
# f.text('SOI = '+str(SOI)+' nm',layer=layer_number).put(-1000,-1000)
# nd.strt(length=420,width=100,layer=layer_clad).put(-1010,-975)




# Ring.put(-2000,-2000)
# MZI.put(-3000,-3000)

# Create GDS file
nd.export_gds(filename="slot_wg.gds")

 


