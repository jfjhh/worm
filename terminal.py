from pg_utils import *

class Terminal:
    def __init__(self, surf, fontpx=gfontpx,
            font=pg.font.Font("monaco.ttf", gfontpx), x=gfontpx/4, y=gfontpx/4,
            color=fg_color, aa=True):
        self.font   = font
        self.fontpx = fontpx
        self.surf   = surf
        self.x0     = x
        self.y0     = y
        self.x      = x
        self.y      = y
        self.w      = 0
        self.color  = color
        self.aa     = aa

    def echo(self, string):
        r = self.font.render(string, 1 if self.aa else 0, self.color)
        self.surf.blit(r, (self.x, self.y))
        size = font.size(string)
        self.w = max(self.w, size[0])
        self.y += 2/3 * self.fontpx

    def clear(self):
        r = pg.Rect(self.x0, self.y0, self.w, self.y - self.y0 + self.fontpx/2)
        pg.draw.rect(self.surf, bg_color, r)
        self.x = self.x0
        self.y = self.y0

