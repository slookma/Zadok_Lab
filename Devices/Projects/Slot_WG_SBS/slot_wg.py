# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:42:43 2024

@author: slookma

Note: All lengths/widths written here are in MICRONS, otherwise specified
"""

import nazca as nd

# Example usage
# gap_width = 0.06
# slab_width = 0.1          # Width of the slab
taper_start_width = 0.7     # Width of the starting taper region
taper_length = 70           # Length of the taper region
small_taper_length = 30     # small taper length
layer_number = 101          # Example layer number
layer_clad = 201            # Example clad layer number
length = 4400 - 2*(taper_length+small_taper_length)
clad_width = 4.7
gaps = [0.03,0.03,0.04,0.04,0.05,0.05,0.06,0.06,0.1,0.1,0.1,0.1]
widths = [0.1,0.15]
SOI = 400                   # SOI device layer thickness in nm 
space = 250                 # spacing between the WGs in Y axis

f = nd.Font('cousine')

# calling the GC
GC = nd.load_gds("GCs.gds", cellname="gratings")
GC2 = nd.load_gds("‏‏GCs2.gds", cellname="gratings")
GC3 = nd.load_gds("GCs3.gds", cellname="gratings")
# GC4 = nd.load_gds("‏‏GCs4.gds", cellname="gratings")
MS = nd.load_gds("my_logo.gds", cellname="logo5.PNG")
Ring = nd.load_gds("Ring.gds", cellname="resonator")

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

for i in range(len(gaps)):
    # creating the slot
    create_slot_waveguide_with_tapers(gaps[i], widths[0], taper_start_width, taper_length, small_taper_length, layer_number, length).put(0,i*space)
    nd.strt(length=2*small_taper_length+2*taper_length+length,width=clad_width,layer=layer_clad).put()
    f.text('Slot Gap = '+str(int(gaps[i]*1000))+' nm, width = '+str(int(widths[0]*1000)),layer=layer_number).put(100,50+i*space)
    nd.strt(length=1000,width=100,layer=layer_clad).put(90,i*space + 80)
    f.text(str(i+1),layer=layer_number).put(-250,i*space)         # numbering
    f.text(str(i+1),layer=layer_number).put(2*small_taper_length+2*taper_length+length+220,i*space)         # numbering
    if i+1 >= 10:
        nd.strt(length=100,width=80,layer=layer_clad).put(-270,25+i*space)
        nd.strt(length=100,width=80,layer=layer_clad).put(2*small_taper_length+2*taper_length+length+200,25+i*space)
    else:
        nd.strt(length=80,width=80,layer=layer_clad).put(-270,25+i*space)
        nd.strt(length=80,width=80,layer=layer_clad).put(2*small_taper_length+2*taper_length+length+200,25+i*space)

        
for j in range(len(gaps)):
    # creating the slot
    create_slot_waveguide_with_tapers(gaps[j], widths[1], taper_start_width, taper_length, small_taper_length, layer_number, length).put(0,(i+j+2)*space)
    nd.strt(length=2*small_taper_length+2*taper_length+length,width=clad_width,layer=layer_clad).put()
    f.text('Slot Gap = '+str(int(gaps[j]*1000))+' nm, width = '+str(int(widths[1]*1000)),layer=layer_number).put(100,50+(i+j+2)*space)
    nd.strt(length=1000,width=100,layer=layer_clad).put(90,(i+j+2)*space + 80)
    f.text(str(i+j+2),layer=layer_number).put(-250,(i+j+2)*space)         # numbering
    f.text(str(i+j+2),layer=layer_number).put(2*small_taper_length+2*taper_length+length+220,(i+j+2)*space)         # numbering
    if i+j+1 >= 10:
        nd.strt(length=100,width=80,layer=layer_clad).put(-270,25+(i+j+2)*space)
        nd.strt(length=100,width=80,layer=layer_clad).put(2*small_taper_length+2*taper_length+length+200,25+(i+j+2)*space)
    else:
        nd.strt(length=80,width=80,layer=layer_clad).put(-270,25+(i+j+2)*space)
        nd.strt(length=80,width=80,layer=layer_clad).put(2*small_taper_length+2*taper_length+length+200,25+(i+j+2)*space)
    
        
        
MS.put(750+length/2,len(gaps)*space) 
nd.strt(length=250,width=100,layer=layer_clad).put(630+length/2,len(gaps)*space+25)
f.text('SOI = '+str(SOI)+' nm',layer=layer_number).put(length/2,len(gaps)*space)
nd.strt(length=420,width=100,layer=layer_clad).put(length/2 -10,len(gaps)*space+25)

for i in range(int(0.5*(len(gaps)))-1):
    GC.put(0,i*2*space)
    GC2.put(2*small_taper_length+2*taper_length+length,i*2*space,flop=True)

GC3.put(0,(i+1)*2*space) # to put the sweep gc on the last one
GC3.put(2*small_taper_length+2*taper_length+length,(i+1)*2*space,flop=True)
        

for i in range(int(0.5*(len(gaps)-1))):
    GC.put(0,space*(len(gaps)+1+2*i))
    GC2.put(2*small_taper_length+2*taper_length+length,space*(len(gaps)+1+2*i),flop=True)
GC3.put(0,space*(len(gaps)+1+2*(i+1))) # to put the sweep gc on the last one
GC3.put(2*small_taper_length+2*taper_length+length,space*(len(gaps)+1+2*(i+1)),flop=True)

Ring.put(0,(len(gaps)*len(widths)+1)*space)

# Create GDS file
nd.export_gds(filename="slot_wg.gds")

 


