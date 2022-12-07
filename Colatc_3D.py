import pygame as pg
import random
import math

# spiral_dist = int(input('Введите расстояние между спиралями: '))
vec2, vec3 = pg.math.Vector2, pg.math.Vector3
RES = WIDTH, HEIGHT = 1300, 700
COLORS = 'purple'.split()
# COLORS = 'red green blue orange purple cyan'.split()
ALPHA = 120
num_points = 100
PAIR_DIST = 0.2
RADIUS = 40*num_points
Z_DIST = num_points * PAIR_DIST
VELOCITY = RADIUS // num_points * PAIR_DIST**3.5


class Point:
    def __init__(self, app, ind, z_dist, radius):
        self.num_points = num_points
        self.ind = ind
        self.flag = 0
        self.one_angle = 2 * math.pi / self.num_points
        self.radius = radius
        self.screen = app.screen
        self.velocity = VELOCITY
        self.z_dist = Z_DIST
        self.pos3d = self.get_pos3d(Z_DIST)
        self.screen_pos = vec2(0, 0)
        self.size = 2
        self.center = vec2(self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.color = random.choice(COLORS)

    def get_pos3d(self, pos_0):
        if self.flag == 1:
            if self.ind != 1:
                self.z_dist = pos_0 + (self.ind - 1) * PAIR_DIST
            else:
                self.z_dist = Z_DIST
        else:
            if self.ind != 1:
                self.z_dist = Z_DIST + (self.ind - 1) * PAIR_DIST
            else:
                self.z_dist = Z_DIST

        angle = self.one_angle * self.ind
        x = self.radius * math.sin(angle)
        y = self.radius * math.cos(angle)
        return vec3(x, y, self.z_dist)

    def update(self, pos_0):
        self.pos3d.z -= self.velocity
        if self.pos3d.z <= 0:
            self.flag = 1
            self.pos3d = self.get_pos3d(pos_0)

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / (self.pos3d.z + 10**(-10000)) + self.center

        # Если надо включить поворот спирали
        # self.pos3d.xy = self.pos3d.xy.rotate(0.2)

        # Для того, чтобы экран следовал на мышкой
        mouse_pos = self.center - vec2(pg.mouse.get_pos())
        self.screen_pos += mouse_pos

    def draw_l(self, pos1, pos2, line_color):
        pg.draw.aaline(self.screen, line_color, pos1, pos2)

    def draw_p(self, pos1):
        pg.draw.circle(self.screen, self.color, pos1, self.size)


class Pointfield:
    def __init__(self, app):
        self.num_points = num_points
        self.z_dist = Z_DIST
        self.radius = RADIUS
        self.points = [Point(app, i, self.z_dist, self.radius) for i in range(1, self.num_points)]
        [point.update(self.points[0].pos3d.z) for point in self.points]

    def run(self):
        [point.update(self.points[0].pos3d.z) for point in self.points]

        for i in range(1, len(self.points)):
            kolatc = (i - 1) / 3
            int_kolatc = int(kolatc)
            pos1 = self.points[i].screen_pos
            self.points[i].draw_p(pos1)

            if i < len(self.points) / 2 and self.points[i].pos3d.z > 0 and\
                    (abs(abs(self.points[i * 2].pos3d.z - self.points[i].pos3d.z) - PAIR_DIST*abs(self.points[i * 2].ind - self.points[i].ind)) < 10)\
                    and (self.points[i * 2].pos3d.z >= self.points[i].pos3d.z):
                line_color = 'red'
                pos2 = self.points[i * 2].screen_pos
                self.points[i].draw_l(pos1, pos2, line_color)
            if kolatc > 0 and kolatc == int_kolatc and int_kolatc % 2 == 1 and self.points[int_kolatc].pos3d.z > 0 and\
                    (abs(self.points[int_kolatc].pos3d.z - self.points[i].pos3d.z) - PAIR_DIST*abs(self.points[int_kolatc].ind - self.points[i].ind) < 10)\
                    and (self.points[i].pos3d.z >= self.points[int_kolatc].pos3d.z):
                line_color = 'yellow'
                pos3 = self.points[int_kolatc].screen_pos
                self.points[i].draw_l(pos1, pos3, line_color)

class App:
    def __init__(self):
        self.screen = pg.display.set_mode([1300, 700])
        self.clock = pg.time.Clock()
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)
        self.center = vec2(self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.Pointfield = Pointfield(self)

    def run(self):
        while True:
            self.screen.blit(self.alpha_surface, (0, 0))
            # self.screen.fill('black')
            self.Pointfield.run()

            pg.display.flip()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()