import numpy as np

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