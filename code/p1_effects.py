# %%
import utils
import utils.jones as j

import numpy as np
import matplotlib.pyplot as plt

# %%
msr = utils.read_msr('../data/21-04-28 - qwp 110.msr')
utils.shutdown_jvm()

# %% plot data

colour = [f'C{i}' for i in range(4)]
ls = [(0,(1,2)),(0, (1,1)),'--','-']
deg = lambda x: f'{x}°'

im = lambda p1, p2: msr[f'p1{p1}p2{p2}'].sum(axis=(1,2))
x_axis = np.arange(0, 171, 10)

fig, ax = plt.subplots(
    2, 4, 
    figsize=(utils.linewidth, 1.5*utils.figheight),
    sharey=True, sharex=True, gridspec_kw=dict(wspace=0.2, hspace=.4)
)

pp = [0,45,90,135]
for i, p in enumerate(pp):
    l = ax[0, 0].plot(x_axis, im(p1=p,   p2=0), color=colour[0], ls=ls[i])
    l = ax[0, 1].plot(x_axis, im(p1=p,  p2=45), color=colour[1], ls=ls[i])
    l = ax[0, 2].plot(x_axis, im(p1=p,  p2=90), color=colour[2], ls=ls[i])
    l = ax[0, 3].plot(x_axis, im(p1=p, p2=135), color=colour[3], label=deg(p), ls=ls[i])

    ax[1, 0].plot(x_axis, im(p1=0,   p2=p), color=colour[i], ls=ls[0])
    ax[1, 1].plot(x_axis, im(p1=45,  p2=p), color=colour[i], ls=ls[1])
    ax[1, 2].plot(x_axis, im(p1=90,  p2=p), color=colour[i], ls=ls[2])
    ax[1, 3].plot(x_axis, im(p1=135, p2=p), color=colour[i], ls=ls[3], label=deg(p))

ax[0, 0].set(ylabel='Intensity after P2 (au)')
ax[1, 0].set(
    ylabel='Intensity after P2 (au)', 
    xticks=np.arange(0, 181, 45), 
    xlim=[-10,190]
)
ax[0, 3].legend(title='P1', loc='upper right')
ax[1, 3].legend(title='P2', loc='upper right')

for i, p in enumerate(pp):
    ax[0, i].set(title=f'P2 = {deg(p)}')
    ax[1, i].set(title=f'P1 = {deg(p)}', xlabel='Control angle (deg)')

fig.savefig('../figures_generated/p1_effects.pdf')

# %% plot simulations
sys = lambda q1, p1, p2, theta: j.intensity(
    j.S_pol(p2) @ j.S_2(theta/2) @ j.S_4(0) @ j.S_4(q1) @ j.p_linear(p1)
)

def build_figure(q1, q2):
    pp = np.linspace(0, .75 * np.pi, 4)
    theta = np.linspace(0,np.pi)
    thetad = theta *180/np.pi
    ppd = (pp *180/np.pi).astype(int)
    
    I = [[[sys(q1, p1, p2, t) for t in theta] for p2 in pp] for p1 in pp]
    I = np.array(I)
    
    fig, ax = plt.subplots(2, 4,
        figsize=(utils.linewidth, 1.25*utils.figheight),
        sharey=True, sharex=True, gridspec_kw=dict(wspace=0.2, hspace=.5)
    )
    
    for i, (p, pd) in enumerate(zip(pp, ppd)):
        ax[0, 0].plot(thetad, I[i, 0, :], label=deg(pd), color=colour[0], ls=ls[i])
        ax[0, 1].plot(thetad, I[i, 1, :], label=deg(pd), color=colour[1], ls=ls[i])
        ax[0, 2].plot(thetad, I[i, 2, :], label=deg(pd), color=colour[2], ls=ls[i])
        ax[0, 3].plot(thetad, I[i, 3, :], label=deg(pd), color=colour[3], ls=ls[i])
        ax[1, 0].plot(thetad, I[0, i, :], label=deg(pd), color=colour[i], ls=ls[0])
        ax[1, 1].plot(thetad, I[1, i, :], label=deg(pd), color=colour[i], ls=ls[1])
        ax[1, 2].plot(thetad, I[2, i, :], label=deg(pd), color=colour[i], ls=ls[2])
        ax[1, 3].plot(thetad, I[3, i, :], label=deg(pd), color=colour[i], ls=ls[3])
        
    ax[0, 0].set(ylabel='Intensity after P2 (au)', ylim=[-.1,1.1])
    ax[1, 0].set(ylabel='Intensity after P2 (au)')
    ax[0, 3].legend(title='P1', loc='upper right', fontsize=5)
    ax[1, 3].legend(title='P2', loc='upper right', fontsize=5)
    
    for i in range(4): 
        
        ax[0, i].set_title(f'P2={deg(int(ppd[i]))}', loc='right')           
        
        ax[1, i].set_title(f'P1={deg(int(ppd[i]))}', loc='right')           
        ax[1, i].set(
            xlabel='Control angle (deg)',
            xticks=np.arange(0, 181, 45)
        )
        
    return fig, ax


fig, ax = build_figure(0, 0)
ax[0, 0].set_title('Q1=0', loc='left', fontdict=dict(fontweight='bold'))
fig.savefig('../figures_generated/p1_effects_qwp_aligned.pdf')
fig, ax = build_figure(30*np.pi/180, 0)
ax[0, 0].set_title('Q1=30', loc='left', fontdict=dict(fontweight='bold'))
fig.savefig('../figures_generated/p1_effects_qwp_30.pdf')
fig, ax = build_figure(np.pi/2, 0)
ax[0, 0].set_title('Q1=90', loc='left', fontdict=dict(fontweight='bold'))
fig.savefig('../figures_generated/p1_effects_qwp_90.pdf')

# %%
