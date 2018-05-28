from vec_utils import *
from pg_utils import *
from terminal import *

class Frame:
    namechar = 'A'
    def __init__(self, rel, name=None, i=None, j=None, k=None,
            r=np.zeros(3), rd=np.zeros(3), rdd=np.zeros(3),
            t=np.zeros(3), td=np.zeros(3), tdd=np.zeros(3)):
        if name is None:
            self.name = Frame.namechar
            Frame.namechar = chr(ord(Frame.namechar)+1)
        if i is None: i = vec([1., 0., 0.])
        if j is None: j = vec([0., 1., 0.])
        if k is None: k = vec([0., 0., 1.])
        self.b   = mat([i, j, k])
        self.rel = rel
        self.i   = self.b[0]
        self.j   = self.b[1]
        self.k   = self.b[2]
        self.r   = r
        self.rd  = rd
        self.rdd = rdd
        self.t   = t
        self.td  = td
        self.tdd = tdd

    def ext_velocity(self):
        return self.rd + np.cross(self.td, self.r)

    def ext_acceleration(self):
        return self.rdd \
                + np.cross(self.tdd, self.r) \
                + 2.*np.cross(self.td, self.rd) \
                + np.cross(self.td, np.cross(self.td, self.r))

    def update(self, dt=1.):
        self.rd += self.rdd * dt
        self.td += self.tdd * dt
        self.r  += self.ext_velocity() * dt
        self.i  += np.cross(self.td, self.i) * dt
        self.j  += np.cross(self.td, self.j) * dt
        self.k  += np.cross(self.td, self.k) * dt

    def relate(self, v=np.zeros(3), frame=False):
        if not frame:
            frame = self.rel
        basis = self.rel.b.transpose() if self.rel is not None else np.eye(3)
        u = basis.dot(v + self.r)
        return u if frame is None else frame.relate(u)

    def draw(self, surf, camera, erase=False, fancy=False):
        v = camera.project(homogenize(self.relate()))
        i = camera.project(homogenize(self.relate(self.i)))
        j = camera.project(homogenize(self.relate(self.j)))
        k = camera.project(homogenize(self.relate(self.k)))
        vx = hwidth  + v[0]
        vy = hheight - v[1]
        ix = hwidth  + i[0]
        iy = hheight - i[1]
        jx = hwidth  + j[0]
        jy = hheight - j[1]
        kx = hwidth  + k[0]
        ky = hheight - k[1]

        tcolor = bg_color if erase else yellow
        xcolor = bg_color if erase else green
        ycolor = bg_color if erase else red
        zcolor = bg_color if erase else blue

        pg.draw.line(surf, xcolor, (vx, vy), (ix, iy))
        pg.draw.line(surf, ycolor, (vx, vy), (jx, jy))
        pg.draw.line(surf, zcolor, (vx, vy), (kx, ky))

        term = Terminal(surf, aa=False, x=vx-8, y=vy, color=tcolor)
        term.echo(self.name)

        if not fancy: return

        r = camera.s
        d = camera.s / np.sqrt(2)

        if np.isclose(vx, ix) and np.isclose(vy, iy):
            j_x_k = j[0]*k[1] - j[1]*k[0]
            pg.draw.circle(surf, bg_color, (vx, vy), r, 0)
            pg.draw.circle(surf, xcolor, (vx, vy), r, 1)
            if j_x_k >= 0:
                pg.draw.circle(surf, xcolor, (vx, vy), r*5/12, 0)
            else:
                pg.draw.line(surf, xcolor, (vx-d, vy+d), (vx+d, vy-d))
                pg.draw.line(surf, xcolor, (vx-d, vy-d), (vx+d, vy+d))
        elif np.isclose(vx, jx) and np.isclose(vy, jy):
            k_x_i = k[0]*i[1] - k[1]*i[0]
            pg.draw.circle(surf, bg_color, (vx, vy), r, 0)
            pg.draw.circle(surf, ycolor, (vx, vy), r, 1)
            if k_x_i >= 0:
                pg.draw.circle(surf, ycolor, (vx, vy), r*5/12, 0)
            else:
                pg.draw.line(surf, ycolor, (vx-d, vy+d), (vx+d, vy-d))
                pg.draw.line(surf, ycolor, (vx-d, vy-d), (vx+d, vy+d))
        elif np.isclose(vx, kx) and np.isclose(vy, ky):
            i_x_j = i[0]*j[1] - i[1]*j[0]
            pg.draw.circle(surf, bg_color, (vx, vy), r, 0)
            pg.draw.circle(surf, zcolor, (vx, vy), r, 1)
            if i_x_j >= 0:
                pg.draw.circle(surf, zcolor, (vx, vy), r*5/12, 0)
            else:
                pg.draw.line(surf, zcolor, (vx-d, vy+d), (vx+d, vy-d))
                pg.draw.line(surf, zcolor, (vx-d, vy-d), (vx+d, vy+d))

