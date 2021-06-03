from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics
import sys
sys.path.append("/home/fran/PycharmProjects/ipkiss_projects_old/scripts2021/microfluidics-thach-comments-master")

from components.inlet_hole_wfillet import InletHole
from components.vacuum_channel_route import VacuumChannelRoute
from circuit_PlaceAndAutoRoute_BubbleTrapVac import CircuitOfVacTraps

# PCell containing several traps
class SingleAssay(microfluidics.PlaceAndAutoRoute):
    """Parametric cell defining Reservoir, Assay and Outlet
    """
    _name_prefix = "singleAssay"
    inlet = i3.ChildCellProperty(default = InletHole(res_radius=750*.5))#i3.NumberProperty()#(default = 3e3)
    outlet = i3.ChildCellProperty(default =InletHole(res_radius=600*.5))#i3.NumberProperty()#(default = 3e3)
    vac_route = i3.ChildCellProperty(default=VacuumChannelRoute()) #change for array  #anything with two ports, stenosis, circuit, array, etc
    vac_traps =  i3.ChildCellProperty(default=CircuitOfVacTraps())
    trace_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate().Layout(width=150))

    def _default_child_cells(self):   #for PlaceAndAutoRoute
        return {"inlet":self.inlet, "assay":self.vac_route, "outlet":self.outlet, "vac_traps": self.vac_traps}

    def _default_links(self):
        links = [#("inlet:out", "assay:in1"),
                # ("assay:out1", "outlet:out"),
                 ("vac_traps:in1", "assay:vac1"),
                 ("vac_traps:in2", "assay:vac2"),
                 ("vac_traps:in3", "assay:vac3"),
                 ("vac_traps:in4", "assay:vac4"),
                 ("vac_traps:in5", "assay:vac5"),
                 ]
        return links

    def _default_external_port_names(self):
        return {"inlet:in":"in",
        "outlet:out":"out"}

    class Layout(microfluidics.PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            return {"inlet": i3.Rotation(rotation=0) + i3.Translation((-12000, -2e3)),
                    "assay": i3.Rotation(rotation=0) + i3.Translation((0.0e3, 0.0)),
                    "outlet": i3.Rotation(rotation=270) + i3.Translation((0, -1e3)),
                    "vac_traps": i3.Translation((-10.5e3, 0))
                    }


        def _generate_ports(self, ports):
            # Add ports
                '''ports += self.instances["assay"].ports[2]
                ports += self.instances["assay"].ports[3]
                ports += self.instances["assay"].ports[4]
                ports += self.instances["assay"].ports[5]
                ports += self.instances["assay"].ports[6]

                #ports += self.instances["vac_traps"].ports[1]
                '''
                return ports



if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"

    myCircuiTrap = SingleAssay()

    myCircuiTrap_layout = myCircuiTrap.Layout(bend_radius =200)
    myCircuiTrap_layout.visualize(annotate=True)
    myCircuiTrap_layout.visualize_2d()
    myCircuiTrap_layout.write_gdsii("Jorge_vacuum_route_traps_assayio.gds")