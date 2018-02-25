import pydart2 as pydart
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT
import os
from pydart2.gui.opengl.renderer import Renderer
from pydart2.gui.trackball import Trackball
from pydart2.gui.glut.window import GLUTWindow
import atexit
import sys
stop = False

class TexWorld(pydart.World):
    def __init__(self,dt,skel_path=None):
        super(TexWorld, self).__init__(dt,skel_path)
        self.force = None
        self.offset = None
        self.contact_point = None
        self.set_text = None
        self.duration = 0

    def set_skel(self, skel):
        self.skeleton = skel

    def step(self,):
        super(TexWorld,self).step()

    def add_force(self, force, offset):
        self.offset = np.asarray(offset)
        self.force = np.asarray(force)

    def set_contact(self,point):
        self.contact_point = point

    def text(self, text):
        self.set_text = text

    def render_with_ri(self, ri):

        if self.force is not None:
            p0 = self.skeleton.bodynodes[0].C + self.offset + np.array([-0.05, 0, 0])
            # print(p0)
            p1 = p0 - 0.050 * self.force
            ri.set_color(1.0, 0.0, 0.0)
            ri.render_arrow(p1, p0, r_base=0.002, head_width=0.004, head_len=0.02)

        if self.contact_point is not None:
            ri.set_color(1.0, 0.0, 0.0)
            ri.render_sphere(self.contact_point, 0.01)

        if self.set_text is not None:
            ri.draw_text(self.set_text)

def get_frames():
    pydart.init()
    world = pydart.World(0.0005, 'examples/data/skel/arti_data.skel')
    skel = world.skeletons[-1]
    bod = skel.root_bodynode()
    bod.add_ext_force(np.array([0, 0, 10000]), np.array([0, 0, 0]))

    # world = pydart.World(0.001, 'examples/data/skel/cube_data.skel')
    # skel = world.skeletons[-1]
    skel.set_mobile(True)
    # bod = skel.root_bodynode()
    #
    # bod.add_ext_force(np.array([900, 0, 900]),np.array([0.015*0, 0, 0.01*0]))
    # skel.tau = (np.array([0, 1, 0, 0, 0, 100]))
    # world.set_skel(skel)
    # world.add_force([1, 0, 1], [0.00, 0.00, 0.00])
    print('pydart create_world OK')
    win = GLUTWindow(world, None, frame_num=1)
    #if not os.path.exists("examples/data/captures/obj"+str(obj_num)+"_"+force_name+"_"):
    #    os.makedirs("examples/data/captures/obj"+str(obj_num)+"_"+force_name+"_")
    # win.set_filename("examples/data/captures/obj"+str(obj_num)+"_"+force_name+"_")
    # win.scene.set_camera(None)
    win.scene.add_camera(
        Trackball(
            rot=[-0.452, 0.045, -0.002, 0.987],
            trans=[0, 0.2, -.100]),
        "Camera Y up")
    win.scene.set_camera(2)
    win.run()
    #win.run_seg()



if __name__ == '__main__':
    get_frames()

