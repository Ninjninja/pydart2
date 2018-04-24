import pydart2 as pydart
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT

from pydart2.gui.opengl.renderer import Renderer
from pydart2.gui.trackball import Trackball
from pydart2.gui.glut.window import GLUTWindow
stop = False

if __name__ == '__main__':
    print('Hello, PyDART!')

    pydart.init()
    print('pydart initialization OK')

    world = pydart.World(0.0005, 'examples/data/skel/arti_data.skel')
    #world.set_gravity([0, -9.8, 0])
    print('pydart create_world OK')
    # pydart.gui.viewer.launch(world)
    skel = world.skeletons[-1]
    bod = skel.root_bodynode()
    bod.add_ext_force(np.array([0,0,1400]))
    # skel.friction = 0.9
    #skel.q = (np.random.rand(skel.ndofs))
    # skel.set_forces(np.array([0, 0, 100, 100, 0, 0]))
    #skel.set_accelerations([0, 5, 0])
    #print(skel.tau)
    #print(skel.friction)
    # skel.controller = ApplyForce(skel)
    win = GLUTWindow(world, None)
    # win.scene.set_camera(None)
    win.scene.add_camera(
        Trackball(
            rot=[-0.152, 0.045, -0.002, 0.987],
            trans=[0, 0.2, -.500]),
        "Camera Y up")
    win.scene.set_camera(2)
    # skel.bodynodes[0].set_mass(1)
    win.run()

