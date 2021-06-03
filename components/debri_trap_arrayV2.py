# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 16:01:10 2018
@author: francisco
"""

# Import the Microfluidic Technology File.
from microfluidics_ipkiss3.technology import *
# Import IPKISS3 Packages.
from ipkiss3 import all as i3
# Import microfluidics API.
import microfluidics_ipkiss3.all as microfluidics
#from debri_trap_singleV2 import DebriTrapSingle
#from debri_trap_singlehalfLeftV2 import Obstacle_Left
#from debri_trap_singlehalfRightV2 import Obstacle_Right

class DebriTrapSingle(i3.PCell):

    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc='Layer to drawn on')
    # Properties of trap
    obstacle_trap_radius = i3.PositiveNumberProperty(default=20., doc="width or radius of obstacle")
    gap_btw_barriers = i3.PositiveNumberProperty(default=30., doc="gap between obstacles")
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):
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
            br1 = i3.Boundary(layer = self.layer, shape = sr1)
            br2 = i3.Boundary(layer = self.layer, shape = sr2)
            bc1 = i3.Boundary(layer = self.layer, shape = sc1)

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

    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc='Layer to drawn on')
    # Properties of trap
    obstacle_trap_radius = i3.PositiveNumberProperty(default=20., doc="width or radius of obstacle")
    gap_btw_barriers = i3.PositiveNumberProperty(default=30., doc="gap between obstacles")
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):
            # First create shapes
            # Break the channel that contain two obstacles into three segments
            # Obstacles need to intersect these three segments
            #  Obs 1. Segment 1:2,   Obs 2 Segment 2:3
            #define points will be helpful to make schematic
            p1 = (self.cInp.x+0.0,self.cInp.y+0.0)
            p2 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),0.0)
            p3 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),self.gap_btw_barriers+self.obstacle_trap_radius*2)
            p4 = (0.0,self.gap_btw_barriers+self.obstacle_trap_radius*2)

            sr1 = i3.Shape(points = [p1,p2,p3,p4], closed =True)

            #Internal holes as Circles  #to do: define position of SC2 as a function of perpendicular GAP
            sc1 = i3.ShapeCircle(center = (self.cInp.x+self.gap_btw_barriers*0.5+self.obstacle_trap_radius, self.gap_btw_barriers*0.5+self.obstacle_trap_radius), radius = (self.obstacle_trap_radius))

            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = self.layer, shape = sr1)
            bc1 = i3.Boundary(layer = self.layer, shape = sc1)

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

    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc='Layer to drawn on')
    # Properties of trap
    obstacle_trap_radius = i3.PositiveNumberProperty(default=20., doc="width or radius of obstacle")
    gap_btw_barriers = i3.PositiveNumberProperty(default=30., doc="gap between obstacles")
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):
            # First create shapes
            # Break the channel that contain two obstacles into three segments
            # Obstacles need to intersect these three segments
            #  Obs 1. Segment 1:2,   Obs 2 Segment 2:3
            #define points will be helpful to make schematic
            p1 = (self.cInp.x+0.0,self.cInp.y+0.0)
            p2 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),0.0)
            p3 = ((self.gap_btw_barriers*0.5+self.obstacle_trap_radius),self.gap_btw_barriers+self.obstacle_trap_radius*2)
            p4 = (0.0,self.gap_btw_barriers+self.obstacle_trap_radius*2)

            sr1 = i3.Shape(points = [p1,p2,p3,p4], closed =True)

            #Internal holes as Circles  #to do: define position of SC2 as a function of perpendicular GAP
            sc1 = i3.ShapeCircle(center = (self.cInp.x+0.0, self.gap_btw_barriers*0.5+self.obstacle_trap_radius), radius = (self.obstacle_trap_radius))

            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = self.layer, shape = sr1)

            bc1 = i3.Boundary(layer = self.layer, shape = sc1)

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

class JoinedObstacles(i3.PCell):
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template for ports")

    mysingleObstacle = i3.ChildCellProperty(doc='the single Obstacle child cell, which will be clonned many times',
                                            default=DebriTrapSingle())
    leftFilling = i3.ChildCellProperty(doc='the single Obstacle child cell, which will be clonned many times',
                                            default=Obstacle_Left())
    rightFilling = i3.ChildCellProperty(doc='the single Obstacle child cell, which will be clonned many times',
                                            default=Obstacle_Right())
    wholeTrapX = i3.PositiveNumberProperty(default=350.0, doc="total X distance length of traps")
    wholeTrapY = i3.PositiveNumberProperty(default=500.0, doc="total Y distance length of traps")
    trap_diameter = i3.PositiveNumberProperty(default=40.0, doc="total X distance length of traps")
    trap_gap =i3.PositiveNumberProperty(default=30.0, doc="gap between obstacles")
    cInp = i3.Coord2Property(default=0.0, doc="")

    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):
            #x_inc = self.mysingleObstacle.gap_btw_barriers*1+self.mysingleObstacle.obstacle_trap_radius*2
            #y_inc = self.mysingleObstacle.obstacle_trap_radius*2+self.mysingleObstacle.gap_btw_barriers

            x_inc = self.trap_gap*1+self.trap_diameter
            y_inc = self.trap_diameter+self.trap_gap

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

            insts += i3.SRef(reference=self.leftFilling, position=(0, y_inc))
            insts += i3.SRef(reference=self.rightFilling, position=(cycles_x * x_inc-x_inc*0.5, y_inc))

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
# Main program
if __name__ == '__main__':

    trap_radius = 80
    trap_gap = 4

    singleObstacle = Obstacle_BooleanBoundary(obstacle_trap_radius= trap_radius, #taken for radius
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
    multipleObstacle = JoinedObstacles(wholeTrapX= 1000,#2000,
                                       wholeTrapY=1000,#2500,
                                       leftFilling = LeftFilling,
                                       rightFilling = RightFilling,
                                       mysingleObstacle=singleObstacle,
                                       trap_diameter = trap_radius*2,
                                       trap_gap =trap_gap
                                       )
    #transformation = i3.Rotation((0.0, 0.0), 40.0)

    multipleObstacle_Layout = multipleObstacle.Layout()
    multipleObstacle_Layout.visualize(annotate = True)
    multipleObstacle_Layout.write_gdsii("Trapi3All.gds")
'''