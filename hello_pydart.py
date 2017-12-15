import pydart2 as pydart
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT
import os
from pydart2.gui.opengl.renderer import Renderer
from pydart2.gui.trackball import Trackball
from pydart2.gui.glut.window import GLUTWindow

stop = False


class Simulate:
    """ Add damping force to the skeleton """

    def __init__(self, skel, mass, friction, force):
        self.skel = skel
        print("check")
        self.count = 0
        self.mass = mass
        self.friction = friction
        self.skel.bodynodes[0].set_mass(self.mass)
        print(self.skel.bodynodes[0].mass())
        self.force = self.skel.dq * 0
        self.force[0:1] = force[0]
        self.force[1] = force[1]
        print(force)

    def compute(self):

        self.count += 1
        if self.count > 10:
            # print("check3")
            if (np.linalg.norm(abs(self.skel.dq) > 0.001)):
                # print(self.skel.bodynodes[0].mass())
                self.force = -skel.dq * self.skel.bodynodes[0].mass() * self.friction
            else:
                self.skel.set_velocities(skel.dq * 0)
        else:
            self.force *= 1
        return self.force


if __name__ == '__main__':
    pydart.init()
    world = pydart.World(0.0005, 'examples/data/skel/cube_data.skel')
    print('pydart create_world OK')
    skel = world.skeletons[-1]
    skel.friction = 0.9
    x = np.random.uniform(-1, 1)
    y = np.random.choice([1, -1]) * np.sqrt(1.0 - np.float_power(x, 2))
    force_direction = np.array([x, y]);
    skel.controller = Simulate(skel, mass=1, friction=0.4, force=10 * force_direction)
    win = GLUTWindow(world, None, frame_num=20)
    if not os.path.exists("examples/data/captures/obj1/"):
        os.makedirs("examples/data/captures/obj1/")
    win.set_filename("examples/data/captures/obj1/")
    # win.scene.set_camera(None)
    win.scene.add_camera(
        Trackball(
            rot=[-0.152, 0.045, -0.002, 0.987],
            trans=[0, 0.2, -.500]),
        "Camera Y up")
    win.scene.set_camera(2)
    win.run()
    win.run_seg()
    # pydart.gui.viewer.launch(world)
    while world.t < 2.0:

        print(world.nframes)
        if world.nframes % 100 == 0:
            stop = True
            skel = world.skeletons[-1]
            print("%.4fs: The last cube COM = %s" % (world.t, str(skel.C)))
        world.step()
