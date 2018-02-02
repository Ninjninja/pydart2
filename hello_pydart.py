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


def get_frames():
    pydart.init()
    world = pydart.World(0.001, 'examples/data/skel/cube_data.skel')
    print('pydart create_world OK')
    win = GLUTWindow(world, None, frame_num=1)
    #if not os.path.exists("examples/data/captures/obj"+str(obj_num)+"_"+force_name+"_"):
    #    os.makedirs("examples/data/captures/obj"+str(obj_num)+"_"+force_name+"_")
    # win.set_filename("examples/data/captures/obj"+str(obj_num)+"_"+force_name+"_")
    # win.scene.set_camera(None)
    win.scene.add_camera(
        Trackball(
            rot=[-0.452, 0.045, -0.002, 0.987],
            trans=[0, 0.2, -1.500]),
        "Camera Y up")
    win.scene.set_camera(2)
    win.run()
    #win.run_seg()



if __name__ == '__main__':
    get_frames()

