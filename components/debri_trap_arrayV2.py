# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 16:01:10 2018
@author: francisco
"""
from microfluidics_pdk.technology import *  ##added for single test
# Import the Microfluidic Technology File.
#from microfluidics_ipkiss3.technology import *
# Import IPKISS3 Packages.

from ipkiss3 import all as i3
# Import microfluidics API.
import microfluidics_ipkiss3.all as microfluidics

#from debri_trap_singleV2 import DebriTrapSingle
#from debri_trap_singlehalfLeftV2 import Obstacle_Left
#from debri_trap_singlehalfRightV2 import Obstacle_Right

class DebriTrapSingle(i3.PCell):

    #TECH = i3.get_technology()
    #layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc='Layer to drawn on')

    fluid_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                   doc="Channel template of the route")
    # Properties of trap
    obstacle_trap_radius = i3.PositiveNumberProperty(default=20., doc="width or radius of obstacle")
    gap_btw_barriers = i3.PositiveNumberProperty(default=30., doc="gap between obstacles")
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):
            layer = self.fluid_channel_template.layer

            # First create shapes
            # Break the channel that contain two obstacles into three segments
            # Obstacles need to intersect these three segments
            #  Obs 1. Segment 1:2,   Obs 2 Segment 2:3
            #define points will be helpful to make schematic
            p1 = (self.cInp.x+0.0,self.cInp.y+0.0)
            p2 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),0.0)
            p3 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),self.gap_btw_barriers+self.obstacle_trap_radius*2)
            p4 = (0.0,self.gap_btw_barriers+self.obstacle_trap_radius*2)
            p5 = (self.gap_btw_barriers+self.obstacle_trap_radius*2, 0.0)
            p6 = (self.gap_btw_barriers+self.obstacle_trap_radius*2, self.gap_btw_barriers+self.obstacle_trap_radius*2)

            sr1 = i3.Shape(points = [p1,p2,p3,p4], closed =True)
            sr2 = i3.Shape(points = [p2,p5,p6,p3], closed =True)

            #Internal holes as Circles  #to do: define position of SC2 as a function of perpendicular GAP
            sc1 = i3.ShapeCircle(center = (self.cInp.x+self.gap_btw_barriers*0.5+self.obstacle_trap_radius, self.gap_btw_barriers*0.5+self.obstacle_trap_radius), radius = (self.obstacle_trap_radius))

            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = layer, shape = sr1)
            br2 = i3.Boundary(layer = layer, shape = sr2)
            bc1 = i3.Boundary(layer = layer, shape = sc1)

            #Substruct boundaries and add to the element list
            b_sub = br1-bc1

            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)

            b_sub = br2-bc1

            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)

            return insts

        #Thach added to define one inlet and one outlet
        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            ports += i3.OpticalPort(name = "in", position = (0., self.obstacle_trap_radius+self.gap_btw_barriers), angle = 180.0)
            ports += i3.OpticalPort(name ="out", position = ((self.gap_btw_barriers*1.5+self.obstacle_trap_radius*3), self.obstacle_trap_radius+self.gap_btw_barriers), angle = 0.0)

            return ports

class Obstacle_Right(i3.PCell):
    #rigth filling with semicircle
    fluid_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                   doc="Channel template of the route")    # Properties of trap
    obstacle_trap_radius = i3.PositiveNumberProperty(default=20., doc="width or radius of obstacle")
    gap_btw_barriers = i3.PositiveNumberProperty(default=30., doc="gap between obstacles")
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):
            layer = self.fluid_channel_template.layer

            # First create shapes
            # Form a rectangle with points
            # Obstacles need to intersect the rectangle
            p1 = (self.cInp.x+0.0,self.cInp.y+0.0)
            p2 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),0.0)
            p3 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),self.gap_btw_barriers+self.obstacle_trap_radius*2)
            p4 = (0.0,self.gap_btw_barriers+self.obstacle_trap_radius*2)

            sr1 = i3.Shape(points = [p1,p2,p3,p4], closed =True)

            #Internal holes as Circles  #to do: define position of SC2 as a function of perpendicular GAP
            sc1 = i3.ShapeCircle(center = (self.cInp.x+self.gap_btw_barriers*0.5+self.obstacle_trap_radius, self.gap_btw_barriers*0.5+self.obstacle_trap_radius), radius = (self.obstacle_trap_radius))

            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = layer, shape = sr1)
            bc1 = i3.Boundary(layer = layer, shape = sc1)

            #Substruct boundaries and add to the element list
            b_sub = br1-bc1

            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)

            return insts

        #Thach added to define one inlet and one outlet
        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            ports += i3.OpticalPort(name = "in", position = (0., self.obstacle_trap_radius+self.gap_btw_barriers), angle = 180.0)
            ports += i3.OpticalPort(name ="out", position = ((self.gap_btw_barriers*1.5+self.obstacle_trap_radius*3), self.obstacle_trap_radius+self.gap_btw_barriers), angle = 0.0)

            return ports

class Obstacle_Left(i3.PCell):
    # left filling with semicircle
    fluid_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                   doc="Channel template of the route")    # Properties of trap
    obstacle_trap_radius = i3.PositiveNumberProperty(default=20., doc="width or radius of obstacle")
    gap_btw_barriers = i3.PositiveNumberProperty(default=30., doc="gap between obstacles")
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):
            layer = self.fluid_channel_template.layer
            # First create shapes
            # Form a rectangle with points
            # Obstacles need to intersect the rectangle
            p1 = (self.cInp.x+0.0,self.cInp.y+0.0)
            p2 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),0.0)
            p3 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),self.gap_btw_barriers+self.obstacle_trap_radius*2)
            p4 = (0.0,self.gap_btw_barriers+self.obstacle_trap_radius*2)

            sr1 = i3.Shape(points = [p1,p2,p3,p4], closed =True)

            #Internal holes as Circles  #to do: define position of SC2 as a function of perpendicular GAP
            sc1 = i3.ShapeCircle(center = (self.cInp.x+0.0, self.gap_btw_barriers*0.5+self.obstacle_trap_radius), radius = (self.obstacle_trap_radius))

            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = layer, shape = sr1)

            bc1 = i3.Boundary(layer = layer, shape = sc1)

            #Substruct boundaries and add to the element list
            b_sub = br1-bc1

            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)

            return insts

        #Thach added to define one inlet and one outlet
        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            ports += i3.OpticalPort(name = "in", position = (0., self.obstacle_trap_radius+self.gap_btw_barriers), angle = 180.0)
            ports += i3.OpticalPort(name ="out", position = ((self.gap_btw_barriers*1.5+self.obstacle_trap_radius*3), self.obstacle_trap_radius+self.gap_btw_barriers), angle = 0.0)

            return ports

class FillerRectangle(i3.PCell):
    #filling rectangle with nothig inside
    fluid_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                   doc="Channel template of the route")    # Properties of trap
    obstacle_trap_radius = i3.PositiveNumberProperty(default=20., doc="width or radius of obstacle")
    gap_btw_barriers = i3.PositiveNumberProperty(default=30., doc="gap between obstacles")
    rectangle_height = i3.PositiveNumberProperty(default=30., doc="rectangle_height")
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):
            layer = self.fluid_channel_template.layer

            # First create shapes
            # Form a rectangle with points
            # Obstacles need to intersect the rectangle
            height = self.rectangle_height
            p1 = (0.0,0.0)
            p2 = ((self.gap_btw_barriers+self.obstacle_trap_radius*2.0),0.0)
            p3 = ((self.gap_btw_barriers+self.obstacle_trap_radius*2.0),height)
            p4 = (0.0,height)

            sr1 = i3.Shape(points = [p1,p2,p3,p4], closed =True)

            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = layer, shape = sr1)

            s= i3.Structure(elements = br1)
            insts += i3.SRef(s)

            return insts

        #Thach added to define one inlet and one outlet
        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            ports += i3.OpticalPort(name = "in", position = (0., self.obstacle_trap_radius+self.gap_btw_barriers), angle = 180.0)
            ports += i3.OpticalPort(name ="out", position = ((self.gap_btw_barriers*1.5+self.obstacle_trap_radius*3), self.obstacle_trap_radius+self.gap_btw_barriers), angle = 0.0)

            return ports
'''
class JoinedObstacles(i3.PCell):
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template for ports")

    mysingleObstacle = i3.ChildCellProperty(doc='the single Obstacle child cell, which will be clonned many times',
                                            default=DebriTrapSingle())
    leftFillingSC = i3.ChildCellProperty(doc='left filling with semicircle',
                                            default=Obstacle_Left())
    rightFillingSC = i3.ChildCellProperty(doc='right filling with semicircle',
                                            default=Obstacle_Right())
    wholeTrapX = i3.PositiveNumberProperty(default=350.0, doc="total X distance length of traps")
    wholeTrapY = i3.PositiveNumberProperty(default=500.0, doc="total Y distance length of traps")
    trap_diameter = i3.PositiveNumberProperty(default=40.0, doc="total X distance length of traps")
    trap_gap =i3.PositiveNumberProperty(default=30.0, doc="gap between obstacles")
    cInp = i3.Coord2Property(default=0.0, doc="")

    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):
            x_inc = self.trap_gap+self.trap_diameter
            y_inc = self.trap_gap+self.trap_diameter

            cycles_x = int(self.wholeTrapX/(self.trap_gap +
                                             self.trap_diameter))
            cycles_y = int(self.wholeTrapY/(y_inc))

            insts += i3.ARef(reference=self.mysingleObstacle, origin=(0,0.0*self.cell.wholeTrapY),
                             period=(x_inc, 0),
                             n_o_periods=(cycles_x, 1),
                             #transformation=i3.Rotation((0.0, 0.0), 40.0)
                             )

            xf =self.trap_gap*0.5 + self.trap_diameter*0.5
            insts += i3.ARef(reference=self.mysingleObstacle, origin=(xf,y_inc),
                             period=(x_inc, 0),
                             n_o_periods=(cycles_x-1, 1),
                             #transformation=i3.Rotation((0.0, 0.0), 40.0)
                             )

            insts += i3.SRef(reference=self.leftFillingSC, position=(0, y_inc))
            insts += i3.SRef(reference=self.rightFillingSC, position=(cycles_x * x_inc-x_inc*0.5, y_inc))

            #transformation=i3.Rotation((0.0, 0.0), 40.0)


            print 'insts',insts


            return insts


        def _generate_ports(self, ports):
            #port1
            ports += microfluidics.FluidicPort(name='in',
                                               position = (0, self.wholeTrapY*0.5),
                                               #position = (0, 'insts_0'.size_info().north*0.5),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=180,
                                               trace_template=self.cell.channel_template
                                               )
            #port2
            ports += microfluidics.FluidicPort(name='out',
                                               position = (self.wholeTrapX,self.wholeTrapY*0.5),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=0,
                                               trace_template=self.cell.channel_template
                                               )

            return ports
'''
class DetLatDisplacement_array(i3.PCell):
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template for ports")

    mysingleObstacle = i3.ChildCellProperty(doc='the single Obstacle child cell, which will be clonned many times',
                                            default=DebriTrapSingle())
    rectangleFillerRight = i3.ChildCellProperty(doc='filler rectangle',
                                            default=FillerRectangle())
    rectangleFillerLeft = i3.ChildCellProperty(doc='filler rectangle',
                                            default=FillerRectangle())
    wholeX_array = i3.PositiveNumberProperty(default=350.0, doc="total X distance length of array, usually lenght")
    wholeY_array = i3.PositiveNumberProperty(default=500.0, doc="total Y distance length of array usually channel width")
    trap_diameter = i3.PositiveNumberProperty(default=40.0, doc="total X distance length of traps")
    trap_gap =i3.PositiveNumberProperty(default=30.0, doc="gap between obstacles")
    cInp = i3.Coord2Property(default=0.0, doc="")
    initial_right_height = i3.PositiveNumberProperty(default=40.0, doc="total X distance length of traps")
    d_l_d_angle = i3.PositiveNumberProperty(default=40.0, doc="total X distance length of traps")

    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):
            x_inc = self.trap_gap+self.trap_diameter
            y_inc = self.trap_gap+self.trap_diameter

            cycles_x = int(self.wholeX_array/(self.trap_gap +
                                             self.trap_diameter))
            cycles_y = int(self.wholeY_array/(y_inc))

            #filler right
            aaa = self.rectangleFillerRight(height=10.0)
            aaa_Layout = aaa.Layout(rectangle_height=10.0)
            #route1_layout = route1.get_default_view(i3.LayoutView)
            #aaa_Layout.set(rectangle_height=10.0)
            #tps_layout.set(cellTrapGap=self.tps_gaps[idx])
            insts += i3.SRef(reference=aaa, position=(0, 0))



            insts += i3.ARef(reference=self.mysingleObstacle, origin=(0,irh),
                             period=(0, y_inc),
                             n_o_periods=(1,2)#cycles_x, 1),
                             #transformation=i3.Rotation((0.0, 0.0), 40.0)
                             )

            #filler left
            insts += i3.SRef(reference=self.rectangleFillerLeft, position=(0, y_inc*2))

            #xf =self.trap_gap*0.5 + self.trap_diameter*0.5
            #insts += i3.ARef(reference=self.mysingleObstacle, origin=(xf,y_inc),
            #                 period=(x_inc, 0),
            #                 n_o_periods=(cycles_x-1, 1),
            #                 #transformation=i3.Rotation((0.0, 0.0), 40.0)
            #                 )

            #insts += i3.SRef(reference=self.rectangleFillerRight, position=(0, y_inc))
            #insts += i3.SRef(reference=self.rectangleFillerLeft, position=(cycles_x * x_inc-x_inc*0.5, y_inc))

            #transformation=i3.Rotation((0.0, 0.0), 40.0)


            print 'insts',insts


            return insts


        def _generate_ports(self, ports):
            #port1
            ports += microfluidics.FluidicPort(name='in',
                                               position = (0, self.wholeX_array *0.5),
                                               #position = (0, 'insts_0'.size_info().north*0.5),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=180,
                                               trace_template=self.cell.channel_template
                                               )
            #port2
            ports += microfluidics.FluidicPort(name='out',
                                               position = (self.wholeX_array,self.wholeY_array*0.5),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=0,
                                               trace_template=self.cell.channel_template
                                               )

            return ports


# Main program
if __name__ == '__main__':

    trap_radius = 10
    trap_gap = 4

    singleObstacle = DebriTrapSingle(obstacle_trap_radius= trap_radius, #taken for radius
                                   gap_btw_barriers = trap_gap,
                                    cInp = (0.0,0.0))
    singleObstacle_Layout =  singleObstacle.Layout()

    LeftFilling = Obstacle_Left(obstacle_trap_radius= trap_radius, #taken for radius
                                   gap_btw_barriers = trap_gap,
                                    cInp = (0.0,0.0))
    Obstacle_Left_Layout =  LeftFilling.Layout()

    RightFilling = Obstacle_Right(obstacle_trap_radius= trap_radius, #taken for radius
                                   gap_btw_barriers = trap_gap,
                                    cInp = (0.0,0.0))
    Obstacle_Right_Layout =  RightFilling.Layout()

    LeftFilling = FillerRectangle(obstacle_trap_radius= trap_radius, #taken for radius
                                   gap_btw_barriers = trap_gap,
                                    cInp = (0.0,0.0))
    LeftFilling_Layout =  LeftFilling.Layout()

    multipleObstacle = DetLatDisplacement_array(wholeX_array = 100,#2000,
                                       wholeY_array = 100,#2500,
                                       rectangleFillerLeft = LeftFilling,
                                    rectangleFillerRight = LeftFilling,
                                       mysingleObstacle = singleObstacle,
                                       trap_diameter = trap_radius*2,
                                       trap_gap =trap_gap
                                       )
    #transformation = i3.Rotation((0.0, 0.0), 40.0)

    multipleObstacle_Layout = multipleObstacle.Layout()
    multipleObstacle_Layout.visualize(annotate = True)
    multipleObstacle_Layout.write_gdsii("Trapi3All.gds")
