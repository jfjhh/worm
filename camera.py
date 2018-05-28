from vec_utils import *

class OrthographicCamera:
    def __init__(self, s=50., x=0., y=0., z=0., tx=0., ty=0., tz=0.):
        self.s  = s
        self.x  = x
        self.y  = y
        self.z  = z
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.scaling     = np.identity(4)
        self.translation = np.identity(4)
        self.rotation    = np.identity(4)
        self.projection  = np.identity(4)
        self.update_scaling()
        self.update_translation()
        self.update_rotation()

    def zoom_in(self, xf=2):            self.s  *= xf; self.update_scaling()
    def zoom_out(self, xf=2):           self.s  /= xf; self.update_scaling()
    def left(self, dl=50):       self.x  -= dl/self.s; self.update_translation()
    def right(self, dl=50):      self.x  += dl/self.s; self.update_translation()
    def up(self, dl=50):         self.y  += dl/self.s; self.update_translation()
    def down(self, dl=100):      self.y  -= dl/self.s; self.update_translation()
    def rotate_left(self, dt=np.pi/8):  self.tx += dt; self.update_rotation()
    def rotate_right(self, dt=np.pi/8): self.tx -= dt; self.update_rotation()
    def rotate_up(self, dt=np.pi/8):    self.ty += dt; self.update_rotation()
    def rotate_down(self, dt=np.pi/8):  self.ty -= dt; self.update_rotation()
    def rotate_near(self, dt=np.pi/8):  self.tz += dt; self.update_rotation()
    def rotate_far(self, dt=np.pi/8):   self.tz -= dt; self.update_rotation()

    def update_scaling(self):
        s = self.s
        self.scaling = mat([
            [s, 0, 0, 0],
            [0, s, 0, 0],
            [0, 0, s, 0],
            [0, 0, 0, 1]])
        self.update_projection()

    def update_translation(self):
        x = self.x
        y = self.y
        z = self.z
        self.translation = mat([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]])
        self.update_projection()

    def update_rotation(self):
        cx = np.cos(self.tx)
        sx = np.sin(self.tx)
        cy = np.cos(self.ty)
        sy = np.sin(self.ty)
        cz = np.cos(self.tz)
        sz = np.sin(self.tz)
        self.rotation = mat([
            [            cy*cz,            -cy*sz,     sy, 0],
            [ cz*sx*sy + cx*sz, -sx*sy*sz + cx*cz, -cy*sx, 0],
            [-cx*cz*sy + sx*sz,  cx*sy*sz + cz*sx,  cx*cy, 0],
            [                0,                 0,      0, 1]])

        self.update_projection()

    def update_projection(self):
        self.projection = self.scaling.dot(self.translation).dot(self.rotation)

    def project(self, v):
        return self.projection.dot(v)

