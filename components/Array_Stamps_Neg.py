# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 16:01:10 2018
@author: francisco
"""
# Import the Microfluidic Technology File.
from microfluidics_ipkiss3.technology import *  #remove when ruunning upper file
# Import IPKISS3 Packages.

from ipkiss3 import all as i3
# Import microfluidics API.
import microfluidics_ipkiss3.all as microfluidics

class DebriTrapSingle(i3.PCell):

    _name_prefix = "dumbell_Neg"
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template")#needed for ports
    TECH = i3.get_technology()

    class Layout(i3.LayoutView):
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc="Layer to draw on")
        cInp = i3.Coord2Property(default=(0.0, 0.0), required=True)
        square = i3.NumberProperty(default=35.0, doc="square")
        bridgeL = i3.NumberProperty(default=56.0, doc="bridge with")
        bridgeW = i3.NumberProperty(default=6.0, doc="bridge height")
        footprintX= i3.NumberProperty(default=50.0, doc="footp x")
        footprintY= i3.NumberProperty(default=50.0, doc="footp y")

        def _generate_instances(self, elems):

            # First create shapes
            # Break the channel that contain two obstacles into three segments
            # Obstacles need to intersect these three segments
            #  Obs 1. Segment 1:2,   Obs 2 Segment 2:3
            #define points will be helpful to make schematic
            #p1 = (self.cInp.x+0.0,self.cInp.y+0.0)
            p1 = (-(self.square+self.bridgeL*0.5),self.square*0.5)
            p2 = (-(self.bridgeL*0.5),self.square*0.5)
            p3 = (-(self.bridgeL*0.5),self.bridgeW*0.5)
            p4 = ((self.bridgeL*0.5),self.bridgeW*0.5)
            p5 = ((self.bridgeL*0.5),self.square*0.5)
            p6 = ((self.square+self.bridgeL*0.5),self.square*0.5)
            p7 = ((self.square+self.bridgeL*0.5),-self.square*0.5)
            p8 = ((self.bridgeL*0.5),-self.square*0.5)
            p9 = ((self.bridgeL*0.5),-self.bridgeW*0.5)
            p10 = (-(self.bridgeL*0.5),-self.bridgeW*0.5)
            p11 = (-(self.bridgeL*0.5),-self.square*0.5)
            p12 = (-(self.square+self.bridgeL*0.5),-self.square*0.5)
            p13 = (-(self.square+self.bridgeL*0.5),self.square*0.5) #same as p1, to start negative area
            p14 = (-(self.square+self.footprintX*0.5+self.bridgeL*0.5),(self.square+self.footprintY)*0.5)
            p15 = ((self.square+(self.bridgeL+self.footprintX)*0.5),(self.square+self.footprintY)*0.5)
            p16 = ((self.square+(self.bridgeL+self.footprintX)*0.5),-(self.square+self.footprintY)*0.5)
            p17 = (-(self.square+self.footprintX*0.5+self.bridgeL*0.5),-(self.square+self.footprintY)*0.5)
            p18 = (-(self.square+self.footprintX*0.5+self.bridgeL*0.5),(self.square+self.footprintY)*0.5)
            sr1 = i3.Shape(points = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p18,p17,p16,p15,p14], closed = True)

            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = self.layer, shape = sr1)
            s= i3.Structure(elements = br1)
            elems += i3.SRef(s)

            return elems

#__all__ = ["Label"]
class Label(i3.PCell):
    name = "LABEL"
    class Layout(i3.LayoutView):
        name = "LABEL"
        label = i3.StringProperty(default="label", doc="label")
        font_size = i3.PositiveNumberProperty(default=25, doc="Height of the text")
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc="Layer to draw text on")
        alignment = i3.Tuple2Property(default=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER), doc="Horizontal & vertical alignment" )

        def _generate_elements(self, elems):
            elems += i3.PolygonText(#name=self.name,
                                    layer=self.layer,
                                    text=self.label,
                                    height=self.font_size,
                                    coordinate=(0, 0),
                                    alignment=self.alignment)
            return elems

class ArrayOfStampsInv(i3.PCell):
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template for ports")

    myStamp = i3.ChildCellProperty(doc='the single Obstacle child cell, which will be clonned many times',
                                            default=DebriTrapSingle())
    myLabel = i3.ChildCellProperty(doc='label', default=Label())

    number_of_stamps_x = i3.PositiveIntProperty(default=10, doc="number of stamps x")
    number_of_stamps_y = i3.PositiveIntProperty(default=10, doc="number of stamps y")
    stamp_sizeX = i3.PositiveNumberProperty(default=50.0, doc="total X distance length of traps")
    stamp_sizeY = i3.PositiveNumberProperty(default=50.0, doc="total X distance length of traps")
    cInp = i3.Coord2Property(default=0.0, doc="")

    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):

            insts += i3.ARef(reference=self.myStamp, origin=(0.0,0.0),
                             period=(self.stamp_sizeX, self.stamp_sizeY),
                             n_o_periods=(self.number_of_stamps_x, self.number_of_stamps_y),
                             )
            #insts +=self.myLabel

            return insts





if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    square_size = 35
    bridge = 100

    singleStamp = DebriTrapSingle()
    singleStamp_Layout =  singleStamp.Layout(square=square_size, bridgeL= bridge)
    #singleObstacle_Layout.visualize(annotate = True)

    stampSize = singleStamp_Layout.size_info()
    stamp_width = stampSize.east - stampSize.west
    stamp_length = stampSize.north - stampSize.south

    stampArray = ArrayOfStampsInv(myStamp=singleStamp,
                                       stamp_sizeX=stamp_width,
                                       stamp_sizeY=stamp_length,
                                       )

    stampArray_Layout = stampArray.Layout()
    stampArray_Layout.visualize(annotate = True)
    stampArray_Layout.write_gdsii("stampArray.gds")