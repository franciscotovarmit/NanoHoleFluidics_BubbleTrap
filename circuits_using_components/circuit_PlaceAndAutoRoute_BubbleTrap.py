#from microfluidics_ipkiss3.technology import * #comment when running main script, uncomment to debug geometry
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics
import sys
import numpy as np
sys.path.append("/home/fran/PycharmProjects/ipkiss_projects_old/scripts2021/NanoHoleFluidics_BubbleTrap-Thach-comments")

from functions.position_coordinates import generate_positions

from components.bubble_trap import BubbleTrapFluid
# PCell containing several traps

class CircuitOfTraps(microfluidics.PlaceAndAutoRoute):
    """Parametric cell with several traps, which are stacked vertically (Parallel) or horizontally (Series)
    """
    #_name_prefix = "circuitOfTraps"
    type = i3.NumberProperty(default = 1) #  0 Paralell 1 Series
    block_distance = i3.NumberProperty(default = 400.) #distance betwn traps
    bubble_fluid_trap = i3.ChildCellListProperty() # Generating traps with Tee from Child Cell List Property
    n_blocks_x = i3.PositiveIntProperty(default = 5)  #how many traps in x
    n_blocks_y = i3.PositiveIntProperty(default = 1)  #how many traps in y
    x_footprint = i3.PositiveIntProperty(default = 8000) #footprint of the trap array in X
    y_footprint = i3.PositiveIntProperty(default = 1000) #footprint of the trap array in Y
    trace_template = microfluidics.ChannelTemplateProperty(default=microfluidics.ShortChannelTemplate().Layout(width=200.0))

    def _default_child_cells(self):
        return {"blk_w_tee{}".format(cnt) : self.bubble_fluid_trap[cnt]
                for cnt in range(self.n_blocks_x*self.n_blocks_y)}

    def _default_links(self):
        links = []
        bx = self.n_blocks_x
        #############   SERIES
        if self.type == 1:             # series
            #all interconnecting horizontally
            if self.n_blocks_x > 1:
                for cnty in range(0, self.n_blocks_y):
                 for cntd in range(0, (self.n_blocks_x-1)):
                    links.append(("blk_w_tee{}:out".format(cnty*bx+cntd), "blk_w_tee{}:in".format(cnty*bx+cntd+1)))

            #left connections
            for cntd in range(1, (self.n_blocks_y-1),2):
                #links.append(("blk_w_tee{}:in1".format(cntd * bx), "blk_w_tee{}:in1".format((cntd+1) * bx)))
                links.append(("blk_w_tee{}:in".format((cntd+1) * bx), "blk_w_tee{}:in".format(cntd * bx)))

            #right connections
            for cntd in range(1, (self.n_blocks_y),2):
                links.append(("blk_w_tee{}:out".format(cntd * bx-1), "blk_w_tee{}:out".format((cntd+1) * bx-1)))
        ########  END SERIES #################

        return links

    def _default_bubble_fluid_trap(self):  # Generating traps from Child Cell List Property
        return [BubbleTrapFluid(name="blk_w_tee_{}".format(cnt) )
                for cnt in range(self.n_blocks_x*self.n_blocks_y)]

    class Layout(microfluidics.PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            # generate grid
            x = np.linspace(0, self.cell.x_footprint, self.cell.n_blocks_x)
            y = np.linspace(0, self.cell.y_footprint, self.cell.n_blocks_y)
            print 'x: ',x
            # generate positions
            coords = generate_positions(x, y, self.type)

            return {"blk_w_tee{}".format(cnt): i3.Translation(coords[cnt])+i3.VMirror() #add mirror
                 for cnt in range(self.n_blocks_x*self.n_blocks_y)}

        def _generate_ports(self, ports):
            # Add ports
            if self.type == 0:
                ports += i3.expose_ports(self.instances,{
                    'blk_w_tee0:in': 'in',
                    'blk_w_tee{}:out'.format(self.n_blocks_x-1): 'out'
                })

            if self.type == 1:
                if self.n_blocks_y %2 == 0:
                    ports += i3.expose_ports(self.instances,{
                    'blk_w_tee0:in': 'in',
                    'blk_w_tee{}:in'.format(self.n_blocks_x*self.n_blocks_y-self.n_blocks_x): 'out' # last left
                })
                else:
                    ports += i3.expose_ports(self.instances, {
                        'blk_w_tee0:in': 'in',
                        'blk_w_tee{}:out'.format(self.n_blocks_x*self.n_blocks_y - 1): 'out'  # last right
                    })

            return ports

if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"
    import numpy as np
    x_footp = 8000 #foot print of array on X
    y_footp = 2500 #foot print of array on Y
    n_traps_x= 5
    n_traps_y = 1

    myCircuiTrap = CircuitOfTraps(name = "circuitOfTraps",
                             n_blocks_x = n_traps_x,
                             n_blocks_y = n_traps_y,
                             x_footprint = x_footp,
                             y_footprint = y_footp,
                             type= 1# 0 Paralell, 1 Series
                          )

    myCircuiTrap_layout = myCircuiTrap.Layout(bend_radius =300)
    myCircuiTrap_layout.write_gdsii("fluidtrap_vacuum.gds")


    myCircuiTrap_layout.visualize(annotate = True)
