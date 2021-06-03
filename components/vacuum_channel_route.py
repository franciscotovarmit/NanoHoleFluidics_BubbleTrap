# Import the Microfluidic Technology File.

from microfluidics_ipkiss3.technology import *

# Import IPKISS3 Packages.

from ipkiss3 import all as i3

# Import microfluidics API.

import microfluidics_ipkiss3.all as microfluidics
import math
from debri_trap_arrayV2 import * #JoinedObstacles
from reservoir import Reservoir

# Define a Custom Class.
class VacuumChannelRoute(i3.PCell):

    # Properties of trap
    width = 200#i3.PositiveNumberProperty(default=200.,doc="width main channel")
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate().Layout(width=width),
                                                             doc="Channel template of the route")
    _name_prefix = "FluidVacTrapF" # a prefix added to the unique identifier
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):

        def _generate_instances(self, insts):

            p1 = (-11e3, -2e3) #route to match SolidWorks drawing
            p2 = (-6.5e3,-2e3)
            p3 = (-3.5e3, -5e3)
            p4 = (-1.5e3, -5e3)
            p5 = (0, -3.5e3)
            p6 = (0, -2e3)

            ######################routing
            in_port_1 = microfluidics.FluidicPort(position=p1, trace_template=self.cell.channel_template)
            out_port_6 = microfluidics.FluidicPort(position=p6, trace_template=self.cell.channel_template)
            in_port_1.angle_deg =  180
            out_port_6.angle_deg = 0

            from ipkiss.plugins.photonics.routing.manhattan import RouteManhattan

            channel_4 = microfluidics.RoundedChannel(trace_template=self.cell.channel_template)  # used for routing
            channel_4_layout = channel_4.Layout()
            channel_4_layout.set(bend_radius = 1500, shape = RouteManhattan(input_port=in_port_1,
                                                                             points=[p1,p2,p3,p4,p5,p6],
                                                                             output_port=out_port_6,
                                                                             bend_radius = 1.0))
            insts += i3.SRef(name = "Route_11", reference = channel_4)

            return insts

        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            ports += i3.OpticalPort(name = "in1", position = (-11e3,-2e3), angle = 180.0)
            ports += i3.OpticalPort(name ="out1", position = (0,-2e3), angle = 90.0)

            ports += i3.OpticalPort(name ="vac1", position = (-10.5e3,-2e3), angle = 90.0)
            ports += i3.OpticalPort(name ="vac2", position = (-8.5e3, -2e3), angle = 90.0)
            ports += i3.OpticalPort(name ="vac3", position = (-6.5e3,-2.1e3), angle = 90.0)
            ports += i3.OpticalPort(name ="vac4", position = (0.0e3,-3.0e3), angle = 180.0)
            ports += i3.OpticalPort(name ="vac5", position = (0e3,-2.0e3), angle = 180.0)

            print 'ports ',ports
            return ports

# Main program
if __name__ == "__main__":
    res_radius = 300.0
    obstacle_diameter = 40
    obstacle_gap = 30.0


    vac_route = VacuumChannelRoute()
    vac_route_layout = vac_route .Layout()
    vac_route_layout.visualize(annotate=True)
    vac_route_layout.visualize_2d()
    vac_route_layout.write_gdsii("vac_route_and_traps.gds")

