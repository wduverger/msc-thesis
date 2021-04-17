# %%

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def p_linear(theta=0):
    return np.array([[np.cos(theta)], [np.sin(theta)]])

def intensity(p):
    return np.squeeze(p.conjugate().T @ p).real

def S_rotate(theta):
    cos = np.cos(theta)
    sin = np.sin(theta)
    return np.array([[cos, sin], [-sin, cos]])

def S_pol(phi=0):
    return S_rotate(-phi) @ np.array([[1, 0], [0, 0]])  @ S_rotate(phi)

def S_4(phi=0):
    return S_rotate(-phi) @ np.array([[1, 0], [0, 1j]]) @ S_rotate(phi)

def S_2(phi=0):
    return S_rotate(-phi) @ np.array([[1, 0], [0, -1]]) @ S_rotate(phi)

def arrow(ax, x0, x1, **kwargs):
    ax.annotate('', x0, x1, arrowprops=kwargs)

def plot_empty(ax):
    ax.set_aspect(1)
    ax.set(xlim=[-1,1], ylim=[-1,1], xticks=[], yticks=[])
    # ax.axis('off')      
     # removing the default axis on all sides:
    for side in ['bottom','right','top','left']:
        ax.spines[side].set_visible(False)  

def plot_axes(ax):
    plot_empty(ax)
    ax.annotate('f', (.95, .04))
    ax.annotate('s', (.04, .95))
    arrow(ax, (-1, 0), (1, 0), arrowstyle='<-')
    arrow(ax, (0, -1), (0, 1), arrowstyle='<-')

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
    # linear_pol(ax, psi*180/np.pi)
    # else:
    #     ellipse(ax, emax, emin, psi*180/np.pi)



# fix, ax = plt.subplots(1, 5, dpi
# =100)
tt = np.linspace(0, 180, 5)

jvec = [S_4() @ p_linear(t * np.pi / 180) for t in tt]
ex = [j[0, 0] for j in jvec]
ey = [j[1, 0] for j in jvec]
delta = np.array([
    np.angle(y) - np.angle(x) 
    for x, y in zip(ex, ey)
])
alpha = np.array([
    np.arctan(np.abs(y/x))    
    for x, y in zip(ex, ey)
])
psi = np.array([
    np.arctan(2 * x * y * np.cos(d) / (x**2 - y**2) )/2
    for x, y, d in zip(np.abs(ex), np.abs(ey), delta)
])
plt.scatter(tt, delta * 180/np.pi, label='delta')
plt.scatter(tt, alpha * 180/np.pi, label='alpha')
plt.scatter(tt, psi* 180/np.pi, label='psi')
plt.legend()
None

# %%

fix, ax = plt.subplots(1, 5, dpi=100)
plot_axes(ax[0])
linear_pol(ax[0], 0)

plot_axes(ax[1]

# %%
def plot_pol_ellipse(ax, jvec):
    ex = jvec[0,0]
    ey = jvec[1,0]

    t = np.linspace(0, 2*np.pi)
    x = np.real(ex * np.exp(1j * t))
    y = np.real(ey * np.exp(1j * t))
    d = np.angle(ey) - np.angle(ex)
    
    lefthanded = d > 0
    circular = d % np.pi > .1 and np.abs(ex) > .1
    color = 'C0' if not circular else (
        'C1' if lefthanded else 'C2'
    )
    ax.plot(x, y, color=color)


n = 9
jvec = [
    p_linear(t*np.pi/180)
    for t in np.linspace(0, 180, n)
] + [
    1/np.sqrt(2) * np.array([[1], [1j]]),
    1/np.sqrt(2) * np.array([[1], [-1j]])
]

fig, ax = plt.subplots(3, len(jvec), dpi=100)

for i, j in enumerate(jvec):
    plot_empty(ax[0, i])
    plot_empty(ax[1, i])
    plot_empty(ax[2, i])

    plot_pol_ellipse(ax[0, i],         j)
    plot_pol_ellipse(ax[1, i], S_2() @ j)
    plot_pol_ellipse(ax[2, i], S_4() @ j)

ax[0, 0].set(title='Original')
ax[1, 0].set(title='After HWP')
ax[2, 0].set(title='After QWP')


# %%
