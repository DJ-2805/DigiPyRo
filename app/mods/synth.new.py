# libraries
import argparse as ap                       # command line lib
import paraboloid as pbd                    # paraboloid lib, paraboloid.py
import numpy as np                          # numerical lib
import matplotlib.pyplot as plt             # plotting lib
import matplotlib.animation as animate      # animation lib

# sets plots to a darker color scheme
plt.style.use("dark_background")
#------------------------------------------------------------------------------
# *** COMMAND LINE INTERFACE SETUP ***
# initial message for program
msg = """ This program creates a synthetic .mp4 movie for use with DigiPyRo.
The video shows a puck sliding on a parabolic surface. The user may change several variables of the puck, and observe the animation in the output"""

parser = ap.ArgumentParser(description = msg,
                           formatter_class=ap.ArgumentDefaultsHelpFormatter)

# collecting arguments for the user to change
parser.add_argument('-t', '--time', type=float, default=5,
                    help='The length of the movie in seconds.')

parser.add_argument('-o', '--omega', type=float, default=3,
                    help=('The deflection of a stationary paraboloid surface '
                          'as if it were an equipotential in a system '
                          'rotating at the specified rate. '
                          'A good value would be between 5 and 15.'))

parser.add_argument('-u', '--u0', type=float, default=0,
                    help=('The initial x-velocity of the puck moving on the '
                          'parabolic surface. If too high, the puck will go '
                          'off the edge during the animation.'))

parser.add_argument('-v', '--v0', type=float, default=0,
                    help=('The initial y-velocity of the puck moving on the '
                          'parabolic surface. If too high, the puck will go '
                          'off the edge during the animation.'))

parser.add_argument('-x', '--x0', type=float, default=1,
                    help=('The initial x-position of the puck moving on the '
                          'parabolic surface. If too high, the puck will go '
                          'off the edge during the animation.'))

parser.add_argument('-r', '--radius', type=float, default=2,
                    help='The radius of the paraboloid')

parser.add_argument('-n', '--name', type=str, default="movie.mp4",
                    help="Title of the movie that will be outputted.")

parser.add_argument('-s', '--switch', type=int, default=0,
                    help=('Choice to either show the animation or save it. '
                          'Default displays the animation. Option [1] will '
                          'save the animation as an mp4.'))

# collecting user input into list
args = parser.parse_args()

time = args.time
omega = args.omega
u0 = args.u0
v0 = args.v0
x0 = args.x0
radius = args.radius
name = args.name
switch = args.switch

def animate_paraboloid(time, omega, u0, v0, x0, radius):
    """Animates the paraboloid.

    Keyword arguments:
    time  -- float, length of animation in seconds
    omega -- float, effective rotation
    u0    -- float, initial x-component of the velocity
    v0    -- float, initial y-component of the velocity
    x0    -- float, initial x-component of the position

    Returns:
    animation -- Obj, animation object
    NOTE: reference matplotlib.animation.funcAnimation for more info.
    """

    # creating circle
    circle = pbd.circle(radius)
    parabola = pbd.parabola(radius, omega)

    # size of plots based off paraboloid radius
    rmax = radius*1.5
    size = (-1*(rmax), rmax)

    # creating figure and plots
    fig, (a0, a1) = plt.subplots(2, 1, figsize=(6,8),
                                 gridspec_kw={'height_ratios': [3,1]})
    # a0 plots out the top-view of the paraboloid
    a0.set_xlim(size)
    a0.set_ylim(size)
    a0.plot(circle[0], circle[1], color='white')
    a0.grid(color='grey')

    puckTop, = a0.plot([], [], linestyle='none',
                    marker='o', mfc='white', mec='red')

    # a1 plots out the side-view of the paraboloid
    a1.set_xlim(size)
    a1.plot(parabola[0], parabola[1], color='white')
    a1.grid(color='grey')

    puckSide, = a1.plot([], [], linestyle='none',
                        marker='o', mfc='white', mec='red')

    fps = 30
    t = np.linspace(start=0, stop=time, num=int(time*fps))
    frames = len(t)
    x, y, z = pbd.position(t, omega, u0, v0, x0)

    def init():
        """Initialization function for the animation."""
        return puckTop, puckSide

    def animation_frame(i):
        """Specific frame of that animation."""
        xpos = x[i]
        ypos = y[i]
        zpos = z[i]

        puckTop.set_data(xpos, ypos)
        puckSide.set_data(xpos, zpos)

        return puckTop, puckSide

    animation = animate.FuncAnimation(fig,
                                      init_func=init,
                                      func=animation_frame,
                                      frames=frames)
    return animation

def save_animation(animation, name):
    """Saves animation when called."""
    animation.save(name, writer='ffmpeg', fps=30, dpi=200)

if __name__ == "__main__":
    animation = animate_paraboloid(time, omega, u0, v0, x0, radius)

    if switch == 0:
        plt.show()
    elif switch == 1:
        save_animation(animation, name)
