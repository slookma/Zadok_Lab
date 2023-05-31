# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import gdspy
import numpy as np
import uuid

ld_NWG = {"layer": 174, "datatype": 0}
ld_Silox = {"layer": 9, "datatype": 0}
ld_taperMark = {"layer": 118, "datatype": 120}
ld_GC = {"layer": 118, "datatype": 121}
ld_SUS = {"layer": 195, "datatype": 0}
ld_VG1 = {"layer": 192, "datatype": 0}
ld_TNR = {"layer": 26, "datatype": 0}
ld_VIA1 = {"layer": 17, "datatype": 0}
ld_VIA2 = {"layer": 27, "datatype": 0}
ld_METAL2 = {"layer": 18, "datatype": 0}
ld_METAL3 = {"layer": 28, "datatype": 0}

ld_dataExtend = {"layer": 118, "datatype": 134}

chip_length = 5000 #microns
Chip_Height = 5000 #microns
Spacing_length_at_start = 200
Spacing_Height_at_start = 200
Taper_length = 200
Taper_Width = 0.15
SUS_spacing=0
SUS_width=70
VG_spacing=-4.5
VG_width=78
chip_X0, chip_Y0= -chip_length/2,-Chip_Height/2

my_length = chip_length - Spacing_length_at_start - Taper_length
my_height = Chip_Height - Spacing_Height_at_start

Width_WG = np.array([1,0.7])
gap = np.array([0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6])

Spacing_Ring_Waveguide = 20
height_in_S = 10
Rad = np.array([50,100])
Spacing_between_Straight = 30

ringHeaterWidth=3
ringHeaterSpacing=3

## Vias size
via1Size=0.26
via1Spacing=0.26
via2Size=0.5
via2Spacing=0.5
# Metal
metal1Width=10
metalLineWidth=10
padSize=100
padSpacing=150
MetalLineOffset=40








lib = gdspy.GdsLibrary()

top_cell =lib.new_cell('TOP')



def sbendPath(wgsbend,L=100,H=50,info = ld_NWG):
# the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
# the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        y = H/2 * (1- np.cos(t*np.pi))
        x =L*t
        
        return (x,y)
    
    def dtsbend(t):
        dy_dt = H/2*np.pi*np.sin(t*np.pi)
        dx_dt = L

        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend   
 

def sbendPathM(wgsbend,L=100,H=50,info = ld_NWG):
# the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
# the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        y = H/2 * (np.cos(t*np.pi))
        x =L*t
        
        return (x,y)
    
    def dtsbend(t):
        dy_dt =  -H/2*np.pi*np.sin(t*np.pi)
        dx_dt = L

        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend ,dtsbend , number_of_evaluations=100,**info)  
    return wgsbend    
    



def a2r(ang):  # angle to radian
    return np.pi/180*ang




def Via (x_i = 0,y_i = 0,info = ld_VIA1 ,info_M = ld_METAL2, l_via = 0.26,dis_from_edge = 0.15,Col = 40,Row = 20,MN = 2):
    
    dis_bet_via = l_via
    F_length =  dis_from_edge*2 + l_via*Col + dis_bet_via*(Col -1)
    F_height = dis_from_edge*2 + l_via*Row + dis_bet_via*(Row - 1)
    
    if (MN == 2):
        rectM = gdspy.Rectangle((x_i - F_length/2, y_i), (x_i + F_length/2, y_i + F_height) , **info_M)
        top_cell.add(rectM)
        
    else:
        rectM = gdspy.Rectangle((x_i - 100/2, y_i), (x_i + 100/2, y_i + 100) , **info_M)
        top_cell.add(rectM)
        
    
    x = x_i - F_length/2 + dis_from_edge
    y = y_i + F_height - dis_from_edge
    
    step = l_via + dis_bet_via
    
    def via (x = 0,y = 0, l = 0.26,info = ld_VIA1):
        rect = gdspy.Rectangle((x,y),(x+l,y-l),**ld_VIA1)
        top_cell.add(rect)
        
    
    for i in range(0,Row):
        for j in range(0,Col):
            via(x = x + step*j , y = y - step*i, l = l_via , info = info)
            
            
            
            


def MZI (my_length = 4800 ,B_length = 500, A_length = 500 , Taper_length = 200, Taper_Width = 0.15 , Width_WG = 1
         ,Hight_in_S = 5 , length_of_S = 500 , Straight_in_MZ = 500 , diff_in_path = 500, Rad = 50 ):
    
    Straight_in_Extra = diff_in_path - 4*Rad
    F_braodening = Width_WG*2 + 0.2 #0.2 is the minimum in Tower
    
    path1 = gdspy.Path(Taper_Width , (-my_length,0))
    path11 = gdspy.Path(3 , (-my_length,0))
    
    path1.segment(length = Taper_length,direction = "+x",final_width = Width_WG,**ld_NWG)
    path11.segment(length = Taper_length,direction = "+x",**ld_taperMark)
    
    path1.segment(length = B_length , direction = "+x" , final_width = F_braodening,**ld_NWG)
    
    
    x = path1.x
    y = path1.y
    
    
    path2 = gdspy.Path(Width_WG , (x,y + 0.6))
    path3 = gdspy.Path(Width_WG , (x,y - 0.6 - height_in_S/2))
    
    path2 = sbendPath(wgsbend = path2,L = length_of_S,H = height_in_S ,info = ld_NWG)
    path3 = sbendPathM(wgsbend = path3,L = length_of_S,H = height_in_S ,info = ld_NWG)
    
    
    
    
    path2.segment(length = Straight_in_MZ/2 , direction = "+x" , **ld_NWG)
    path2.arc( radius = Rad ,initial_angle = a2r(270), final_angle = a2r(360),**ld_NWG)
    path2.arc( radius = Rad ,initial_angle = a2r(180), final_angle = a2r(90),**ld_NWG)
    
    path7 = gdspy.Path(Width_WG , (path2.x,path2.y))
    path8 = gdspy.Path(Width_WG , (path2.x,path2.y))
    
    path8.arc(radius = 10, initial_angle = a2r(270),final_angle = a2r(180),final_width = 8,**ld_TNR)
    
    Via(x_i = path8.x  , y_i = path8.y + 1 , info = ld_VIA1 , info_M = ld_METAL2 , l_via = 0.26 , dis_from_edge = 0.15 , Col = 40 , Row = 20 , MN = 2)
    
    Via(x_i = path8.x  , y_i = path8.y + 1 , info = ld_VIA2 , info_M = ld_METAL3 , l_via = 0.5 , dis_from_edge = 0.5 , Col = 20 , Row = 10 , MN = 3)
    
    rect = gdspy.Rectangle((path8.x - 15 , path8.y),(path8.x + 15 , path8.y + 15),**ld_TNR)
    
    top_cell.add(rect)
    
    path7.segment(length = Straight_in_Extra , direction = "+x" , **ld_TNR)
    path7.arc(radius = 10, initial_angle = a2r(270),final_angle = a2r(360),final_width = 8,**ld_TNR)
    
    Via(x_i = path7.x , y_i = path7.y + 1 , info = ld_VIA1 , info_M = ld_METAL2 , l_via = 0.26 , dis_from_edge = 0.15 , Col = 40 , Row = 20 , MN = 2)
    Via(x_i = path7.x  , y_i = path7.y + 1 , info = ld_VIA2 , info_M = ld_METAL3 , l_via = 0.5 , dis_from_edge = 0.5 , Col = 20 , Row = 10 , MN = 3)
    
    rect = gdspy.Rectangle((path7.x - 15 , path7.y),(path7.x + 15 , path7.y + 15),**ld_TNR)
    
    top_cell.add(rect)
    
    path2.segment(length = Straight_in_Extra , direction = "+x" , **ld_NWG)
    path2.arc( radius = Rad ,initial_angle = a2r(90), final_angle = a2r(0),**ld_NWG)
    path2.arc( radius = Rad ,initial_angle = a2r(180), final_angle = a2r(270),**ld_NWG)
    path2.segment(length = Straight_in_MZ/2 , direction = "+x" , **ld_NWG)
    
    path3.segment(length = Straight_in_MZ + Straight_in_Extra +4*Rad , direction = "+x" , **ld_NWG)
    
    
    
    path6 = gdspy.Path(Width_WG , (path2.x , path2.y - height_in_S/2))
    
    path6 = sbendPathM(wgsbend = path6,L = length_of_S,H = height_in_S ,info = ld_NWG)
    path3 = sbendPath(wgsbend = path3,L = length_of_S,H = height_in_S ,info = ld_NWG)
    
    path4 = gdspy.Path(2*Width_WG + 0.2, (path3.x , path3.y + 0.6))
    path4.segment(length = A_length , direction = "+x" , final_width = Width_WG , **ld_NWG)
    
    xT = path4.x
    yT = path4.y
    
    path5 = gdspy.Path(3 , (xT,yT))
    path5.segment(length = Taper_length , direction = "+x" , **ld_taperMark)
    
    top_cell.add(path1)
    top_cell.add(path11)
    top_cell.add(path2)
    top_cell.add(path3)
    top_cell.add(path4)
    top_cell.add(path5)
    top_cell.add(path6)
    top_cell.add(path7)
    top_cell.add(path8)
    
    
    
    
    

MZI()

    
# lib.write_gds('tryMZI.gds')
gdspy.LayoutViewer(lib)








