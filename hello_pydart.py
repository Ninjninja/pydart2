import pydart2 as pydart
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT

from pydart2.gui.opengl.renderer import Renderer
from pydart2.gui.trackball import Trackball
from pydart2.gui.glut.window import GLUTWindow
stop = False


class ApplyForce:
    """ Add damping force to the skeleton """

    def __init__(self, skel):
        self.skel = skel
        print("check")
        self.count = 0

    def compute(self):
        damping = skel.dq*0
        # print (skel.dq)
        # if skel.dq[1]>0.3:
        #     skel.set_mobile(False)
        self.count += 1
        if self.count > 10:
            print("check3")
            if(np.linalg.norm(skel.dq>0.001)):
                damping = -skel.dq*skel.bodynodes[0].mass()*0.4
            else:
                skel.set_velocities(skel.dq*0)
        else:
            #skel.set_mobile(True)
           # print("check2")
            damping[1] = 9.8
        return damping


if __name__ == '__main__':
    print('Hello, PyDART!')

    pydart.init()
    print('pydart initialization OK')

    world = pydart.World(0.0005, 'examples/data/skel/cube_data.skel')
    #world.set_gravity([0, -9.8, 0])
    print('pydart create_world OK')
    # pydart.gui.viewer.launch(world)
    skel = world.skeletons[-1]
    skel.friction = 0.9
    #skel.q = (np.random.rand(skel.ndofs))
    #skel.set_forces(np.array([0, 0, 0, 100, 0, 0]))
    #skel.set_accelerations([0, 5, 0])
    #print(skel.tau)
    #print(skel.friction)
    skel.controller = ApplyForce(skel)
    win = GLUTWindow(world, None)
    # win.scene.set_camera(None)
    win.scene.add_camera(
        Trackball(
            rot=[-0.152, 0.045, -0.002, 0.987],
            trans=[0, 0.2, -.500]),
        "Camera Y up")
    win.scene.set_camera(2)
    skel.bodynodes[0].set_mass(1)
    print(skel.q)
    win.run()

    pydart.gui.viewer.launch(world)
    while world.t < 2.0:

        print(world.nframes)
        if world.nframes % 100 == 0:
            stop = True
            skel = world.skeletons[-1]
            print("%.4fs: The last cube COM = %s" % (world.t, str(skel.C)))
        world.step()
