from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics
import sys
import numpy as np
sys.path.append("/home/fran/PycharmProjects/ipkiss_projects_old/scripts2021/microfluidics-thach-comments-master")

from functions.position_coordinates import generate_positions

from components.bubble_trap_vac import VacuumTrap
# PCell containing several traps

class CircuitOfVacTraps(microfluidics.PlaceAndAutoRoute):
    """Parametric cell with several traps, which are stacked vertically (Parallel) or horizontally (Series)
    """
    #_name_prefix = "circuitOfTraps"
    type = i3.NumberProperty(default = 0) #  0 Paralell 1 Series
    block_distance = i3.NumberProperty(default = 400.) #distance betwn traps
    vacuum_trap = i3.ChildCellListProperty() #Generating vacuum traps fromm Child Cell List Property
    n_blocks_x = i3.PositiveIntProperty(default = 5) #how many traps in x
    n_blocks_y = i3.PositiveIntProperty(default = 1) #how many traps in y
    x_footprint = i3.PositiveIntProperty(default = 8000)  #footprint of the trap array in X
    y_footprint = i3.PositiveIntProperty(default = 1000)  #footprint of the trap array in Y
    trace_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate().Layout(width=200.0))

    def _default_child_cells(self):
        return {"vac_{}".format(cnt) : self.vacuum_trap[cnt]
                for cnt in range(self.n_blocks_x*self.n_blocks_y)}

    def _default_links(self):
        links = []  #no links needed on this design, this function can be removed
        return links

    def _default_vacuum_trap(self):  # Generating traps from Child Cell List Property
        return [VacuumTrap(name="vac_{}".format(cnt),
                           vacuum_channel_circular=200,
                           membrane_thickess=30,
                           radius_fluid=300)
                for cnt in range(self.n_blocks_x*self.n_blocks_y)]

    class Layout(microfluidics.PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            # generate grid
            x = np.linspace(0, self.cell.x_footprint, self.cell.n_blocks_x)
            y = np.linspace(0, self.cell.y_footprint, self.cell.n_blocks_y)
            print 'x: ',x
            # generate positions
            coords = generate_positions(x, y, self.type)

            return {"vac_{}".format(cnt): i3.Translation(coords[cnt])+i3.VMirror() #add mirror
                 for cnt in range(self.n_blocks_x*self.n_blocks_y)}

        def _generate_ports(self, ports):
                ports += i3.expose_ports(self.instances,
                                         {'vac_0:in': 'in1',
                                          'vac_1:in': 'in2',
                                          'vac_2:in': 'in3',
                                          'vac_3:in': 'in4',
                                          'vac_4:in': 'in5'
                                          })
                #below didnt work!
                '''
                for cnt in range(self.n_blocks_x * self.n_blocks_y):
                    ports += i3.expose_ports(self.instances,{'vac_{}:in'.format(cnt): 'in{}'.format(cnt)})
                    #ports += i3.OpticalPort(name ={'vac_{}:in'.format(cnt): 'in{}'.format(cnt)})
                    print 'ports?: ',ports
                '''
                print 'ports?: ', ports
                return ports

if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"
    import numpy as np
    x_footp = 8000 #foot print of array on X
    y_footp = 2500 #foot print of array on Y
    n_traps_x= 5
    n_traps_y = 1

    myCircuiTrap = CircuitOfVacTraps(name = "circuitOfTraps",
                             n_blocks_x = n_traps_x,
                             n_blocks_y = n_traps_y,
                             x_footprint = x_footp,
                             y_footprint = y_footp,
                             type= 1# 0 Paralell, 1 Series
                          )

    myCircuiTrap_layout = myCircuiTrap.Layout(bend_radius =300)
    myCircuiTrap_layout.write_gdsii("trap_vacuum.gds")
    myCircuiTrap_layout.visualize(annotate = True)
