# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:42:43 2024

@author: slookma
"""

import nazca as nd

# Example usage
gap_width = 0.06*2 # do double, doeesn't work otherwise
slab_width = 0.1  # Width of the slab
taper_start_width = 0.7  # Width of the starting taper region
taper_length = 5  # Length of the taper region
small_taper_length = 1 #  small taper length
layer_number = 101  # Example layer number
layer_clad = 201
length = 4400 - 12
clad_width = 4.7
gaps = [2*0.03,2*0.04,2*0.05,2*0.06]
f = nd.Font('cousine')

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
        width_total = 2*slab_width + gap
        width_half = width_total/2
        #start taper from slab WG to slot 
        nd.taper(length=taper_length,width1=taper_start_width,width2=width_total,layer=layer_number).put(0,0) 
        # tapers splitting for slot
        nd.taper(length=small_taper_length,width1=width_half,width2=slab_width,layer=layer_number).put(taper_length,gap/4+slab_width/2) 
        nd.taper(length=small_taper_length,width1=width_half,width2=slab_width,layer=layer_number).put(taper_length,-gap/4-slab_width/2) 
        # straight slot waveguide
        nd.strt(length=length,width=slab_width,layer=layer_number).put(small_taper_length+taper_length,gap/4+slab_width/2)
        nd.strt(length=length,width=slab_width,layer=layer_number).put(small_taper_length+taper_length,-gap/4-slab_width/2)
        # tpaers for combining slot to slab WG
        nd.taper(length=small_taper_length,width1=slab_width,width2=width_half,layer=layer_number).put(small_taper_length+taper_length+length,gap/4+slab_width/2) 
        nd.taper(length=small_taper_length,width1=slab_width,width2=width_half,layer=layer_number).put(small_taper_length+taper_length+length,-gap/4-slab_width/2)
        #taper from slot to slab WG
        nd.taper(length=taper_length,width1=width_total,width2=taper_start_width,layer=layer_number).put(2+taper_length+length) 

    return slot

for i in range(len(gaps)):
    # creating the slot
    create_slot_waveguide_with_tapers(gaps[i], slab_width, taper_start_width, taper_length, small_taper_length, layer_number, length).put(0,i*500)
    nd.strt(length=2*small_taper_length+2*taper_length+length,width=clad_width,layer=layer_clad).put()
    f.text('Slot  Gap = '+str(int(gaps[i]*500))+' nm  width = '+str(int(slab_width*1000)),layer=layer_number).put(0,500*i + 50)
    nd.strt(length=1000,width=100,layer=layer_clad).put(-10,500*i + 85)
        

# Create GDS file
nd.export_gds(filename="slot_wg.gds")

 
# # calling the GC
# GC = nd.load_gds("WIFI_GC.gds", cellname="grating")
# GC.put(0,0.001)
# GC.put(2+2*taper_length+length,flop=True)


