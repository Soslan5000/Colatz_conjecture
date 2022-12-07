import pygame as pg
import math

class Cardioid:
    def __init__(self, app):
        self.app = app
        self.radius = 300
        self.num_lines = 4
        self.translate = self.app.screen.get_width() // 2, self.app.screen.get_height() // 2
        self.counter, self.inc = 0, 0.01

    def get_color(self, color1='red'):
        self.counter += self.inc
        self.counter, self.inc = (self.counter, self.inc) if 0 < self.counter < 1 else (
            max(min(self.counter, 1), 0), -self.inc)

        return pg.Color(color1)

    def draw(self):
        app.text = '1'
        dop_radius = 20

        for i in range(self.num_lines):
            one_angle = 2 * math.pi / self.num_lines
            theta = one_angle * i
            x_d = int((self.radius + dop_radius) * math.cos(theta)) + self.translate[0]
            y_d = int((self.radius + dop_radius) * math.sin(theta)) + self.translate[1]

            if i == 0:
                text_font = app.font.render(str(self.num_lines), False, (200, 200, 200))
            else:
                text_font = app.font.render(str(i), False, (200, 200, 200))
            app.screen.blit(text_font, (x_d, y_d))
            app.text = str(int(app.text) + 1)

        for i in range(1, self.num_lines):
            one_angle = 2 * math.pi / self.num_lines
            theta = one_angle * i
            kolatc = (i - 1) / 3
            int_kolatc = int(kolatc)

            x1 = int(self.radius * math.cos(theta)) + self.translate[0]
            y1 = int(self.radius * math.sin(theta)) + self.translate[1]

            if i <= self.num_lines // 2:
                x2 = int(self.radius * math.cos(2 * theta)) + self.translate[0]
                y2 = int(self.radius * math.sin(2 * theta)) + self.translate[1]
                pg.draw.aaline(self.app.screen, self.get_color('blue'), (x1, y1), (x2, y2))

            if kolatc > 0 and kolatc == int_kolatc and int_kolatc % 2 == 1:
                x3 = int(self.radius * math.cos((theta - one_angle) / 3)) + self.translate[0]
                y3 = int(self.radius * math.sin((theta - one_angle) / 3)) + self.translate[1]
                if int(math.log2(i)) == math.log2(i):
                    pg.draw.aaline(self.app.screen, self.get_color('red'), (x1, y1), (x3, y3))
                else:
                    pg.draw.aaline(self.app.screen, self.get_color('green'), (x1, y1), (x3, y3))

        self.num_lines += 1



class App:
    def __init__(self):
        self.screen = pg.display.set_mode([1000, 700])
        pg.font.init()
        self.font = pg.font.Font(None, 20)
        self.text = '1'
        self.clock = pg.time.Clock()
        self.cardioid = Cardioid(self)

    def draw(self):
        self.screen.fill('black')
        self.cardioid.draw()
        pg.display.flip()

    def run(self):
        while True:
            self.draw()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()