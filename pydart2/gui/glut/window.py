import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT
import sys
import numpy as np
from pydart2.gui.opengl.scene import OpenGLScene

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.


class GLUTWindow(object):
    def __init__(self, sim, title,frame_num):
        self.sim1 = sim
        self.sim = sim
        self.title = title if title is not None else "GLUT Window"
        self.window_size = (1280, 720)
        self.scene = OpenGLScene(*self.window_size)
        self.frame_num = frame_num
        self.mouseLastPos = None
        self.is_simulating = True
        self.is_animating = False
        self.frame_index = 0
        self.capture_index = 0
        self.folder_name = "examples/data/captures/"
        self.stop = 0

    def set_filename(self,folder_name):
        self.folder_name = folder_name

    def initGL(self, w, h):
        self.scene.init()

    def resizeGL(self, w, h):
        self.scene.resize(w, h)

    def drawGL_seg(self, ):

        GL.glDisable(GL.GL_LIGHTING)
        GL.glColor3f(0.0, 0.0, 1.0)
        self.scene.render(self.sim)
        # GLUT.glutSolidSphere(0.3, 20, 20)  # Default object for debugging
        GLUT.glutSwapBuffers()

    def drawGL(self, ):

        self.scene.render(self.sim)
        # GLUT.glutSolidSphere(0.3, 20, 20)  # Default object for debugging
        GLUT.glutSwapBuffers()
        if self.frame_num==self.capture_index:
            return

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
        if self.capture_index == self.frame_num:
            return
        else:
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
        filename = self.folder_name+"capture%04d.png" % self.capture_index
        img.save(filename, 'png')
        self.capture_index += 1
        if self.capture_index == self.frame_num:
            GLUT.glutDestroyWindow(self.window)
            #self.close()
            return
            #self.run_seg()
            #sys.exit()
        else:
            GLUT.glutTimerFunc(100, self.capture, 1)

    def capture_seg(self,timer):
        print("capture! index seg= %d" % self.capture_index)
        from PIL import Image
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        w, h = 1280, 720
        data = GL.glReadPixels(0, 0, w, h, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        img = Image.frombytes("RGBA", (w, h), data)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        filename = self.folder_name+"capture_seg%04d.png" % self.capture_index
        img.save(filename, 'png')
        #self.capture_index += 1
        if self.frame_num == self.capture_index:
            GLUT.glutDestroyWindow(self.window)
            #sys.exit()

        GLUT.glutTimerFunc(100, self.capture_seg, 1)

    def close(self):
        self.stop = 1
        GLUT.glutLeaveMainLoop()

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
        GLUT.glutWMCloseFunc(self.close)
        GLUT.glutIdleFunc(self.idle)
        GLUT.glutReshapeFunc(self.resizeGL)
        GLUT.glutKeyboardFunc(self.keyPressed)
        GLUT.glutMouseFunc(self.mouseFunc)
        GLUT.glutMotionFunc(self.motionFunc)
        GLUT.glutTimerFunc(25, self.renderTimer, 1)
        GLUT.glutTimerFunc(100, self.capture, 1)

        GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
                           GLUT.GLUT_ACTION_CONTINUE_EXECUTION)
        GLUT.glutSetOption(GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS,
                           GLUT.GLUT_ACTION_CONTINUE_EXECUTION)


        self.initGL(*self.window_size)

        # Run
        while not self.stop:
            GLUT.glutCheckLoop()
        #GLUT.glutMainLoop()
        a = 5+6
        print("exited")

    def run_seg(self, ):
        self.sim = self.sim1
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
        GLUT.glutDisplayFunc(self.drawGL_seg)
        GLUT.glutIdleFunc(self.idle)
        GLUT.glutReshapeFunc(self.resizeGL)
        GLUT.glutKeyboardFunc(self.keyPressed)
        GLUT.glutMouseFunc(self.mouseFunc)
        GLUT.glutMotionFunc(self.motionFunc)
        GLUT.glutTimerFunc(25, self.renderTimer, 1)
        GLUT.glutTimerFunc(100, self.capture_seg, 1)
        self.initGL(*self.window_size)

        # Run
        GLUT.glutMainLoop()
