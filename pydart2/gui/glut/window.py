import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT
import sys
import time
import cv2 as cv
import numpy as np
from pydart2.gui.opengl.scene import OpenGLScene
import os
EPSILON = sys.float_info.epsilon
# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
np.random.seed(int(133))

class Simulate:
    """ Add damping force to the skeleton """

    def __init__(self, skel, mass, friction, force):
        self.skel = skel
        #print("check")
        self.count = 0
        self.mass = mass
        self.friction = friction
        self.skel.bodynodes[0].set_mass(self.mass)
        print(self.skel.bodynodes[0].mass())
        self.force = self.skel.dq * 0
        self.force[0:1] = force[0]
        self.force[1] = force[1]
        #print(force)

    def compute(self):

        self.count += 1
        if self.count > 50:
            # print("check3")
            mask = self.skel.dq * 0 + 1
            mask[abs(self.skel.dq) < 0.001] = 0
            self.skel.set_velocities(np.multiply(self.skel.dq, mask))
            #self.skel.dq[self.skel.dq > 10] = 0
            # print(self.skel.bodynodes[0].mass())
            self.force = - self.skel.dq * self.skel.bodynodes[0].mass() * self.friction
            self.skel.set_velocities(np.multiply(self.skel.dq, mask))
            #print(self.skel.dq, self.force)
                #self.skel.set_velocities(self.skel.dq * 0)
                #self.force = [0, 0, 0]

        else:
            self.force *= 1
        return self.force

    def reset(self, mass, friction, force):
        self.count = 0
        self.mass = mass
        self.friction = friction
        self.skel.bodynodes[0].set_mass(self.mass)
        print(self.skel.bodynodes[0].mass())
        self.force = self.skel.dq * 0
        self.force[0:1] = force[0]
        self.force[1] = force[1]


class GLUTWindow(object):
    def __init__(self, sim, title,frame_num,filename1,filename2):
        # self.sim1 = deepcopy(sim)
        for root, dirs, files in os.walk('/home/niranjan/Projects/datasets/ETH_Synthesizability/texture',
                                         topdown=False):
            pass
        self.root = root
        self.files = files
        self.simulation_num = 0
        self.sim = sim
        self.skel = self.sim.skeletons[-1]
        self.loc = self.skel.q
        self.set_parm()
        self.skel.controller = Simulate(self.skel, mass=self.parm['mass'], friction=self.parm['friction'], force=self.parm['force'])
        self.render = False
        #self.skel.render_with_color([0.5, 0.5, 0.5])

        self.title = title if title is not None else "GLUT Window"
        self.window_size = (1280, 720)
        self.scene = OpenGLScene(*self.window_size)
        self.frame_num = frame_num
        self.mouseLastPos = None
        self.is_simulating = True
        self.is_animating = False
        self.frame_index = 0
        self.capture_index = 0
        self.folder_name = "/home/niranjan/Projects/datasets/push_tex/"
        self.stop = 0
        self.seg_mode = 0
        self.filename1 = filename1
        self.filename2 = filename2

    def set_parm(self):
        self.simulation_num += 1
        loc = np.random.normal(0, 0.1s, 3)
        loc[2] = self.loc[2]
        self.skel.set_positions(loc)
        x = np.random.uniform(-1, 1)
        y = np.random.choice([1, -1]) * np.sqrt(1.0 - np.float_power(x, 2))
        force_direction = np.array([x, y])
        m = np.random.uniform(0.2, 3)
        self.filename2 = os.path.join(self.root, self.files[np.random.randint(len(self.files))])
        self.filename1 = os.path.join(self.root, self.files[np.random.randint(len(self.files))])
        if hasattr(self, 'scene'):
            print('Entered')
            self.scene.set_textures(self.filename1, self.filename2)
        force = 10 * force_direction
        self.parm = {'mass': m, 'friction': 0.7, 'force': force}

    def convert_to_rgb(self, minval, maxval, val, colors):
        fi = float(val - minval) / float(maxval - minval) * (len(colors) - 1)
        i = int(fi)
        f = fi - i
        if f < EPSILON:
            return colors[i]
        else:
            (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i + 1]
            return int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))

    def set_filename(self,folder_name):
        self.folder_name = folder_name

    def initGL(self, w, h):
        self.scene.init()
        self.scene.set_textures(self.filename1, self.filename2)

    def resizeGL(self, w, h):
        self.scene.resize(w, h)

    def drawGL(self, ):
        # print(self.seg_mode)
        if self.seg_mode == 0:
            GL.glEnable(GL.GL_LIGHTING)
            self.scene.render(self.sim)
            #GL.glTranslated(0.0, 0, -1)
            #GL.glColor3f(0.0, 0.0, 1.0)

           # GLUT.glutSolidSphere(0.02, 20, 20)  # Default object for debugging
            #GL.glTranslated(0.0, 0, -1)
            #self.scene.renderer.draw_image(0, 0)
            # GLUT.glutSwapBuffers()
            GL.glFinish()
            # if self.frame_num == self.capture_index:
            #     return
        else:
            GL.glDisable(GL.GL_LIGHTING)
            #GL.glColor3f(0.0, 0.0, 1.0)
            self.scene.render_seg(self.sim)
            # GLUT.glutSolidSphere(0.3, 20, 20)  # Default object for debugging
            # GLUT.glutSwapBuffers()
            GL.glFinish()
        if self.render:
            self.render = False
            GLUT.glutTimerFunc(100, self.record_frames, 1)

    # The function called whenever a key is pressed.
    # Note the use of Python tuples to pass in: (key, x, y)
    def keyPressed(self, key, x, y):

        keycode = ord(key)
        key = key.decode('utf-8')
        # print("key = [%s] = [%d]" % (key, ord(key)))

        # n = sim.num_frames()
        if keycode == 27:
            GLUT.glutDestroyWindow(self.window)
            sys.exit()
        elif key == ' ':
            self.is_simulating = not self.is_simulating
            self.is_animating = False
            print("self.is_simulating = %s" % self.is_simulating)
        elif key == 'a':
            self.is_animating = not self.is_animating
            self.is_simulating = False
            print("self.is_animating = %s" % self.is_animating)
        elif key == '1':
            self.is_simulating = False
            self.is_animating = False
            self.frame_index = 1
            print (self.frame_index)
            self.sim.set_frame(self.frame_index)
        elif key == '2':
            self.is_simulating = False
            self.is_animating = False
            self.frame_index = self.sim.num_frames()-1
            print(self.frame_index)
            self.sim.set_frame(self.frame_index)
        elif key == ']':
            self.frame_index = (self.frame_index + 1) % self.sim.num_frames()
            print("frame = %d/%d" % (self.frame_index, self.sim.num_frames()))
            if hasattr(self.sim, "set_frame"):
                self.sim.set_frame(self.frame_index)
        elif key == '[':
            self.frame_index = (self.frame_index - 1) % self.sim.num_frames()
            print("frame = %d/%d" % (self.frame_index, self.sim.num_frames()))
            if hasattr(self.sim, "set_frame"):
                self.sim.set_frame(self.frame_index)
        elif key == 'c':
            self.capture()

    def mouseFunc(self, button, state, x, y):
        if state == 0:  # Mouse pressed
            self.mouseLastPos = np.array([x, y])
        elif state == 1:
            self.mouseLastPos = None

    def motionFunc(self, x, y):
        dx = x - self.mouseLastPos[0]
        dy = y - self.mouseLastPos[1]
        modifiers = GLUT.glutGetModifiers()
        tb = self.scene.tb
        if modifiers == GLUT.GLUT_ACTIVE_SHIFT:
            tb.zoom_to(dx, -dy)
        elif modifiers == GLUT.GLUT_ACTIVE_CTRL:
            tb.trans_to(dx, -dy)
        else:
            tb.drag_to(x, y, dx, -dy)
        self.mouseLastPos = np.array([x, y])

    def idle(self, ):
        if self.sim is None:
            return
        if self.is_simulating:
            self.sim.step()

            # if self.sim.frame % 10 == 0:
            #     self.capture()
        elif self.is_animating:
            self.frame_index = (self.frame_index + 1) % self.sim.num_frames()
            if hasattr(self.sim, "set_frame"):
                self.sim.set_frame(self.frame_index)


    def renderTimer(self, timer):
        # if self.capture_index == self.frame_num:
        #     return
        # else:
            GLUT.glutPostRedisplay()
            GLUT.glutTimerFunc(20, self.renderTimer, 1)


    def capture(self, timer):
        print("capture! index = %d" % self.capture_index)
        from PIL import Image
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        w, h = 1280, 720
        data = GL.glReadPixels(0, 0, w, h, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        img = Image.frombytes("RGBA", (w, h), data)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        if self.seg_mode == 0:
            filename = self.folder_name+"_A%01d.png" % self.capture_index
            img.save(filename, 'png')
            if self.capture_index == self.frame_num:
                self.run_seg()
                return
            GLUT.glutTimerFunc(5000, self.capture, 1)
        else:
            mass = self.skel.bodynodes[0].mass()*50
            cimg = np.array(img)
            idx = cimg[:, :, 0] < 100
            r, g, b = self.rgb(1, 3, mass)
            cimg[idx, 0] = r
            cimg[idx, 1] = g
            cimg[idx, 2] = b
            cimg[~idx, 0] = 0
            cimg[~idx, 1] = 0
            cimg[~idx, 2] = 0
            img = Image.fromarray(cimg)
            filename = self.folder_name + "_B%01d.png" % self.capture_index
            img.save(filename, 'png')
            sys.exit(1)
            if self.capture_index == self.frame_num:
                GLUT.glutDestroyWindow(self.window)
                 #print("done")'
            else:
                GLUT.glutTimerFunc(5000, self.capture, 1)
        self.capture_index += 1
        # if self.capture_index == self.frame_num:
            #GLUT.glutDestroyWindow(self.window)
            #self.close()
            #return
            # self.run_seg()
            #sys.exit()
        # else:

    def capture2(self):
        print("capture! index = %d" % self.capture_index)
        from PIL import Image
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        w, h = 1280, 720
        data = GL.glReadPixels(0, 0, w, h, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        img = Image.frombytes("RGBA", (w, h), data)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        if self.seg_mode == 0:
            print('normal capture')
            filename = self.folder_name+"_A%01d.png" % self.capture_index
            # img.save(filename, 'png')
            if self.capture_index == self.frame_num:
                self.image2 = img
                self.run_seg()
                return
            self.image1 = img
            #GLUT.glutTimerFunc(5000, self.capture, 1)
            self.capture_index += 1
            #self.capture2()
            return
        else:
            print('seg_capture')
            mass = self.skel.bodynodes[0].mass()
            cimg = np.array(img)
            idx = cimg[:, :, 0] < 100
            colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
            r, g, b = self.convert_to_rgb(0.2, 3, mass, colors)
            cimg[idx, 0] = r
            cimg[idx, 1] = g
            cimg[idx, 2] = b
            cimg[~idx, 0] = 0
            cimg[~idx, 1] = 0
            cimg[~idx, 2] = 0
            img = Image.fromarray(cimg)
            filename = "%01d.png" % self.simulation_num
            # img.save(filename, 'png')
            self.image3 = img
            imgf = Image.fromarray(np.concatenate((np.asarray(self.image1), np.asarray(self.image2), np.asarray(self.image3)), 1))
            imgf = imgf.resize((256*3, 256), Image.ANTIALIAS)
            imgf.save(os.path.join(self.folder_name, filename), 'png')
            self.seg_mode = 0
            print('got_seg')
            # self.skel.set_positions(self.loc)


            # GLUT.glutDestroyWindow(self.window)
            #sys.exit(1)
            # if self.capture_index == self.frame_num:
            #     # GLUT.glutDestroyWindow(self.window)
            #     print('done')
            # else:
            #     GLUT.glutTimerFunc(5000, self.capture, 1)

        # if self.capture_index == self.frame_num:
            #GLUT.glutDestroyWindow(self.window)
            #self.close()
            #return
            # self.run_seg()
            #sys.exit()
        # else:

    def close(self):
        self.stop = 1
        GLUT.glutLeaveMainLoop()

    def record_frames(self,timer):
        print(self.frame_index)
        self.is_simulating = False
        self.is_animating = False
        if not self.frame_index == 1 and self.seg_mode == 0:
            print("check..1")
            self.capture2()
            self.frame_index = 1
            print(self.frame_index)
            self.sim.set_frame(self.frame_index)
            self.render = True
            # GLUT.glutTimerFunc(100, self.record_frames, 1)
            return
        if self.seg_mode == 1:
            print("check..2")
            self.capture2()
            # self.frame_index = self.sim.num_frames()
            self.frame_index = 1
            self.sim.set_frame(self.frame_index)
            self.skel.set_velocities(self.loc*0)
            self.sim.reset()
            self.set_parm()
            self.skel.controller.reset(mass=self.parm['mass'], friction=self.parm['friction'], force=self.parm['force'])
            self.is_simulating = True
            self.is_animating = True
            self.seg_mode = 0
            # self.is_simulating = True
            # self.is_animating = True
            GLUT.glutTimerFunc(1000, self.record_frames, 1)
            print('waiting for capture')
        else:
            print("check..3")
            self.capture2()
            # self.frame_index = self.sim.num_frames()
            self.frame_index = 1
            self.sim.set_frame(self.frame_index)
            self.render = True
            # GLUT.glutTimerFunc(200, self.record_frames, 1)

    def run(self, ):
        print("\n")
        print("space bar: simulation on/off")
        print("' ': run/stop simulation")
        print("'a': run/stop animation")
        print("'[' and ']': play one frame backward and forward")

        # Init glut
        GLUT.glutInit(())
        GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA |
                                 GLUT.GLUT_DOUBLE |
                                 GLUT.GLUT_MULTISAMPLE |
                                 GLUT.GLUT_ALPHA |
                                 GLUT.GLUT_DEPTH)

        GLUT.glutInitWindowSize(*self.window_size)
        GLUT.glutInitWindowPosition(0, 0)
        self.window = GLUT.glutCreateWindow(self.title)

        # Init functions
        # glutFullScreen()
        GLUT.glutDisplayFunc(self.drawGL)
        # GLUT.glutWMCloseFunc(self.close)
        GLUT.glutIdleFunc(self.idle)
        GLUT.glutReshapeFunc(self.resizeGL)
        GLUT.glutKeyboardFunc(self.keyPressed)
        GLUT.glutMouseFunc(self.mouseFunc)
        GLUT.glutMotionFunc(self.motionFunc)
        GLUT.glutTimerFunc(1, self.renderTimer, 1)
        GLUT.glutTimerFunc(2000, self.record_frames, 1)
        #
        # GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
        #                    GLUT.GLUT_ACTION_CONTINUE_EXECUTION)
        # GLUT.glutSetOption(GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS,
        #                    GLUT.GLUT_ACTION_CONTINUE_EXECUTION)


        self.initGL(*self.window_size)

        # Run
        # while not self.stop:
        #     GLUT.glutCheckLoop()
        GLUT.glutMainLoop()

    def run_seg(self, ):
        self.capture_index = 0
        # self.sim = deepcopy(self.sim1)
        #self.skel.q = self.loc
        # self.skel.set_positions(self.loc)
        self.seg_mode = 1
        print("seg mode on")
        # print("space bar: simulation on/off")
        # print("' ': run/stop simulation")
        # print("'a': run/stop animation")
        # print("'[' and ']': play one frame backward and forward")
        #GLUT.glutTimerFunc(100, self.capture, 1)
        # # Init glut
        # GLUT.glutInit(())
        # GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA |
        #                          GLUT.GLUT_DOUBLE |
        #                          GLUT.GLUT_MULTISAMPLE |
        #                          GLUT.GLUT_ALPHA |
        #                          GLUT.GLUT_DEPTH)
        #
        # GLUT.glutInitWindowSize(*self.window_size)
        # GLUT.glutInitWindowPosition(0, 0)
        # self.window = GLUT.glutCreateWindow(self.title)
        #
        # # Init functions
        # # glutFullScreen()
        # GLUT.glutDisplayFunc(self.drawGL_seg)
        # GLUT.glutIdleFunc(self.idle)
        # GLUT.glutReshapeFunc(self.resizeGL)
        # GLUT.glutKeyboardFunc(self.keyPressed)
        # GLUT.glutMouseFunc(self.mouseFunc)
        # GLUT.glutMotionFunc(self.motionFunc)
        # GLUT.glutTimerFunc(25, self.renderTimer, 1)
        # GLUT.glutTimerFunc(100, self.capture_seg, 1)
        # self.initGL(*self.window_size)

        # Run