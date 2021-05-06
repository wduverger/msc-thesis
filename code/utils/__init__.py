# Import utility functions
import matplotlib

from .data_reading import read_power_data, read_msr, shutdown_jvm
from .data_analysis import stack_to_rgb, align_stack, align_multiple_stacks,find_steps, compensate_bleaching
from .data_visualisation import add_scalebar, add_colourwheel, generate_wheel

# Apply default  figure styling
linewidth = (169-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth  # Standard matplotlib aspect ratio

matplotlib.rc('font', size=6)
matplotlib.rc('figure', figsize=(linewidth, figheight))
matplotlib.rc('savefig', bbox='tight')
