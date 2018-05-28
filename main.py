from vec_utils import *
from pg_utils import *
from camera import *
from frame import *
from terminal import *

def main():
    pg.init()
    pg.mixer.quit()
    pg.display.set_caption("worm")

    screen = pg.display.set_mode((width, height))
    surf = pg.Surface((width, height))
    running = True
    camera = OrthographicCamera()
    terminal = Terminal(surf)

    frames = []
    root_frame = Frame(None,
            r=vec([0., 0., 0.]),
            td=vec([0., 0., 1.0]),
            )
    b_frame = Frame(root_frame,
            r=vec([1., 0.2, 0.]),
            td=vec([5.0, 0., 0.]),
            )
    c_frame = Frame(b_frame,
            r=vec([1., 1., 0.]),
            td=vec([0.0, 0., 1.0]),
            )
    d_frame = Frame(c_frame,
            r=vec([0., 0., 0.]),
            rd=vec([-0.1, -0.1, -0.1]),
            td=vec([1., 0.5, 0.]),
            )
    frames.append(root_frame)
    frames.append(b_frame)
    frames.append(c_frame)
    frames.append(d_frame)

    # TODO:
    # - Variable frame rate.
    # - Frames as a collection of unit vectors, actual rotated drawing.

    gdt = 1e-4
    iters = 1e-2/gdt
    gdtf = 1/(fps*iters*gdt)
    ticks = 0
    roll = 64
    rfps = [fps] * roll
    riters = [iters] * roll
    surf.fill(bg_color)

    while running:
        ticks += 1
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                k = event.key
                surf.fill(bg_color)
                if   k == K_ESCAPE or k == K_q: running = False
                elif k == K_r:       camera = OrthographicCamera()
                elif k == K_COMMA:   camera.zoom_in()
                elif k == K_PERIOD:  camera.zoom_out()
                elif k == K_LEFT:    camera.left()
                elif k == K_RIGHT:   camera.right()
                elif k == K_UP:      camera.up()
                elif k == K_DOWN:    camera.down()
                elif k == K_h:       camera.rotate_left()
                elif k == K_l:       camera.rotate_right()
                elif k == K_j:       camera.rotate_down()
                elif k == K_k:       camera.rotate_up()
                elif k == K_u:       camera.rotate_near()
                elif k == K_m:       camera.rotate_far()
                elif k == K_d:       gdt *= 2.
                elif k == K_a:       gdt /= 2.

        grid_spacing = 10
        for i in range(0, int(hwidth / grid_spacing)):
            xr = hwidth + grid_spacing*i
            xl = hwidth - grid_spacing*i
            color = darkgray if i % 5 == 0 else darkergray
            pg.draw.line(surf, color, (xr, 0), (xr, height), 1)
            pg.draw.line(surf, color, (xl, 0), (xl, height), 1)
        for i in range(0, int(hheight / grid_spacing)):
            yu = hheight - grid_spacing*i
            yd = hheight + grid_spacing*i
            color = darkgray if i % 5 == 0 else darkergray
            pg.draw.line(surf, color, (0, yu), (width, yu), 1)
            pg.draw.line(surf, color, (0, yd), (width, yd), 1)
        pg.draw.line(surf, gray, (hwidth-2,hheight), (hwidth+2,hheight), 1)
        pg.draw.line(surf, gray, (hwidth,hheight-2), (hwidth,hheight+2), 1)

        for frame in frames:
            frame.draw(surf, camera, erase=True, fancy=gfancy)
        for i in range(0, round(iters)):
            for frame in frames:
                frame.update(gdt)
        for frame in frames:
            frame.draw(surf, camera, fancy=gfancy)

        cur_fps = clock.get_fps()
        roll_push(rfps, cur_fps)
        roll_push(riters, iters)
        mfps = mean(rfps)
        miters = mean(riters)

        terminal.clear()
        terminal.echo(":: worm ::")
        terminal.echo("ver: 0.1")
        terminal.echo("who: alex striff")
        terminal.echo("xf/s: {0:.1f}".format(fps))
        terminal.echo("if/s: {0:.1f}".format(cur_fps))
        terminal.echo("it/f: {0:.1f}".format(iters))
        terminal.echo("#rm: {0}".format(roll))
        terminal.echo("rf/s: {0:.1f}".format(mfps))
        terminal.echo("rt/f: {0:.1f}".format(miters))
        terminal.echo("rt/s: {0}".format(int(mfps*miters)))
        terminal.echo("#tk: {0}".format(ticks))
        terminal.echo("est: {0:.1f}".format(ticks*iters*gdt*gdtf))
        terminal.echo("gdt: {0:.3g}".format(gdt))
        terminal.echo("#fr: {0}".format(len(frames)))
        vec_label = lambda v: "    {0:3.1f}  {1:3.1f}  {2:3.1f}".format(*v)
        for frame in frames:
            terminal.echo(" :: {0} frame ::".format(frame.name))
            terminal.echo(vec_label(frame.r))
            terminal.echo(vec_label(frame.i))
            terminal.echo(vec_label(frame.j))
            terminal.echo(vec_label(frame.k))

        # terminal.echo(vec_label(self.r))
        # terminal.echo(vec_label(self.i))
        # terminal.echo(vec_label(self.j))
        # terminal.echo(vec_label(self.k))


        screen.blit(surf, (0, 0))
        pg.display.flip()

        # if mfps < fps:
        #     iters -= 0.05
        # else:
        #     iters += 0.05

        # clock.tick(fps)


if __name__ == "__main__":
    main()

