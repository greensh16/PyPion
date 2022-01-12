# Author: Sam Green, Created: 11-10-20

# Script to call all PyPion classes to plot Silo data.

from Plotting_Classes import Plotting2d, Plotting3d
from argparse_command import InputValues
#-------------------------------
import matplotlib
# Using this to stop matplotlib from using a $DISPLAY environment variable.
# i.e. This now works over ssh without the need for a x-server.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#-------------------------------
import warnings
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
#-------------------------------
line = InputValues()
time_dicts = line.time_dicts
dimen = line.dimen
#-------------------------------

for files in time_dicts:

     arr = time_dicts[files]

     var1 = ["Density", -22.1, -27, "viridis", 'y', 127]
     #var1 = ["Temperature", 8, 2, "inferno", 'y', 63]

     fig = plt.figure()

     if dimen == "2d" or dimen == "2D":
          a = Plotting2d(arr).plot2d_1(var1[0], fig, var1)

     elif dimen == "3d" or dimen == "3D":
          #a = Plotting3d(arr).XZXYslice(var1[0], fig, var1)
          a = Plotting3d(arr).Bmag(var1[0], fig, var1)
          #a = Plotting3d(arr).XY_slice(var1[0], fig, var1)
          #a = Plotting3d(arr).Xpos(var1[0], fig, var1)

     else:
          print("Please choose a correct dimenion (1d, 2d, or 3d)")

     imagefile = "%s%s_%s.png" % (line.img_path, line.img_file, time_dicts[files][0][len(time_dicts[files][0]) - 13:len(time_dicts[files][0]) - 5])
     plt.savefig(imagefile, bbox_inches='tight', dpi=300)

     del fig
