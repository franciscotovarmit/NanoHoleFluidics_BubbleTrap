from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry

from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from supplementary_objects import Wafer, Triangle
import math

#Trap has been updated with boolean operation, to have flat ends

class MarksWafer(i3.PCell):
    """A generic cell trap class. It is defined by a boundary which are defined by points
    """
    _name_prefix = "MARKSWAFER" # a prefix added to the unique identifier
    triangleSide = i3.ChildCellProperty(default= Triangle(), doc="side triangle mark")
    wafer = i3.ChildCellProperty(default=Wafer(size=29.8e3), doc="radius of reservoir")
    position = i3.PositiveNumberProperty(default=10e3, doc="position of triangle")
    channel_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate(), doc="Channel template")
    TECH = i3.get_technology()
    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.CH2.TRENCH, doc='Layer to drawn on')


    class Layout(i3.LayoutView):

        def _generate_elements(self, insts):

            #wafer
            offset =100
            insts += i3.SRef(reference =self.wafer, position=(0., 0.),
                             #transformation=i3.Rotation((0.0, 0.0), 0.0)
                             )
            #triangles
            insts += i3.SRef(reference =self.triangleSide, position=(10e3-offset, 10e3-offset),
                             transformation=i3.Rotation((0.0, 0.0), 180.0)
                             )
            insts += i3.SRef(reference =self.triangleSide, position=(-10e3+offset, 10e3-offset),
                             transformation=i3.Rotation((0.0, 0.0), -90.0)
                             )
            insts += i3.SRef(reference =self.triangleSide, position=(-10e3+offset, -10e3+offset),
                             transformation=i3.Rotation((0.0, 0.0), 0.0)
                             )
            insts += i3.SRef(reference =self.triangleSide, position=(10e3-offset, -10e3+offset),
                             transformation=i3.Rotation((0.0, 0.0), 90.0)
                             )
            return insts


# Main program
if __name__ == "__main__":
    marksWafer = MarksWafer()
    marksWafer_layout = marksWafer.Layout()
    marksWafer_layout.visualize(annotate=True)
    marksWafer_layout.visualize_2d()
    # visualize_2d displays a top down view of the fabricated layout
    #trap_layout.cross_section(i3.Shape([(0, 25), (100, 25)]), process_flow=TECH.VFABRICATION.PROCESS_FLOW).visualize()
    #lay.cross_section(i3.Shape([(-9, 3), (9, 3)]), process_flow=vfab_flow).visualize()
    #trap_layout.write_gdsii("erik_trapI3.gds")

