# Author: Sam Green, Created: 20-10-17
# Script that defines functions to use the data created from core2D_Silo.py to plot the silo file's data.

# Comments from previous script version (Silo_Plot.py):
# -2016-09-22 SG: Created to work with the Bubble Nebula simulations, adapted from MultiMesh_Silo_plot.py.
# -2016-09-23 JM/SG: Correction to fix the "too many files open" bug; edited to accommodate new InputValues class.
# -2016-12-14 JM: Set up instance of class "ThisFile" to try to fix
#   memory leak problems.  Also only setup InputValues() once.
# -2017-01-17 SG: Set density and temperature to a constant max and min.
# -2017-5-22 SG: Few small changes made to fix some bugs.

# New comments:
# -2017-10-28 SG: Set up plotting code as a function
# -2017-11-6 SG: New class to plot velocity data as vector/streamline
# -2017-12-05 SG: Few changes made to temp plotting function.
# -2019-07-22 SG: Added class to plot slices of the 3D data.
# -2019-08-12 SG: Tidied up a few things.

# -------------- Set of libraries needed:
from ReadData import Read2dSiloData, Read3dSiloData
from matplotlib.colorbar import Colorbar

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MultipleLocator

import numpy as np
from astropy import units as u

plt.rc('font', **{'size': 12})
# plt.rc('lines', linewidth=2)
plt.rc('font', weight='bold')  # <-------------

# -------------- Class to plot the data from 2d Silo files.


class Plotting2d(Read2dSiloData):
    def plotsilo_2d(self, lim_min, lim_max, fig, var1, var2, alpha=1):
        xmin = self.xmin().to(u.pc)  # Set data to units of parsecs.
        xmax = self.xmax().to(u.pc)

        var1 = var1
        var2 = var2

        level_min = self.level_min().to(u.pc)  # Set data to units of parsecs.
        level_max = self.level_max().to(u.pc)

        ax1 = fig.add_subplot(2, 1, 1)
        ax1.set_title('      Time = %5.5f Myr' % self.sim_time().value)

        if var1[4] == 'log':
            log_d = np.log10(self.reshaped_parameter2d(var1[0]))
        else:
            log_d = self.reshaped_parameter2d(var1[0])

        ax1.set_xlim(lim_min[0].value, lim_max[0].value)
        ax1.set_ylim(lim_min[1].value, lim_max[1].value)

        im1 = ax1.imshow(log_d, interpolation='nearest', cmap=var1[3],
                         extent=[level_min[0].value, level_max[0].value, level_min[1].value,
                                 level_max[1].value],
                         origin='lower', vmax=var1[1], vmin=var1[2], alpha=alpha)
        divider1 = make_axes_locatable(ax1)  # Create divider for existing axes instance.
        cax1 = divider1.append_axes("right", size="5%", pad=0.05)  # Append axes to the right of ax1.
        cbar1 = plt.colorbar(im1, cax=cax1, ticks=MultipleLocator(1),
                             format="%.2f")  # Create colorbar in the appended axes.
        txt1 = ax1.text(0.8, 0.92, r'$log(\rho)$', transform=ax1.transAxes)
        ax1.axes.get_xaxis().set_visible(False)  # Remove the x-axis.

        # Temperature plot:
        ax2 = fig.add_subplot(2, 1, 2)

        if var1[4] == 'log':
            log_t = np.log10(self.reshaped_parameter2d(var2[0]))
        else:
            log_t = self.reshaped_parameter2d(var2[0])

        ax2.set_xlim(lim_min[0].value, lim_max[0].value)
        ax2.set_ylim(-lim_max[1].value, lim_min[1].value)

        im2 = ax2.imshow(log_t, interpolation='nearest', cmap=var2[3],
                         extent=[level_min[0].value, level_max[0].value,
                                 -level_max[1].value, -level_min[1].value],
                         vmax=var2[1], vmin=var2[2], alpha=alpha)
        divider2 = make_axes_locatable(ax2)
        cax2 = divider2.append_axes("right", size="5%", pad=0.05)
        cbar2 = plt.colorbar(im2, cax=cax2, ticks=MultipleLocator(1), format="%.2f")
        txt2 = ax2.text(0.8, 0.05, r'$log(T)$', transform=ax2.transAxes, color='white')
        ax2.set_xlabel('     x-axis (pc)')
        ax2.set_ylabel('                                              z-axis (pc)')

        fig.subplots_adjust(wspace=0, hspace=0)  # Remove the whitespace between the images

        del xmin
        del xmax
        # del var1
        # del var2
        # del level_min
        # del level_max
        # del log_d
        # del log_t
        # del im1
        # del im2
        # self.db.close()
        # del self.db

        return fig


class Plotting3d(Read3dSiloData):
    def plotsilo_3dslice(self, lim_min, lim_max, fig, gs, var1, alpha=1):
        xmin = self.xmin().to(u.pc)  # Set data to units of parsecs.
        xmax = self.xmax().to(u.pc)

        var1 = var1

        level_min = self.level_min().to(u.pc)  # Set data to units of parsecs.
        level_max = self.level_max().to(u.pc)

        x_sliced_parameter3d = self.reshaped_parameter3d(var1[0])[var1[6], :, :]
        y_sliced_parameter3d = self.reshaped_parameter3d(var1[0])[:, var1[6], :]
        z_sliced_parameter3d = self.reshaped_parameter3d(var1[0])[:, :, 127]

        if var1[4] == 'log':
            log_dx = np.log10(x_sliced_parameter3d)
            log_dy = np.log10(y_sliced_parameter3d)
            log_dz = np.log10(z_sliced_parameter3d)
        else:
            log_dx = x_sliced_parameter3d
            log_dy = y_sliced_parameter3d
            log_dz = z_sliced_parameter3d

        # --------------Left Plot----------------------------
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_title('                                                   Time = %5.5f Myr' % self.sim_time().value)

        ax1.set_xlim(lim_min[0].value, lim_max[0].value)
        ax1.set_ylim(lim_min[1].value, lim_max[1].value)

        im1 = ax1.imshow(log_dy, interpolation='nearest', cmap=var1[3],
                         extent=[level_min[0].value, level_max[0].value, level_min[1].value,
                                 level_max[1].value],
                         origin='lower', vmax=var1[1], vmin=var1[2], alpha=alpha)
        # txt1 = ax1.text(0.8, 0.92, r'$log(\rho)$', transform=ax1.transAxes)
        ax1.set_xlabel('x-axis (pc)')
        ax1.set_ylabel('z-axis (pc)')

        # --------------Middle Plot----------------------------
        ax2 = fig.add_subplot(gs[0, 1])
        # ax2.set_title('Time = %5.5f Myr' % self.sim_time().value)

        ax2.set_xlim(lim_min[0].value, lim_max[0].value)
        ax2.set_ylim(lim_min[2].value, lim_max[2].value)

        im2 = ax2.imshow(log_dx, interpolation='nearest', cmap=var1[3],
                         extent=[level_min[0].value, level_max[0].value, level_min[2].value,
                                 level_max[2].value],
                         origin='lower', vmax=var1[1], vmin=var1[2], alpha=alpha)
        # txt2 = ax2.text(0.8, 0.92, r'$log(\rho)$', transform=ax1.transAxes)
        ax2.set_xlabel('x-axis (pc)')
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()
        ax2.set_ylabel('y-axis (pc)')

        cbax = plt.subplot(gs[-1, 0:])
        cb = Colorbar(ax=cbax, mappable=im1, orientation='horizontal', ticklocation='bottom')
        # cb.set_label(r'Colorbar !', labelpad=10)

        del xmin
        del xmax
        del log_dx
        del log_dy
        del log_dz
        del x_sliced_parameter3d
        del y_sliced_parameter3d
        del z_sliced_parameter3d
        del var1
        del level_min
        del level_max
        del im1
        del im2
        del ax1
        del ax2

        return fig
