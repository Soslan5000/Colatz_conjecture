import pygame as pg
import math
import time


class Cardioid:
    def __init__(self, app):
        self.app = app
        self.radius = 300
        self.num_lines = 4
        self.translate = self.app.screen.get_width() // 2, self.app.screen.get_height() // 2
        self.counter, self.inc = 0, 0.09

    def get_color(self, color1='red'):
        self.counter += self.inc
        self.counter, self.inc = (self.counter, self.inc) if 0 < self.counter < 1 else (
            max(min(self.counter, 1), 0), -self.inc)

        return pg.Color('red').lerp('green', self.counter)

    def colatc(self, n):
        steps = [n]
        while n != 1:
            if n % 2 == 0:
                n = n // 2
                steps.append(n)
            else:
                n = n * 3 + 1
                steps.append(n)
        return steps

    def draw(self):
        number = app.number
        points = self.colatc(number)
        dop_radius = 30
        self.num_lines = max(points)
        one_angle = 2 * math.pi / self.num_lines

        pg.draw.circle(app.screen, (255, 255, 255), (self.translate[0], self.translate[1]), self.radius, 2)

        for i in points:
            theta = one_angle * i
            x_d = int((self.radius + dop_radius) * math.cos(theta)) + self.translate[0]
            y_d = int((self.radius + dop_radius) * math.sin(theta)) + self.translate[1]
            x_c = int((self.radius) * math.cos(theta)) + self.translate[0]
            y_c = int((self.radius) * math.sin(theta)) + self.translate[1]
            pg.draw.circle(app.screen, (255, 0, 255), (x_c, y_c), 5)

            if i == 0:
                text_font = app.font.render(str(max(points)), False, (200, 200, 200))
            else:
                text_font = app.font.render(str(i), False, (200, 200, 200))
            app.screen.blit(text_font, (x_d, y_d))
            app.text = str(int(app.text) + 1)

        for i in range(len(points) - 1):
            if points[i] % 2 == 1:
                color = pg.Color('red')
            else:
                color = pg.Color('green')

            theta1 = one_angle * points[i]
            theta2 = one_angle * points[i + 1]

            x1 = int(self.radius * math.cos(theta1)) + self.translate[0]
            y1 = int(self.radius * math.sin(theta1)) + self.translate[1]

            x2 = int(self.radius * math.cos(theta2)) + self.translate[0]
            y2 = int(self.radius * math.sin(theta2)) + self.translate[1]
            pg.draw.aaline(self.app.screen, color, (x1, y1), (x2, y2))
        font = pg.font.SysFont("serif", 72)

        text = font.render(str(app.number), True, (255, 0, 0))
        app.screen.blit(text, (10, 100))

        self.counter, self.inc = 0, 0.09


class App:
    def __init__(self):
        pg.font.init()
        self.text = '1'
        self.screen = pg.display.set_mode([1000, 700])
        self.font = pg.font.Font(None, 20)
        self.clock = pg.time.Clock()
        self.cardioid = Cardioid(self)
        self.number = 2
        self.PAUSED = False

    def draw(self):
        self.screen.fill('black')
        self.cardioid.draw()
        pg.display.flip()

    def run(self):

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.PAUSED = not self.PAUSED
                        font = pg.font.SysFont("serif", 72)
                        self.text_paused = font.render("PAUSED", True, (255, 0, 0))
                        self.screen.blit(self.text_paused, (10, 10))
                        pg.display.flip()


            if not self.PAUSED:
                self.number += 1
                pg.display.flip()
                self.draw()
                [exit() for i in pg.event.get() if i.type == pg.QUIT]
                self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()