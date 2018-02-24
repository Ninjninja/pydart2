import pydart2 as pydart
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT

from pydart2.gui.opengl.renderer import Renderer
from pydart2.gui.trackball import Trackball
from pydart2.gui.glut.window import GLUTWindow
from pydart2.skeleton import Skeleton
from pydart2.bodynode import BodyNode
stop = False

class DampingController(object):
    """ Add damping force to the skeleton """
    def __init__(self, skel):
        self.skel = skel

    def compute(self):
        # print(self.skel.q)
        damping = -self.skel.q *0
        # damping[-1] = 10
        # damping[1::3] *= 0.1
        bod = skel.root_bodynode()
        # bod.add_ext_force(np.array([0, 0, 2]), np.array([0, 0, 0]))
        return damping

if __name__ == '__main__':
    print('Hello, PyDART!')

    pydart.init()
    print('pydart initialization OK')

    world = pydart.World(0.0005,'examples/data/skel/cube_data.skel')
    skel = world.skeletons[-1]
    bod = skel.root_bodynode()
    bod.add_ext_force(np.array([0, 0, 400]), np.array([0, 0, 0]))
    # bod.add_ext_force(np.array([100, 0, 100]), np.array([0, 0, 0]))
    # skel.q = np.random.rand(skel.ndofs) - 0.5
    # skel.set_mobile(True)
    # world.set_gravity([0, 9.8, 0])
    win = GLUTWindow(world, None)
    # win.scene.set_camera(None)
    win.scene.add_camera(
        Trackball(
            rot=[-0.152, 0.045, -0.002, 0.987],
            trans=[0, 0.2, -.500]),
        "Camera Y up")
    win.scene.set_camera(2)
    skel.controller = DampingController(skel)
    print(skel.ndofs)
    win.run()

    # pydart.gui.viewer.launch(world)

