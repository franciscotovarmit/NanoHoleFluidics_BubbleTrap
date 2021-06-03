# Import the Microfluidic Technology File.
from microfluidics_ipkiss3.technology import *

# Import IPKISS3 Packages.
from ipkiss3 import all as i3
# Import microfluidics API.

import microfluidics_ipkiss3.all as microfluidics
import math
from debri_trap_singleV2 import Obstacle_BooleanBoundary
from debri_trap_singlehalfLeftV2 import Obstacle_Left
from debri_trap_singlehalfRightV2 import Obstacle_Right
from debri_trap_arrayV2 import JoinedObstacles
from reservoir import Reservoir

# Define a Custom Class.
class BubbleTrapFluid(i3.PCell):

    # Properties of trap
    width = 200#i3.PositiveNumberProperty(default=200.,doc="width main channel")
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate().Layout(width=width),
                                                             doc="Channel template of the route")
    _name_prefix = "FluidVacTrapF" # a prefix added to the unique identifier
    reservoir = i3.ChildCellProperty(doc='reservoir', default=Reservoir(res_radius = 300))
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):
            angle = 225
            reservoir_dimension = self.reservoir.size_info()
            reservoir_width = reservoir_dimension.east - reservoir_dimension.west
            reservoir_length = reservoir_dimension.north - reservoir_dimension.south

            Funnel_x =  reservoir_length*0.5 +  reservoir_width - reservoir_length
            p1 = (Funnel_x*math.cos(math.pi*(angle)/180), Funnel_x*math.sin(math.pi*(angle)/180) ) #near cylinders
            p2 = (-self.reservoir.res_radius*1.25,-self.reservoir.res_radius*1.25)
            p3 = (5.0*self.reservoir.res_radius, 0)
            p4 = (3.0*self.reservoir.res_radius, 0)
            p5 = (4.0*self.reservoir.res_radius, 0)

            import operator
            p2 = tuple(map(operator.add, p1,p2))
            p3 = tuple(map(operator.add, p2,p3))

            #Input channel - segment
            channel1 = microfluidics.Channel(trace_template = self.cell.channel_template)
            channel1_lo = channel1.Layout(shape=[(2.0*self.reservoir.res_radius, 0), (0, 0)])
            insts += i3.SRef(channel1_lo, position=(-2.0*self.reservoir.res_radius, 0), transformation=i3.Rotation((0.0, 0.0), 0.0))

            #reservoir
            insts += i3.SRef(reference=self.reservoir, position=(0.0, 0.0),
                             transformation=i3.Rotation((0.0, 0.0), angle))

            ######################routing
            in_port_1 = microfluidics.FluidicPort(position=p1, trace_template=self.cell.channel_template)
            out_port_1 = microfluidics.FluidicPort(trace_template=self.cell.channel_template)
            in_port_1.angle_deg =  angle #225
            out_port_1.angle_deg = 0

            from ipkiss3.pcell.routing import RouteToAngle
            # create the route object. From Reservoir to route
            channel_1 = microfluidics.RoundedChannel(trace_template=self.cell.channel_template)  # used for routing
            channel_1_layout = channel_1.Layout()
            channel_1_layout.set(bend_radius = self.reservoir.res_radius*0.35, shape = RouteToAngle(input_port = in_port_1,
                                                                           start_straight = 500,
                                                                           end_straight = 900,
                                                                           angle_out = 0))
            #insts += i3.SRef(name = "Route_Res_to_East", reference = channel_1)

            # create the route object. From route to east to route
            from ipkiss.plugins.photonics.routing.manhattan import RouteManhattan

            channel_4 = microfluidics.RoundedChannel(trace_template=self.cell.channel_template)  # used for routing
            channel_4_layout = channel_4.Layout()

            in_port_2 = microfluidics.FluidicPort(position=p2, trace_template=self.cell.channel_template)
            in_port_2.angle_deg =  0#angle #225

            out_port_5 = microfluidics.FluidicPort(position=p5, trace_template=self.cell.channel_template)
            out_port_5.angle_deg = 180
            channel_4_layout.set(bend_radius = self.reservoir.res_radius*0.35, shape = RouteManhattan(input_port=in_port_1,
                                                                             points=[p1,p2,p3,p4,p5],
                                                                             output_port=out_port_5,
                                                                             bend_radius = 50.0))
            insts += i3.SRef(name = "Route_11", reference = channel_4)

            return insts

        #Thach added to define one inlet and one outlet
        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            ports += i3.OpticalPort(name = "in", position = (-2.0*self.reservoir.res_radius,0.0), angle = 180.0)
            ports += i3.OpticalPort(name ="out", position = (4.0*self.reservoir.res_radius,0.0), angle = 0.0)
            return ports

# Main program
if __name__ == "__main__":
    res_radius = 300.0
    obstacle_diameter = 40
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

    trap = BubbleTrapFluid(reservoir  = res)
    trap_layout = trap.Layout()
    trap_layout.visualize(annotate=True)
    trap_layout.visualize_2d()
    trap_layout.write_gdsii("trap_fluid.gds")

