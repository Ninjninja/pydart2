import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT
from PIL import Image
from pydart2.gui.opengl.renderer_split import Renderer1
from pydart2.gui.trackball import Trackball
from pydart2.gui.opengl.scene import OpenGLScene

class OpenGLScene_split(OpenGLScene):
    def __init__(self, width, height, window=None):
        super().__init__(width,height,window)
        self.renderer = Renderer1()

    def init(self):
        # GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        # GL.glClearDepth(1.0)
        # GL.glDepthFunc(GL.GL_LEQUAL)
        # GL.glEnable(GL.GL_DEPTH_TEST)
        # GL.glShadeModel(GL.GL_SMOOTH)
        # GL.glMatrixMode(GL.GL_PROJECTION)
        # GL.glLoadIdentity()
        # GL.gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
        # GL.glMatrixMode(GL.GL_MODELVIEW)
        self.disable2D()
        GL.glDisable(GL.GL_CULL_FACE)
        # GL.glEnable(GL.GL_DEPTH_TEST)

        # GL.glDepthFunc(GL.GL_LEQUAL)
        GL.glHint(GL.GL_PERSPECTIVE_CORRECTION_HINT, GL.GL_NICEST)

        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
        # GlEnable(GL.GL_POLYGON_SMOOTH)
        GL.glHint(GL.GL_POLYGON_SMOOTH_HINT, GL.GL_NICEST)

        GL.glEnable(GL.GL_DITHER)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glHint(GL.GL_PERSPECTIVE_CORRECTION_HINT, GL.GL_NICEST)

        GL.glClearColor(1.0, 1.0, 1.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LEQUAL)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_NORMALIZE)

        GL.glColorMaterial(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE)
        GL.glEnable(GL.GL_COLOR_MATERIAL)

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_MULTISAMPLE)
        # GLUT.glutSetOption(GLUT.GLUT_MULTISAMPLE, 4)

        # glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

        ambient = [0.2, 0.2, 0.2, 1.0]
        diffuse = [0.6, 0.6, 0.6, 1.0]
        front_mat_shininess = [60.0]
        front_mat_specular = [0.2, 0.2, 0.2, 1.0]
        front_mat_diffuse = [0.5, 0.28, 0.38, 1.0]
        lmodel_ambient = [0.2, 0.2, 0.2, 1.0]
        lmodel_twoside = [GL.GL_FALSE]

        # position = [1.0, 1.0, 1.0, 0.0]
        # position1 = [-1.0, 1.0, 0.0, 0.0]

        position = [1.0, 1.0, 0.0, 0.0]
        position1 = [-1.0, 0.0, 0.0, 0.0]

        GL.glEnable(GL.GL_LIGHT0)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, ambient)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, diffuse)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, position)

        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_TWO_SIDE, lmodel_twoside)

        GL.glEnable(GL.GL_LIGHT1)
        # glLightfv(GL.GL_LIGHT1, GL.GL_AMBIENT, ambient)
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_DIFFUSE, diffuse)
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_POSITION, position1)
        GL.glEnable(GL.GL_LIGHTING)

        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS,
                        front_mat_shininess)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_SPECULAR,
                        front_mat_specular)
        GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_DIFFUSE,
                        front_mat_diffuse)

        self.tex = self.renderer.gen_textures(1)
        # print('check2', self.tex)
        # self.renderer.bind_texture(self.tex)
        self.tex2 = self.renderer.gen_textures(1)
        self.tex3 = self.renderer.gen_textures(1)
        # print('check2', self.tex2)
        # self.renderer.bind_texture(self.tex2)

    def convert_to_rgb(self, minval, maxval, val, colors):
        fi = float(val - minval) / float(maxval - minval) * (len(colors) - 1)
        i = int(fi)
        f = fi - i
        EPSILON = sys.float_info.epsilon

        if f < EPSILON:
            return colors[i]
        else:
            (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i + 1]
            return int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))

    def set_textures(self,filename1, filename2, filename3):

        img = Image.open(filename1)
        self.renderer.bind_texture(self.tex)
        self.texture = self.renderer.set_texture_as_image(img, self.tex)
        self.renderer.bind_texture(self.tex)


        img = Image.open(filename2)
        self.renderer.bind_texture(self.tex2)
        self.texture = self.renderer.set_texture_as_image(img, self.tex2)
        self.renderer.bind_texture(self.tex2)

        img = Image.open(filename3)
        self.renderer.bind_texture(self.tex3)
        self.texture = self.renderer.set_texture_as_image(img, self.tex3)
        self.renderer.bind_texture(self.tex3)

    def render(self, sim=None):
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(0.98, 0.98, 0.98, 0.0)
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glLoadIdentity()
        # glTranslate(0.0, -0.2, self.zoom)  # Camera

        # GL.glTranslate(0.1, 0, -1.6)
        # GL.glRotate(-0.452, 0.045, -0.002, 0.987)
        #
        GL.glLoadIdentity()
        # print(*self.tb.trans)
        GL.glTranslate(*self.tb.trans)
        GL.glMultMatrixf(self.tb.matrix)
        GL.glEnable(GL.GL_TEXTURE_2D)
        skel = sim.skeletons[-1]
        gnd  = sim.skeletons[-2]
        bod = skel.root_bodynode()
        # loc = skel.q
        # # print(loc[:3])
        # # print(bod.C)
        # GL.glBindTexture(GL.GL_TEXTURE_2D, 1)
        # bod.shapenodes[0].shape.render()
        # bod.shapenodes[1].shape.render()
        # ground.root_bodynode().shapenodes[0].shape.render()
        # self.renderer.render_box((loc[3], -0.25, loc[5]), (loc[0]/3.14*180, loc[1]/3.14*180, loc[2]/3.14*180), (0.05, 0.05, 0.05))



        #GLUT.glutSwapBuffers()
        # GL.glDisable(GL.GL_TEXTURE_2D)
        # GL.glEnable(GL.GL_TEXTURE_GEN_S)
        # GL.glEnable(GL.GL_TEXTURE_GEN_T)
        GL.glEnable(GL.GL_TEXTURE_2D)
        # GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glEnable(GL.GL_TEXTURE_GEN_S)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex)
        GL.glMultMatrixf(skel.bodynodes[0].T.T)
        # bod.shapenodes[0].shape.render()
        self.renderer.render_box((0.025, 0, 0), (1, 1, 1), (0.05, 0.01, 0.01))
        GL.glLoadIdentity()
        GL.glTranslate(*self.tb.trans)
        GL.glMultMatrixf(self.tb.matrix)
        GL.glMultMatrixf(skel.bodynodes[1].T.T)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex2)
        self.renderer.render_box((-0.025, 0, 0), (1, 1, 1), (0.05, 0.01, 0.01))
        # skel.bodynodes[1].shapenodes[1].shape.render()
        GL.glLoadIdentity()
        GL.glTranslate(*self.tb.trans)
        GL.glMultMatrixf(self.tb.matrix)
        GL.glMultMatrixf(gnd.bodynodes[0].T.T)
        GL.glEnable(GL.GL_TEXTURE_GEN_T)
        # GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.tex3)
        # gnd.bodynodes[0].shapenodes[0].shape.render()
        self.renderer.render_box((0, -0.1, 0), (0, 0, 0),(0.50, 0.05, 0.50))

    def render_seg(self, sim=None):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(0.98, 0.98, 0.98, 0.0)
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glLoadIdentity()
        # glTranslate(0.0, -0.2, self.zoom)  # Camera

        # GL.glTranslate(0.1, 0, -1.6)
        # GL.glRotate(-0.452, 0.045, -0.002, 0.987)
        #
        GL.glLoadIdentity()
        # print(*self.tb.trans)
        GL.glTranslate(*self.tb.trans)
        GL.glMultMatrixf(self.tb.matrix)
        GL.glDisable(GL.GL_TEXTURE_2D)
        # GL.glDisable(GL.GL_LIGHTING)
        skel = sim.skeletons[-1]
        loc = skel.q
        # print(loc)

        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        # self.renderer.render_box((-0+loc[1], -0.25, -0+loc[0]), (0.1, 0.1, 0.1))
        # self.renderer.render_box((loc[3], -0.25, loc[5]),
        #                          (loc[0] / 3.14 * 180, loc[1] / 3.14 * 180, loc[2] / 3.14 * 180), (0.2, 0.2, 0.2))

        #GLUT.glutSwapBuffers()
        # skel = sim.skeletons[-1]
        gnd  = sim.skeletons[-2]
        bod = skel.root_bodynode()

        GL.glDisable(GL.GL_TEXTURE_2D)
        # GL.glEnable(GL.GL_TEXTURE_GEN_S)
        # GL.glEnable(GL.GL_TEXTURE_GEN_T)
        # GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glMultMatrixf(skel.bodynodes[0].T.T)
        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
        r, g, b = self.convert_to_rgb(1, 3, skel.bodynodes[0].mass(), colors)
        GL.glColor3f(r/255., b/255., g/255.)
        self.renderer.render_box((0.025, 0, 0), (1, 1, 1), (0.05, 0.01, 0.01))
        # bod.shapenodes[0].shape.render()
        GL.glLoadIdentity()
        GL.glTranslate(*self.tb.trans)
        GL.glMultMatrixf(self.tb.matrix)
        GL.glMultMatrixf(skel.bodynodes[1].T.T)
        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
        r, g, b = self.convert_to_rgb(1, 3, skel.bodynodes[1].mass(), colors)
        GL.glColor3f(r/255., b/255., g/255.)
        self.renderer.render_box((-0.025, 0, 0), (1, 1, 1), (0.05, 0.01, 0.01))
        # skel.bodynodes[1].shapenodes[1].shape.render()
        # if sim is None:
        #     return
        #
        # if hasattr(sim, "render"):
        #     sim.render()
        # #self.renderer.enable("COLOR_MATERIAL")
        # if hasattr(sim, "render_with_ri"):
        #     sim.render_with_ri(self.renderer)
        #
        # self.enable2D()
        # if hasattr(sim, "draw_with_ri"):
        #     sim.draw_with_ri(self.renderer)
        #     self.renderer.draw_text([-100, -100], "")
        # self.disable2D()
        #GLUT.glutSwapBuffers()

    def enable2D(self):
        w, h = self.width, self.height
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glDisable(GL.GL_LIGHTING | GL.GL_DEPTH_TEST)
        GL.glDepthMask(0)
        GL.glOrtho(0, w, h, 0, -1, 1)
        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def disable2D(self):
        w, h = self.width, self.height
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()

        GL.glEnable(GL.GL_DEPTH_TEST | GL.GL_LIGHTING)
        GL.glDepthMask(1)
        GLU.gluPerspective(45.0, float(w) / float(h), 0.01, 100.0)

        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def init_cameras(self,):
        self.cameras = list()
        self.add_camera(
            Trackball(
                rot=[-0.152, 0.045, -0.002, 0.987],
                trans=[0.050, 0.210, -2.500]),
            "Camera Y up")
        self.add_camera(
            Trackball(
                rot=[0.535, 0.284, 0.376, 0.701], trans=[0.10, 0.02, -2.770]),
            "Camera Z up")
        self.set_camera(0)

    def num_cameras(self,):
        return len(self.cameras)

    def replace_camera(self, idx, trackball):
        if idx >= self.num_cameras():
            return False
        self.cameras[idx] = trackball
        return True

    def add_camera(self, trackball, name):
        self.cameras.append(trackball)
        if self.window is not None:
            # Need to pass self because glwidget is not inited yet
            self.window.add_camera_event(self, trackball, name)

    def set_camera(self, camera_index):
        print("set_camera: %d" % camera_index)
        self.tb = self.cameras[camera_index]
