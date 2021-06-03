from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics
import sys
sys.path.append("/home/fran/PycharmProjects/ipkiss_projects_old/scripts2021/microfluidics-thach-comments-master")
from components.inlet_hole_wfillet import InletHole
from components.marks_wafer import MarksWafer
from circuit_PlaceAndAutoRoute_BubbleTrap import CircuitOfTraps

class SingleAssay(microfluidics.PlaceAndAutoRoute):
    """Parametric cell defining Reservoir, Assay and Outlet """
    _name_prefix = "singleAssay"
    inlet = i3.ChildCellProperty(default = InletHole(res_radius=750*.5)) #diameter of circle
    outlet = i3.ChildCellProperty(default =InletHole(res_radius=600*.5))
    traps =  i3.ChildCellProperty(default= CircuitOfTraps())
    inlet2 = i3.ChildCellProperty(default = InletHole(res_radius=600*.5), angleout = 90) #near NHA
    outlet2 = i3.ChildCellProperty(default =InletHole(res_radius=750*.5), angleout = 0) #outlet
    marks = i3.ChildCellProperty(default = MarksWafer())
    trace_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate().Layout(width=200))

    def _default_child_cells(self):   #for PlaceAndAut oRoute
        return {"inlet":self.inlet,  #inlet 1 where fluid gets in
                "assay":self.traps,  # series of traps
                "outlet":self.outlet, #outlet to nano H array
                "inlet2": self.inlet2,  #inlet for exit channel
                "outlet2": self.outlet2, #outlet
                "marks":self.marks
                }

    def _default_links(self):
        links = [("inlet2:in", "outlet2:out")
                 ]
        return links

    def _default_external_port_names(self):
        return {"inlet:in":"in",
        "outlet:out":"out"}

    class Layout(microfluidics.PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            return {"inlet": i3.Rotation(rotation=0) + i3.Translation((-12000, 0e3)),
                    "assay":  i3.Translation((-.5e3, 0.0)),
                    "outlet": i3.Rotation(rotation=180) + i3.Translation((-0.6e3, 0e3)),
                    "inlet2": i3.Rotation(rotation=0) + i3.Translation((0.6e3, 0e3)),
                    "outlet2": i3.Rotation(rotation=180) + i3.Translation((12e3, 0e3)),
                    "marks":i3.Rotation(rotation=0) + i3.Translation((0, 0))
                    }

        def _generate_ports(self, ports):
                return ports

if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"
    myCircuiTrap = SingleAssay()
    myCircuiTrap_layout = myCircuiTrap.Layout(bend_radius =200)
    myCircuiTrap_layout.visualize(annotate=True)
    myCircuiTrap_layout.visualize_2d()
    myCircuiTrap_layout.write_gdsii("Jorge_bubble_traps_assayio.gds")