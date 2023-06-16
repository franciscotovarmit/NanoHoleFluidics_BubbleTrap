import sys
#sys.path.append("C:/Users/e54491/OneDrive - RMIT University-/Software")
#sys.path.append("C:/Users/e54491/OneDrive - RMIT University-/Investigations/Staff/Francisco/NanoHoleFluidics_BubbleTrap")
sys.path.append("/home/fran/PycharmProjects/ipkiss_projects_old/scripts2021/NanoHoleFluidics_BubbleTrap-Thach-comments")

from microfluidics_pdk.technology import *

# Import IPKISS3 Packages.

from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics
import microfluidics_pdk.all as pdk

from components.bubble_trap import BubbleTrap

from components.Array_Stamps_Neg import DebriTrapSingle
from components.Array_Stamps_Neg import Obstacle_Left
from components.Array_Stamps_Neg import Obstacle_Right
from components.Array_Stamps_Neg import JoinedObstacles

from components.reservoir import Reservoir

# Thach: Import reservoir

res_radius = 300.0
obstacle_diameter = 40
obstacle_gap = 30.0

singleObstacle = DebriTrapSingle(obstacle_trap_radius=obstacle_diameter * 0.5,
                                          gap_btw_barriers=obstacle_gap,
                                          cInp=(0.0, 0.0))
singleObstacle_Layout = singleObstacle.Layout()
LeftFilling = Obstacle_Left(obstacle_trap_radius=obstacle_diameter * 0.5,
                            gap_btw_barriers=obstacle_gap,
                            cInp=(0.0, 0.0))
Obstacle_Left_Layout = LeftFilling.Layout()
RightFilling = Obstacle_Right(obstacle_trap_radius=obstacle_diameter * 0.5,
                              gap_btw_barriers=obstacle_gap,
                              cInp=(0.0, 0.0))
Obstacle_Right_Layout = RightFilling.Layout()
multipleObstacle = JoinedObstacles(wholeTrapX=res_radius * 1.2,  # 2000,
                                   wholeTrapY=1000,  # 2500,
                                   leftFilling=LeftFilling,
                                   rightFilling=RightFilling,
                                   mysingleObstacle=singleObstacle,
                                   trap_diameter=obstacle_diameter,
                                   trap_gap=obstacle_gap
                                   )

# define properties in mother object ?
res = Reservoir(res_radius=res_radius, obstacles=multipleObstacle)

fluid_channel_template = pdk.FluidChannelTemplate()
fluid_channel_template.Layout(channel_width=200)

vacuum_channel_template = pdk.VacuumChannelTemplate()
vacuum_channel_template.Layout(channel_width=200)


trap = BubbleTrap(reservoir=res,
                  fluid_channel_template=fluid_channel_template,
                  vacuum_channel_template=vacuum_channel_template)

trap_layout = trap.Layout()
trap_layout.visualize(annotate=True)
trap_layout.visualize_2d()
trap_layout.write_gdsii("trap_fluid.gds")

