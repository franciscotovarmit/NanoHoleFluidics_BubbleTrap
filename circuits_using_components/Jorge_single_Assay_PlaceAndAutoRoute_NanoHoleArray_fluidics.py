from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics
import sys
sys.path.append("/home/fran/PycharmProjects/ipkiss_projects_old/scripts2021/microfluidics-thach-comments-master")
from components.nanohole_array_vacuum import NanoHoleArrayF
from components.marks_wafer import MarksWafer

class SingleAssay(microfluidics.PlaceAndAutoRoute):
    """Parametric cell defining Reservoir, Assay and Outlet"""
    _name_prefix = "singleAssay"
    nanoHarrayFluidics =  i3.ChildCellProperty(default= NanoHoleArrayF())
    marks = i3.ChildCellProperty(default = MarksWafer())
    trace_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate().Layout(width=200))

    def _default_child_cells(self):
        return {
                "assay":self.nanoHarrayFluidics,
                "marks":self.marks
                }

    def _default_links(self):
        links = []
        return links  #No links needed in this design (this def function can be removed)

    class Layout(microfluidics.PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            return {
                    "assay":  i3.Translation((33e3, 0.0)),
                    "marks":i3.Rotation(rotation=0) + i3.Translation((33e3, 0))
                    }

        def _generate_ports(self, ports):
                return ports

if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"
    myCircuiTrap = SingleAssay()
    myCircuiTrap_layout = myCircuiTrap.Layout()
    myCircuiTrap_layout.visualize(annotate=True)
    myCircuiTrap_layout.visualize_2d()
    myCircuiTrap_layout.write_gdsii("Jorge_nano_holeArray_assayio.gds")