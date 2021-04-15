# %%

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import utils.jones as j

def arrow(ax, x0, x1, **kwargs):
    ax.annotate('', x0, x1, arrowprops=kwargs)

def plot_axes(ax):
    ax.set_aspect(1)

    ax.set(xlim=[-1,1], ylim=[-1,1], xticks=[], yticks=[])
    ax.axis('off')        
    ax.annotate('f', (.95, .04))
    ax.annotate('s', (.04, .95))
    arrow(ax, (-1, 0), (1, 0), arrowstyle='<-')
    arrow(ax, (0, -1), (0, 1), arrowstyle='<-')
    return fig, ax

# %%

fix, ax = plt.subplots(1)
plot_axes(ax)
arrow(ax, (0, 0), (.5, .5), arrowstyle='<-', color='r')
arrow(ax, (0, 0), (0, .5), arrowstyle='<-', color='r')
arrow(ax, (0, 0), (.5, 0), arrowstyle='<-', color='r')

# %%


def linear_pol(ax, angle):
    x = np.cos(angle * np.pi / 180)
    y = np.sin(angle * np.pi / 180)
    ax.arrow(-x, -y, 2*x, 2*y, #arrowstyle='<->', 
        length_includes_head=True,
        color='r', lw=1, head_width=.05)
    ax.arrow(x, y, -2*x, -2*y, #arrowstyle='<->', 
        length_includes_head=True,
        color='r', lw=1, head_width=.05)    

fix, ax = plt.subplots(1, 5, dpi=100)
t = np.linspace(0, 180, 5)

for i in range(5):
    plot_axes(ax[i])
    linear_pol(ax[i], t[i])


# %%

def ellipse(ax, emax, emin, t, head_width=.15, clockwise=True):
    head_length=1.5*head_width

    ax.add_patch(Ellipse((0,0), emax*2, emin*2, angle=t, fill=None, edgecolor='r'))

    m = -np.tan((90-t)*np.pi/180)

    x1, y1 = emax*np.cos(t*np.pi/180), emax*np.sin(t*np.pi/180) # Mid point
    d = .5*head_length
    c, s = np.sin((t-90)*np.pi/180), np.cos((t-90)*np.pi/180)
    # display((t, x1, y1, (x1-d*c, y1-d*s), (x1-2*d*c, y1-2*d*s)))

    arrow_coords = (x1-d*s, y1-d*c, 2*d*s, 2*d*c) if clockwise else (x1+d*s, y1+d*c, -2*d*s, -2*d*c)
    ax.arrow(*arrow_coords,
        length_includes_head=True, 
        color='r', lw=0, head_width=head_width, head_length=head_length
    )

fix, ax = plt.subplots(1, 5, dpi=100)
t = np.linspace(0, 180, 5)

for i in range(5):
    plot_axes(ax[i])
    ellipse(ax[i], .8, .4, t[i], clockwise=False)

# %%
def plot_pol(ax, jones_vector):
    ex = jones_vector[0, 0]
    ey = jones_vector[1, 0]

    delta = np.angle(ey) - np.angle(ex)
    alpha = np.arctan(np.abs(ey/ex))

    psi = np.arctan(np.tan(2*alpha)*np.cos(delta))/2
    chi = np.arcsin(np.sin(2*alpha)*np.sin(delta))/2

    print(jones_vector)
    print(delta*180/np.pi)

    # if np.abs(chi) < .01:
    linear_pol(ax, psi*180/np.pi)
    # else:
    #     ellipse(ax, emax, emin, psi*180/np.pi)



fix, ax = plt.subplots(1, 5, dpi=100)
t = np.linspace(0, 180, 5)

for i in range(5):
    print(t[i])
    plot_axes(ax[i])
    plot_pol(ax[i], j.S_4() @ j.p_linear(t[i] * np.pi / 180))
    print('--')

# %%
