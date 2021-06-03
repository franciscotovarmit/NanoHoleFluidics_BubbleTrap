# Import the Microfluidic Technology File.

from microfluidics_ipkiss3.technology import *

# Import IPKISS3 Packages.

from ipkiss3 import all as i3
import math
import numpy as np
# Import microfluidics API.

import microfluidics_ipkiss3.all as microfluidics

# Define a Custom Class.
class VacuumTrap(i3.PCell):

    # Properties of trap
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate().Layout(width=150),
                                                             doc="Channel template of the tee")



    _name_prefix = "VacTrapV" # a prefix added to the unique identifier

    radius_fluid =i3.PositiveNumberProperty(default=300., doc="radius of the circular vacuum section collecting air")
    vacuum_channel_circular =i3.PositiveNumberProperty(default=200., doc="width of circular channel collecting air")
    inlet_channel_length = i3.PositiveNumberProperty(default=300., doc="length of inlet channel vac")
    membrane_thickess = i3.PositiveNumberProperty(default=10., doc="length of inlet channel vac")
    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc='Layer to drawn on')


    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):

            radius = self.radius_fluid + self.vacuum_channel_circular + self.membrane_thickess
            sr1 = i3.ShapeCircle(center=(0.0,0.0),radius=radius)
            sr2 = i3.ShapeCircle(center=(0.0,0.0),radius=radius-self.vacuum_channel_circular)

            #Rectangles to be substracted to concentric circle shape
            sc1 = i3.ShapeRectangle(center = (self.cInp.x-radius,-radius),
                                    box_size = (radius*2,radius*2+300)) #300 has to be linked to channel input width))
            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = self.layer, shape = sr1)
            br2 = i3.Boundary(layer=self.layer, shape=sr2)

            bc1 = i3.Boundary(layer = self.layer, shape = sc1)

            #Substruct boundaries and add to the element list
            b_sub = br1-br2           #b_sub is the main circular channel vacuum

            barrier_dim = 25
            point_list = []
            point_list.append((-barrier_dim*0.5, -barrier_dim*0.5))
            point_list.insert(0,(-barrier_dim*0.5, barrier_dim*0.5))
            point_list.append((barrier_dim*0.5, -barrier_dim*0.5))
            point_list.insert(0,(barrier_dim*0.5,barrier_dim*0.5))

            #bumps
            t = i3.Shape(point_list, closed=True)
            radius_m = self.radius_fluid + self.membrane_thickess

            angle = np.linspace(275, 540, 40)
            for i in angle:
                bump = i3.Boundary(layer=self.layer,
                                   shape=t,
                                   transformation=(i3.Rotation((0.0, 0.0), i)+
                                                   i3.Translation((radius_m*math.cos(math.pi*(i)/180), radius_m*math.sin(math.pi*(i)/180))))
                                   )
                #substracting bumps to circle channel
                b_sub = b_sub[0] - bump

            #substract square
            b_sub = b_sub[0] - bc1
            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)

            #Input channel - segment
            channel1 = microfluidics.Channel(trace_template = self.cell.channel_template)

            channel1_lo = channel1.Layout(shape=[(0, 0), (0, self.inlet_channel_length+self.vacuum_channel_circular*0.5)])
            insts += i3.SRef(channel1_lo, position=(0, radius-self.vacuum_channel_circular*0.5), transformation=i3.Rotation((0.0, 0.0), 0.0))

            return insts

        #Thach added to define one inlet and one outlet
        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            ports += i3.OpticalPort(name = "in", position = (0., self.radius_fluid + self.vacuum_channel_circular + self.membrane_thickess + self.inlet_channel_length), angle = 90.0)

            return ports

# Main program
if __name__ == "__main__":
    trap = VacuumTrap(vacuum_channel_circular = 200, #300
                      membrane_thickess =30,
                      radius_fluid = 300)
    trap_layout = trap.Layout()
    trap_layout.visualize(annotate=True)
    trap_layout.visualize_2d()
    trap_layout.write_gdsii("trap_vacuum.gds")

