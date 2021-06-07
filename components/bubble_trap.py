# Import the Microfluidic Technology File.
# Thach: technology should only imported in the top level script, not in the component

# Import IPKISS3 Packages.
from ipkiss3 import all as i3
# Import microfluidics API.

import microfluidics_ipkiss3.all as microfluidics
import math
import numpy as np
from reservoir import Reservoir

# Define a Custom Class.
# Thach: Multilayer PCell
class BubbleTrap(i3.PCell):

    # Properties of trap
    fluid_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                   doc="Channel template of the route")
    vacuum_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.VACUUM_CHANNEL.DEFAULT,
                                                                   doc="Channel template of the route")
    _name_prefix = "FluidVacTrapF" # a prefix added to the unique identifier
    reservoir = i3.ChildCellProperty(doc='reservoir', default=Reservoir(res_radius = 300))
    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)   # Thach: not necessary, all components start at (0, 0)


    class Layout(i3.LayoutView):
        radius_fluid = i3.PositiveNumberProperty(default=300.,
                                                 doc="radius of the circular vacuum section collecting air")
        vacuum_channel_circular = i3.PositiveNumberProperty(default=200.,
                                                            doc="width of circular channel collecting air")
        inlet_channel_length = i3.PositiveNumberProperty(default=300., doc="length of inlet channel vac")
        membrane_thickess = i3.PositiveNumberProperty(default=10., doc="length of inlet channel vac")


        def _generate_elements(self, elems):

            layer = self.vacuum_channel_template.layer

            radius = self.radius_fluid + self.vacuum_channel_circular + self.membrane_thickess
            sr1 = i3.ShapeCircle(center=(0.0,0.0),radius=radius)
            sr2 = i3.ShapeCircle(center=(0.0,0.0),radius=radius-self.vacuum_channel_circular)

            #Rectangles to be substracted to concentric circle shape
            sc1 = i3.ShapeRectangle(center = (self.cInp.x-radius,-radius),
                                    box_size = (radius*2,radius*2+300)) #300 has to be linked to channel input width))
            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = layer, shape = sr1)
            br2 = i3.Boundary(layer=layer, shape=sr2)

            bc1 = i3.Boundary(layer = layer, shape = sc1)

            #Substruct boundaries and add to the element list
            b_sub = br1-br2           #b_sub is the main circular channel vacuum

            barrier_dim = 25
            point_list = []
            point_list.append((-barrier_dim*0.5, -barrier_dim*0.5))
            point_list.insert(0,(-barrier_dim*0.5, barrier_dim*0.5))
            point_list.append((barrier_dim*0.5, -barrier_dim*0.5))
            point_list.insert(0,(barrier_dim*0.5,barrier_dim*0.5))

            # bumps
            t = i3.Shape(point_list, closed=True)
            radius_m = self.radius_fluid + self.membrane_thickess

            angle = np.linspace(275, 540, 40)
            for i in angle:
                bump = i3.Boundary(layer=layer,
                                   shape=t,
                                   transformation=(i3.Rotation((0.0, 0.0), i)+
                                                   i3.Translation((radius_m*math.cos(math.pi*(i)/180), radius_m*math.sin(math.pi*(i)/180))))
                                   )
                #substracting bumps to circle channel
                b_sub = b_sub[0] - bump

            #substract square
            b_sub = b_sub[0] - bc1

            elems += b_sub

            return elems

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
            channel1 = microfluidics.Channel(trace_template = self.cell.fluid_channel_template)
            channel1_lo = channel1.Layout(shape=[(2.0*self.reservoir.res_radius, 0), (0, 0)])
            insts += i3.SRef(channel1_lo, position=(-2.0*self.reservoir.res_radius, 0), transformation=i3.Rotation((0.0, 0.0), 0.0))

            #reservoir
            insts += i3.SRef(reference=self.reservoir, position=(0.0, 0.0),
                             transformation=i3.Rotation((0.0, 0.0), angle))

            ######################routing
            in_port_1 = microfluidics.FluidicPort(position=p1, trace_template=self.cell.fluid_channel_template)
            out_port_1 = microfluidics.FluidicPort(trace_template=self.cell.fluid_channel_template)
            in_port_1.angle_deg =  angle #225
            out_port_1.angle_deg = 0

            from ipkiss3.pcell.routing import RouteToAngle
            # create the route object. From Reservoir to route
            channel_1 = microfluidics.RoundedChannel(trace_template=self.cell.fluid_channel_template)  # used for routing
            channel_1_layout = channel_1.Layout()
            channel_1_layout.set(bend_radius = self.reservoir.res_radius*0.35, shape = RouteToAngle(input_port = in_port_1,
                                                                           start_straight = 500,
                                                                           end_straight = 900,
                                                                           angle_out = 0))
            #insts += i3.SRef(name = "Route_Res_to_East", reference = channel_1)

            # create the route object. From route to east to route
            from ipkiss.plugins.photonics.routing.manhattan import RouteManhattan

            channel_4 = microfluidics.RoundedChannel(trace_template=self.cell.fluid_channel_template)  # used for routing
            channel_4_layout = channel_4.Layout()

            in_port_2 = microfluidics.FluidicPort(position=p2, trace_template=self.cell.fluid_channel_template)
            in_port_2.angle_deg =  0#angle #225

            out_port_5 = microfluidics.FluidicPort(position=p5, trace_template=self.cell.fluid_channel_template)
            out_port_5.angle_deg = 180
            channel_4_layout.set(bend_radius = self.reservoir.res_radius*0.35, shape = RouteManhattan(input_port=in_port_1,
                                                                             points=[p1,p2,p3,p4,p5],
                                                                             output_port=out_port_5,
                                                                             bend_radius = 50.0))
            insts += i3.SRef(name = "Route_11", reference = channel_4)

            # Vacuum input channel segment
            radius = self.radius_fluid + self.vacuum_channel_circular + self.membrane_thickess
            channel6 = microfluidics.Channel(trace_template = self.cell.vacuum_channel_template)

            channel6_lo = channel6.Layout(shape=[(0, 0), (0, self.inlet_channel_length+self.vacuum_channel_circular*0.5)])
            insts += i3.SRef(channel6_lo,
                             position=(0, radius-self.vacuum_channel_circular*0.5),
                             transformation=i3.Rotation((0.0, 0.0), 0.0))

            return insts

        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            ports += microfluidics.FluidicPort(name = "in",
                                               position = (-2.0*self.reservoir.res_radius,0.0), angle = 180.0,
                                               trace_template=self.fluid_channel_template
                                               )

            ports += microfluidics.FluidicPort(name ="out", position = (4.0*self.reservoir.res_radius,0.0),
                                               angle = 0.0,
                                               trace_template=self.fluid_channel_template
                                               )

            ports += microfluidics.FluidicPort(name="vacuum_in",
                                               position=(0.,
                                                         self.radius_fluid + self.vacuum_channel_circular + self.membrane_thickess + self.inlet_channel_length),
                                               angle=90.0,
                                               trace_template=self.vacuum_channel_template
                                               )

            return ports
