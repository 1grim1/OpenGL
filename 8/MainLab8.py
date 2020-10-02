from pyglet.window import mouse
from Figure import *
from Lab8 import *
import pickle

pos_and_color = [
    # 1 Red
    0, 0, 0, 1, 0, 0,
    1, 0, 0, 1, 0, 0,
    1, 1, 0, 1, 0, 0,
    0, 1, 0, 1, 0, 0,
    # 2 Green
    0, 0, 0, 0, 1, 0,
    1, 0, 0, 0, 1, 0,
    1, 0, 1, 0, 1, 0,
    0, 0, 1, 0, 1, 0,
    # 3 White
    1, 1, 0, 1, 1, 1,
    0, 1, 0, 1, 1, 1,
    0, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
    # 4 Yellow
    1, 0, 0, 1, 1, 0,
    1, 1, 0, 1, 1, 0,
    1, 1, 1, 1, 1, 0,
    1, 0, 1, 1, 1, 0,
    # 5 Blue
    0, 0, 0, 0, 0, 1,
    0, 1, 0, 0, 0, 1,
    0, 1, 1, 0, 0, 1,
    0, 0, 1, 0, 0, 1,
    # 6 Purple
    1, 0, 1, 1, 0, 1,
    0, 0, 1, 1, 0, 1,
    0, 1, 1, 1, 0, 1,
    1, 1, 1, 1, 0, 1
]
point_animation = [Point(0, 0, 0)]
points = [Point(0, 0, 0)]


def f():
    R = 10
    t = pi / 2
    while t >= 0:
        x = R * cos(t)
        y = R * (sin(t) - 1)
        t -= pi / 30
        points.append(Point(x, y, 0))
    points.append(Point(1, -10, 0))
    points.append(Point(1, -20, 0))
    points.append(Point(0, -20, 0))
    size = len(points) - 2
    dy = 30 / size
    for i in range(size):
        point_animation.append(Point(10, -dy * i, 0))
    point_animation.append(Point(0, -(30 - dy), 0))


f()


class RealWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_maximum_size(500, 500)
        glClearColor(0, 0, 0, 0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.Figure = Figure(points)
        self.vertex = self.Figure.vertex
        self.vertex_size = len(self.vertex)
        self.test_obj = Object(self.vertex)
        self.scale = 0.02
        self.test_obj.updateScale(self.scale)
        self.alpha = 0
        self.betta = 90
        self.move = [0, 0]
        self.mode = 3
        self.poligon_mode = False
        self.text_flag = False
        self.light_on = False
        self.light_pos = [0, 0, 0]

        self.Figure_animated = Figure(point_animation)

        self.Figure.Animation = TwiningAnimation(self.Figure, self.Figure_animated)

    def save(self):  # сохранение все понятно
        with open("data.pickle", "wb") as write_file:
            print("Saving")

            pickle.dump(self.Figure.points, write_file)
            pickle.dump(self.Figure.start_point, write_file)
            pickle.dump(self.Figure.end_point, write_file)
            pickle.dump(self.Figure.xyz, write_file)
            pickle.dump(self.Figure.angle_mode, write_file)
            pickle.dump(self.Figure.vertex, write_file)
            pickle.dump(self.Figure.wire, write_file)
            pickle.dump(self.Figure.Texture, write_file)
            pickle.dump(self.Figure.Animation, write_file)
            pickle.dump(self.Figure.animation_on, write_file)

            pickle.dump(self.vertex, write_file)
            pickle.dump(self.vertex_size, write_file)
            pickle.dump(self.test_obj, write_file)
            pickle.dump(self.scale, write_file)
            pickle.dump(self.alpha, write_file)
            pickle.dump(self.betta, write_file)
            pickle.dump(self.move, write_file)
            pickle.dump(self.mode, write_file)
            pickle.dump(self.poligon_mode, write_file)
            pickle.dump(self.text_flag, write_file)
            pickle.dump(self.light_on, write_file)
            pickle.dump(self.light_pos, write_file)
            pickle.dump(self.Figure_animated, write_file)
            print("Scene Saved!")

    def load(self):  # сохранение и в конце изменение параметров для корректной работы
        with open("data.pickle", "rb") as read_file:
            print("Load....")
            # Model

            self.Figure.points = pickle.load(read_file)
            self.Figure.start_point = pickle.load(read_file)
            self.Figure.end_point = pickle.load(read_file)
            self.Figure.xyz = pickle.load(read_file)
            self.Figure.angle_mode = pickle.load(read_file)
            self.Figure.vertex = pickle.load(read_file)
            self.Figure.wire = pickle.load(read_file)
            self.Figure.Texture = pickle.load(read_file)
            self.Figure.Animation = pickle.load(read_file)
            self.Figure.animation_on = pickle.load(read_file)

            self.vertex = pickle.load(read_file)
            self.vertex_size = pickle.load(read_file)
            self.test_obj = pickle.load(read_file)
            self.scale = pickle.load(read_file)
            self.alpha = pickle.load(read_file)
            self.betta = pickle.load(read_file)
            self.move = pickle.load(read_file)
            self.mode = pickle.load(read_file)
            self.poligon_mode = pickle.load(read_file)
            self.text_flag = pickle.load(read_file)
            self.light_on = pickle.load(read_file)
            self.light_pos = pickle.load(read_file)
            self.Figure_animated = pickle.load(read_file)
            self.test_obj.use()
            self.test_obj.changeLightflag(self.light_on)
            self.test_obj.chagneTextureFlag(self.text_flag)
            self.Figure.Texture.open_texture(self.Figure.texture_name)
            self.test_obj.changeLightPos(self.light_pos)
            self.test_obj.updateScale(self.scale)
            self.test_obj.updateTranslate(self.move[0], self.move[1], 0)
            self.test_obj.updateRotateValue(self.alpha / 100, 1, 0, 0)
            self.test_obj.updateRotateValue(self.betta / 100, 0, 1, 0)
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_size // 11 + 11)
            print("Scene Load!")

    def on_draw(self):
        self.clear()
        glEnable(GL_DEPTH_TEST)
        if self.poligon_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_size // 11 + 11)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.Figure.changeAngleMode(scroll_y)
        self.Figure_animated.changeAngleMode(scroll_y)
        self.vertex = self.Figure.vertex
        self.vertex_size = len(self.vertex)
        self.test_obj.changeBuffer(self.vertex)
        self.Figure.Animation.changeVal(self.Figure, self.Figure_animated)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            self.alpha += dy
            self.betta += dx
            self.test_obj.updateRotateValue(self.alpha / 100, 1, 0, 0)
            self.test_obj.updateRotateValue(self.betta / 100, 0, 1, 0)
        if buttons == mouse.RIGHT:
            self.move[0] = dx / (self.width / 2)
            self.move[1] = dy / (self.height / 2)
            self.test_obj.updateTranslate(self.move[0], self.move[1], 0)

    def on_key_press(self, symbol, modifiers):
        if symbol == 119:
            self.scale += 0.01
            self.test_obj.updateScale(self.scale)
        if symbol == 115:
            self.scale -= 0.01
            self.test_obj.updateScale(self.scale)
        if symbol == 112:  # P
            self.poligon_mode = not self.poligon_mode
        if symbol == 116:  # T
            self.text_flag = not self.text_flag
            self.test_obj.chagneTextureFlag(self.text_flag)
        if symbol == 108:  # L
            self.light_on = not self.light_on
            self.test_obj.changeLightflag(self.light_on)

        if symbol == 97:  # A
            self.Figure.animation_on = not self.Figure.animation_on

        if symbol == 65474:  # f5
            self.save()
        if symbol == 65478:  # f9
            self.load()

    def update(self, dt):
        if self.Figure.animation_on:
            self.Figure.GetAnimation()
            self.vertex = []
            self.vertex = self.Figure.vertex
            self.vertex_size = len(self.vertex)
            self.test_obj.changeBuffer(self.vertex)


if __name__ == "__main__":
    window = RealWindow(500, 500, "Main_LAB8", resizable=True)
    pyglet.clock.schedule_interval(window.update, .1)
    pyglet.app.run()
