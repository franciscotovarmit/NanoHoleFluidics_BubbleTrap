# Import the Microfluidic Technology File.
from microfluidics_ipkiss3.technology import *
# Import IPKISS3 Packages.
from ipkiss3 import all as i3
import math
import numpy as np
# Import microfluidics API.

import microfluidics_ipkiss3.all as microfluidics

# Define a Custom Class.
class NanoHoleArrayF(i3.PCell):

    # Properties of trap
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate().Layout(width=150),
                                                             doc="Channel template of the tee")

    _name_prefix = "VacTrapV" # a prefix added to the unique identifier

    radius_fluid =i3.PositiveNumberProperty(default=1500., doc="radius of the circular vacuum section collecting air")
    vacuum_channel_circular =i3.PositiveNumberProperty(default=500., doc="width of circular channel collecting air")
    inlet_channel_length = i3.PositiveNumberProperty(default=300., doc="length of inlet channel vac")
    membrane_thickess = i3.PositiveNumberProperty(default=10., doc="length of inlet channel vac")
    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc='Layer to drawn on')


    cInp = i3.Coord2Property(default = (0.0,0.0),required = True)

    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):

            #central rounded rectangle
            crr = i3.RoundedRectangle(layer = self.layer,center=(0.0,0.0), box_size=(1800,600), radius=300,angle_step=1)
            s = i3.Structure(elements=crr)
            insts += i3.SRef(s)
            #end central rounded rectanlge

            #ring
            radius = self.radius_fluid + self.vacuum_channel_circular + self.membrane_thickess
            sr1 = i3.ShapeCircle(center=(0.0,0.0),radius=radius)
            sr2 = i3.ShapeCircle(center=(0.0,0.0),radius=radius-self.vacuum_channel_circular)
            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = self.layer, shape = sr1)
            br2 = i3.Boundary(layer=self.layer, shape=sr2)
            b_sub = br1-br2           #b_sub is the main circular channel vacuum

            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)
            #end ring

            #diver mask shape
            #Rectangles and circle definition
            sc1 = i3.ShapeRoundedRectangle(center = (0,700-50), box_size = (2050,500), radius=300)
            sc2 = i3.ShapeRoundedRectangle(center = (0,-700+50), box_size = (2050,500), radius=300)
            sr1 = i3.ShapeCircle(center=(0.0, -900), radius=300)

            #Define the boundaries for shapes
            top_rec = i3.Boundary(layer = self.layer, shape = sc1)#br1
            bot_rec = i3.Boundary(layer=self.layer, shape=sc2)#br2
            circ = i3.Boundary(layer = self.layer, shape = sr1)#bc1

            #add boundaries and add to the element list
            bot_rec_circ = bot_rec | circ  #bottom rectangle and circle, boolean op

            #two arcs are needed to define Left curvature
            #left arc 1
            sring = i3.ShapeRingSegment(center=(-600, 0), inner_radius=400, outer_radius=600,
                                      angle_end=270,
                                      angle_start=90,
                                        end_face_angle=90,
                                        start_face_angle=90
                                      )
            arc1 = i3.Boundary(layer=self.layer, shape=sring)

            #left arc 2
            sring = i3.ShapeRingSegment(center=(300, 0), inner_radius=1300, outer_radius=1500,
                                        #center=(-530, 0), inner_radius=650, outer_radius=900,
                                      angle_end=210,
                                      angle_start=150,
                                        end_face_angle=90,
                                        start_face_angle=90
                                      )
            arc2 = i3.Boundary(layer=self.layer, shape=sring)
            arcsL= arc1 | arc2  #adding left arcs

            rec_bot_arcL = bot_rec_circ[0] | arcsL[0] #adding bottom rectangle and left arcs
            rec_bot_arcL_rec_top = rec_bot_arcL[0] | top_rec   #adding top rectangle to previous geometry

            #two arcs are needed to define Rigth curvature
            #rigth arc 1
            sring = i3.ShapeRingSegment(center=(600, 0), inner_radius=400, outer_radius=600,
                                      angle_start=270,
                                      angle_end=90,
                                        end_face_angle=90,
                                        start_face_angle=90
                                      )
            arc1R = i3.Boundary(layer=self.layer, shape=sring)

            #left arc 2
            sring = i3.ShapeRingSegment(center=(-300, 0), inner_radius=1300, outer_radius=1500,
                                      angle_start=-30,#210,
                                      angle_end=30,#150,
                                        end_face_angle=90,
                                        start_face_angle=90
                                      )

            arc2R = i3.Boundary(layer=self.layer, shape=sring)
            arcsR = arc1R | arc2R   #adding right arcs together
            diver_mask = rec_bot_arcL_rec_top[0] | arcsR[0]  #adding Right arcs to previous geometry
            s = i3.Structure(elements=diver_mask)
            insts += i3.SRef(s)

            return insts

        #Thach added to define one inlet and one outlet
        def _generate_ports(self, ports):  # Use _generate_ports method to define ports
            #ports += i3.OpticalPort(name = "in", position = (0., self.radius_fluid + self.vacuum_channel_circular + self.membrane_thickess + self.inlet_channel_length), angle = 90.0)

            return ports

# Main program
if __name__ == "__main__":
    trap = NanoHoleArrayF(vacuum_channel_circular = 500,
                      membrane_thickess =30,
                      radius_fluid = 1500)
    trap_layout = trap.Layout()
    trap_layout.visualize(annotate=True)
    trap_layout.visualize_2d()

