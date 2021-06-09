#from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry

from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from debri_trap_arrayV2 import * #JoinedObstacles
import math

#Trap has been updated with boolean operation, to have flat ends

class Reservoir(i3.PCell):
    """A generic cell trap class. It is defined by a boundary which are defined by points
    """
    _name_prefix = "BLOCK" # a prefix added to the unique identifier
    res_radius = i3.PositiveNumberProperty(default=292., doc="radius of reservoir")
    length_funnel = i3.PositiveNumberProperty(default=100., doc="exit funnel length")
    width_end_funnel = i3.PositiveNumberProperty(default=200., doc="width funnel length where route channels connect")
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template")
    obstacles = i3.ChildCellProperty(doc='the single Obstacle child cell, which will be clonned many times',
                                            default=JoinedObstacles())

    fluid_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                   doc="Channel template of the route")
    #TECH = i3.get_technology()
    #layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc='Layer to drawn on')


    class Layout(i3.LayoutView):
        # definition of the default values of the block PCELL
        block_length = i3.PositiveNumberProperty(default = 300.0)


        def _generate_elements(self, insts):
            layer = self.fluid_channel_template.layer
            circle = i3.ShapeCircle(center=(0.0, 0.0), radius=self.res_radius)

            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = layer, shape = circle)

            point_list = []

            point_list.append( (self.res_radius*0.0, -self.res_radius))
            point_list.insert(0,  (self.res_radius*0.0, self.res_radius))

            point_list.append( (self.res_radius+self.obstacles.trap_gap*0.5, -self.res_radius*0.6))
            point_list.insert(0, (self.res_radius+self.obstacles.trap_gap*0.5, self.res_radius*0.6))

            t = i3.Shape(point_list, closed=True)
            bo = i3.Boundary(layer = layer, shape = t)
            #Substruct boundaries and add to the element list
            b_sub = br1 | bo

            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)

            #then trap
            insts += i3.SRef(reference =self.obstacles, position=(self.res_radius, self.res_radius*0.6),
                             transformation=i3.Rotation((0.0, 0.0), -90.0))

            #exit funnel
            point_list = []
            obstacle_dimension = self.obstacles.size_info()
            obstacle_width = obstacle_dimension.north - obstacle_dimension.south

            print 'feature_width ',obstacle_width
            Funnel_x0 =self.res_radius + obstacle_width


            point_list.append((Funnel_x0-self.obstacles.trap_gap * 0.5, -self.res_radius * 0.6))
            point_list.insert(0, (Funnel_x0-self.obstacles.trap_gap * 0.5, self.res_radius * 0.6))

            point_list.append( (Funnel_x0, -self.res_radius*0.6))
            point_list.insert(0,  (Funnel_x0, self.res_radius*0.6))

            point_list.append( (Funnel_x0+self.length_funnel, -self.width_end_funnel*0.5))
            point_list.insert(0, (Funnel_x0+self.length_funnel, self.width_end_funnel*0.5))

            t = i3.Shape(point_list, closed=True)
            exit_funnel = i3.Boundary(layer = layer, shape = t)
            insts += exit_funnel

            return insts

        def _generate_ports(self, ports):

            #port1
            #the aim of next three lines is to get the end of funnel x coordinate
            obstacle_dimension = self.obstacles.size_info()
            obstacle_width = obstacle_dimension.north - obstacle_dimension.south
            Funnel_x =self.res_radius + obstacle_width + self.length_funnel

            ports += microfluidics.FluidicPort(name='in1', position = (0.0, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=180,
                                               trace_template=self.channel_template
                                               )

            ports += microfluidics.FluidicPort(name='out1', position = (Funnel_x, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=0,
                                               trace_template=self.channel_template
                                               )

            return ports


# Main program
if __name__ == "__main__":
    res_radius = 800.0
    obstacle_diameter = 90
    obstacle_gap = 30.0


    singleObstacle = Obstacle_BooleanBoundary(obstacle_trap_radius= obstacle_diameter*0.5,
                                   gap_btw_barriers = obstacle_gap,
                                    cInp = (0.0,0.0))
    singleObstacle_Layout =  singleObstacle.Layout()
    LeftFilling = Obstacle_Left(obstacle_trap_radius= obstacle_diameter*0.5,
                                   gap_btw_barriers = obstacle_gap,
                                    cInp = (0.0,0.0))
    Obstacle_Left_Layout =  LeftFilling.Layout()
    RightFilling = Obstacle_Right(obstacle_trap_radius= obstacle_diameter*0.5,
                                   gap_btw_barriers = obstacle_gap,
                                    cInp = (0.0,0.0))
    Obstacle_Right_Layout =  RightFilling.Layout()
    multipleObstacle = JoinedObstacles(wholeTrapX= res_radius*1.2,#2000,
                                       wholeTrapY=1000,#2500,
                                       leftFilling = LeftFilling,
                                       rightFilling = RightFilling,
                                       mysingleObstacle=singleObstacle,
                                       trap_diameter = obstacle_diameter,
                                       trap_gap =obstacle_gap
                                       )

    #define properties in mother object ?
    res = Reservoir(res_radius = res_radius, obstacles =multipleObstacle)
    res_layout = res.Layout()
    res_layout.visualize(annotate=True)
    res_layout.visualize_2d()
    # visualize_2d displays a top down view of the fabricated layout
    #trap_layout.cross_section(i3.Shape([(0, 25), (100, 25)]), process_flow=TECH.VFABRICATION.PROCESS_FLOW).visualize()
    #lay.cross_section(i3.Shape([(-9, 3), (9, 3)]), process_flow=vfab_flow).visualize()
    #trap_layout.write_gdsii("erik_trapI3.gds")

