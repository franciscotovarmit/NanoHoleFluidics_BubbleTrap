#from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry

from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from debri_trap_arrayV2 import * #JoinedObstacles
import math

#Trap has been updated with boolean operation, to have flat ends

class InletHole(i3.PCell):
    """A generic cell trap class. It is defined by a boundary which are defined by points
    """
    _name_prefix = "INLETHOLE" # a prefix added to the unique identifier
    res_radius = i3.PositiveNumberProperty(default=600*0.5, doc="radius of reservoir")
    anglein = i3.PositiveNumberProperty(default=0.01, doc="port angle")
    angleout = i3.PositiveNumberProperty(default=180, doc="port angle")
    fillet_radius = i3.PositiveNumberProperty(default=600, doc="radius of fillet")
    length_channel = i3.PositiveNumberProperty(default=1000., doc="exit funnel length")
    width_channel_out = i3.PositiveNumberProperty(default=200., doc="width funnel length where route channels connect")
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template")
    TECH = i3.get_technology()
    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc='Layer to drawn on')

    class Layout(i3.LayoutView):
        # definition of the default values of the block PCELL
        block_length = i3.PositiveNumberProperty(default = 300.0)

        def _generate_elements(self, insts):

            circle = i3.ShapeCircle(center=(0.0, 0.0), radius=self.res_radius)
            #Define the boundaries for shapes
            br1 = i3.Boundary(layer = self.layer, shape = circle)

            channel_out = i3.ShapeRectangle(center=(self.length_channel*0.5, 0.0),
                                               box_size=(self.length_channel, self.width_channel_out))
            bo2 = i3.Boundary(layer=self.layer, shape=channel_out)
            b_sub = br1 | bo2

            #fillet
            #first create filling gaps rectangle
            filling_rect = i3.ShapeRectangle(center=(self.res_radius, 0.0),
                                               box_size=(self.res_radius, self.res_radius))
            bo2 = i3.Boundary(layer=self.layer, shape =filling_rect)
            b_sub = b_sub[0] | bo2


            fillet1_top = i3.ShapeRoundedRectangle(center=(self.res_radius+self.length_channel*0.43, self.width_channel_out),
                                               box_size=(self.length_channel, self.width_channel_out),
                                               radius=self.res_radius)
            bo2 = i3.Boundary(layer = self.layer, shape = fillet1_top)
            b_sub = b_sub[0] - bo2

            fillet1_bottom = i3.ShapeRoundedRectangle(
                center=(self.res_radius + self.length_channel * 0.43, -self.width_channel_out),
                box_size=(self.length_channel, self.width_channel_out),
                radius=self.res_radius)
            bo2 = i3.Boundary(layer=self.layer, shape=fillet1_bottom)
            b_sub = b_sub[0] - bo2


            s= i3.Structure(elements = b_sub)
            insts += i3.SRef(s)


            return insts

        def _generate_ports(self, ports):


            ports += microfluidics.FluidicPort(name='in', position = (self.length_channel, 0.0),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg= self.anglein,
                                               trace_template=self.channel_template
                                               )

            ports += microfluidics.FluidicPort(name='out', position = (self.length_channel, 0.0),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=self.angleout,
                                               trace_template=self.channel_template
                                               )

            return ports


# Main program
if __name__ == "__main__":
    res_radius = 800.0
    obstacle_diameter = 90
    obstacle_gap = 30.0

    #define properties in mother object ?
    res = InletHole()#(res_radius = res_radius, obstacles =multipleObstacle)
    res_layout = res.Layout()
    res_layout.visualize(annotate=True)
    res_layout.visualize_2d()
    # visualize_2d displays a top down view of the fabricated layout
    #trap_layout.cross_section(i3.Shape([(0, 25), (100, 25)]), process_flow=TECH.VFABRICATION.PROCESS_FLOW).visualize()
    #lay.cross_section(i3.Shape([(-9, 3), (9, 3)]), process_flow=vfab_flow).visualize()
    #trap_layout.write_gdsii("erik_trapI3.gds")

