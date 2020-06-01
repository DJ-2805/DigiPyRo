import numpy as np

g = 9.817

def position(t, omega, u0, v0, x0):
    """Finds position of puck on paraboloid. The equations come from
    Cushman-Roisin Chapter 2, in particular, 2.17a, and 2.17b.

    Keyword arguments:
    t     -- float, time of given moment
    omega -- float, effective rotation
    u0    -- float, initial x-component of the velocity [cm/s]
    v0    -- float, initial y-component of the velocity [cm/s]
    x0    -- float, initial x-component of the position [m]

    Returns:
    x -- float, x-component of the position [m]
    y -- float, y-component of the position [m]
    z -- float, z-component of the position [m]
    """
    ot = omega * t

    x = x0*np.cos(ot) + u0/omega*np.sin(ot)
    y = v0/omega*np.sin(ot)
    z = omega**2/(2*g)*(x**2 + y**2)

    return x, y, z

def circle(r):
    """Creates circle that represents edge of the paraboloid.

    Keyword arguments:
    r -- float, radius of the circle

    Returns:
    xc -- array(float); x-values of the circle
    yc -- array(float); y-values of the circle
    """
    twopi = 2 * np.pi

    k = np.arange(1, 102)
    xc = r * np.cos(k * twopi / 100)
    yc = r * np.sin(k * twopi / 100)

    return xc, yc

def parabola(r, omega):
    """Creates parabola that represents the sides of the paraboloid.

    Keyword arguments:
    r -- float, radius of the paraboloid
    omega -- float, effective rotation

    Returns:
    s -- array(float), x-values that make up parabola
    z -- array(float), z-values that make up parabola
    """

    s = np.linspace(start=-r,stop=r)
    z = omega**2/(2*g)*s**2

    return s, z

def checkEdge(x, y, r):
    """Checks if puck is off the edge of the paraboloid.

    Keyword arguments:
    x -- float, x-component of the position of the puck
    y -- float, y-component of the position of the puck
    r -- float, radius of the circle

    Returns:
    offEdge -- bool, True if puck crossed the radius of the paraboloid
    """
    offEdge = False

    if(r > np.sqrt(x**2 + y**2)):
        offEdge = True

    return offEdge
