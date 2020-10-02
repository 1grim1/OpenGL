from math import *
import pyglet
from pyglet.gl import *
import copy


def mat_mult(matrix, points):  # Умножение матриц
    point = [points.x, points.y, points.z]
    new_point = []
    for i in range(3):
        elem = 0
        for j in range(3):
            elem += matrix[i][j] * point[j]
        new_point.append(elem)
    return Point(new_point[0], new_point[1], new_point[2])


def get_n(a, b):  # длина вектора
    len_xyz = sqrt(
        (b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2
    )
    return [((b.x - a.x) / len_xyz), ((b.y - a.y) / len_xyz), ((b.z - a.z) / len_xyz)]


class Point:  # точка

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.normal = [0, 0, 0]
        self.count_normal = 0

    def addNormal(self, normal):  # добавление к точке нормали
        self.normal[0] += normal.x
        self.normal[1] += normal.y
        self.normal[2] += normal.z
        self.count_normal += 1

    def getNormal(self):
        if self.normal == [0, 0, 0]:
            return 0, 0, 0
        size = sqrt(self.normal[0] ** 2 + self.normal[1] ** 2 + self.normal[2] ** 2)
        self.normal[0] /= size
        self.normal[1] /= size
        self.normal[2] /= size
        return self.normal[0] / self.count_normal, self.normal[1] / self.count_normal, self.normal[2] / self.count_normal


def makeNormal(p1, p2, p3, mode):  # создает нормаль к примитиву
    v1 = [p1.x - p2.x, p1.y - p2.y, p1.z - p2.z]
    v2 = [p3.x - p1.x, p3.y - p1.y, p3.z - p1.z]
    A = v1[1] * v2[2] - v1[2] * v2[1]
    B = v1[2] * v2[0] - v1[0] * v2[2]
    C = v1[0] * v2[1] - v1[1] * v2[0]
    if mode:
        return [A, B, C]
    else:
        return [-A, -B, -C]


def prepareNormal(p1, p2, p3, mark):  # добавляет в каждую точку плоскости нормаль
    n = makeNormal(p1, p2, p3, mark)
    n = Point(n[0], n[1], n[2])
    p1.addNormal(n)
    p2.addNormal(n)
    p3.addNormal(n)


class Texture:  # Текстура

    def __init__(self, dx, dy):
        self.texture = None
        self.x = 0
        self.y = 1
        self.dx = dx
        self.dy = dy

    def getTexCoord(self, i, j):  # получение координат текстур точке по координатам матрицы
        x = j * self.dx
        y = 1 - (i + 1) * self.dy
        return x, y

    def open_texture(self, name):
        self.texture = pyglet.image.load(name)
        self.load_texture()

    def load_texture(self):
        glBindTexture(self.texture.get_texture().target, self.texture.get_texture().id)
        glTexImage2D(GL_TEXTURE_2D,
                     0,
                     GL_RGBA,
                     self.texture.width,
                     self.texture.height,
                     0,
                     GL_RGBA,
                     GL_UNSIGNED_BYTE,
                     self.texture.get_image_data().get_data("RGBA", 4 * self.texture.width)
                     )
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)


class Figure:
    def __init__(self, points):
        self.points = points
        self.start_point = self.points[0]
        self.end_point = self.points[len(self.points) - 1]
        self.xyz = get_n(self.start_point, self.end_point)
        self.angle_mode = 6
        self.vertex = []
        self.wire = []
        self.wire = self.makeWire()
        self.Texture = Texture(1 / self.angle_mode, 1 / ((len(self.wire)) + 2))
        self.texture_name = "B:/21/" + "gold.bmp"
        self.Texture.open_texture(self.texture_name)
        self.prepareVertex()
        self.makeVertexBuffer()

        # Animation
        self.Animation = 0
        self.animation_on = False

    def changeAngleMode(self, change):  # изменение разбиений
        self.angle_mode += change
        self.angle_mode = max(self.angle_mode, 3)
        self.Texture.dx = 1 / self.angle_mode
        self.Texture.dy = 1 / ((len(self.wire)) + 2)
        self.wire = self.makeWire()
        self.prepareVertex()
        self.vertex = []
        self.makeVertexBuffer()

    def draw(self):  # Для рисования нормалей
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-100, 100, -100, 100, -100, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glScalef(10, 10, 10)
        for i in range(0, len(self.vertex), 11):
            glBegin(GL_LINES)
            glColor3ub(0, 0, 0)
            glVertex3d(self.vertex[i], self.vertex[i + 1], self.vertex[i + 2])
            glColor3ub(0, 0, 0)
            glVertex3d(self.vertex[i] + 10 * self.vertex[i + 6], self.vertex[i + 1] + 10 * self.vertex[i + 7], self.vertex[i + 2] + 10 * self.vertex[i + 8])
            glEnd()
        glPopMatrix()

    def prepareVertex(self):  # Подготовка и интерполяция нормалей
        self.prepareVertexStart()
        self.prepareVertexMid()
        self.prepareVertexEnd()

    def prepareVertexStart(self):  # интерполяция нормалей к примитивам в которые входит начальная точка
        size = len(self.wire[0])
        for i in range(0, size - 1):
            prepareNormal(self.wire[0][i], self.start_point, self.wire[0][i + 1], False)
            prepareNormal(self.wire[0][i + 1], self.start_point, self.start_point, False)
        prepareNormal(self.wire[0][size - 1], self.start_point, self.wire[0][0], False)
        prepareNormal(self.wire[0][0], self.start_point, self.start_point, False)

    def prepareVertexEnd(self):  # интерполяция конечной точки
        size = len(self.wire[len(self.wire) - 1])
        for i in range(0, size - 1):
            prepareNormal(self.end_point, self.wire[len(self.wire) - 1][i], self.end_point, False)
            prepareNormal(self.end_point, self.wire[len(self.wire) - 1][i], self.wire[len(self.wire) - 1][i + 1], False)
        prepareNormal(self.end_point, self.wire[len(self.wire) - 1][size - 1], self.end_point, False)
        prepareNormal(self.end_point, self.wire[len(self.wire) - 1][size - 1], self.wire[len(self.wire) - 1][0], False)

    def prepareVertexMid(self):  # интерполяция примитивов основных
        for i in range(0, len(self.wire) - 1):
            for j in range(0, len(self.wire[i]) - 1):
                prepareNormal(self.wire[i + 1][j], self.wire[i][j], self.wire[i + 1][j + 1], False)
                prepareNormal(self.wire[i + 1][j + 1], self.wire[i][j], self.wire[i][j + 1], False)
            prepareNormal(self.wire[i + 1][len((self.wire[i])) - 1], self.wire[i][len(self.wire[i]) - 1], self.wire[i + 1][0], False)
            prepareNormal(self.wire[i + 1][0], self.wire[i][len(self.wire[i]) - 1], self.wire[i][0], False)

    def rotate(self, angle):  # поворот матрица
        rotate = [[cos(angle) + (1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[0]),
                   (1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[1]) - float(self.xyz[2]) * sin(angle),
                   (1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[2]) + float(self.xyz[1]) * sin(angle)],
                  [(1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[1]) + float(self.xyz[2]) * sin(angle),
                   cos(angle) + (1.0 - cos(angle)) * float(self.xyz[1] * self.xyz[1]),
                   (1.0 - cos(angle)) * float(self.xyz[1] * self.xyz[2]) - float(self.xyz[0]) * sin(angle)],
                  [(1.0 - cos(angle)) * float(self.xyz[0] * self.xyz[2]) - float(self.xyz[1]) * sin(angle),
                   (1.0 - cos(angle)) * float(self.xyz[1] * self.xyz[2]) + float(self.xyz[0]) * sin(angle),
                   cos(angle) + (1.0 - cos(angle)) * float(self.xyz[2] * self.xyz[2])]]
        return rotate

    def makeWire(self):  # создает матрицу точек
        wire = []
        for i in range(1, len(self.points) - 1):
            angle = 0
            rotate_points = []
            point = Point(self.points[i].x, self.points[i].y, self.points[i].z)
            for k in range(int(self.angle_mode)):
                m = self.rotate(angle)
                p_new = mat_mult(m, point)
                rotate_points.append(p_new)
                angle += (2 * pi) / self.angle_mode
            wire.append(rotate_points)
        return wire

    def startVertexBuffer(self):  # делает буфер
        r, g, b = 1, 1, 1
        size1 = len(self.wire[0])
        for i in range(0, size1 - 1):
            A = self.start_point
            B = self.start_point
            C = self.wire[0][i]
            D = self.wire[0][i + 1]

            # C
            n_x, n_y, n_z = C.getNormal()
            x, y = self.Texture.getTexCoord(0, i)
            self.addInArr(
                [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # A
            n_x, n_y, n_z = A.getNormal()
            x, y = self.Texture.getTexCoord(-1, i)
            self.addInArr(
                [A.x, A.y, A.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # B
            n_x, n_y, n_z = B.getNormal()
            x, y = self.Texture.getTexCoord(-1, i + 1)
            self.addInArr(
                [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # B
            n_x, n_y, n_z = B.getNormal()
            x, y = self.Texture.getTexCoord(-1, i + 1)
            self.addInArr(
                [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # D
            n_x, n_y, n_z = D.getNormal()
            x, y = self.Texture.getTexCoord(0, i + 1)
            self.addInArr(
                [D.x, D.y, D.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # C
            n_x, n_y, n_z = C.getNormal()
            x, y = self.Texture.getTexCoord(0, i)
            self.addInArr(
                [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
            )

        A = self.start_point
        B = self.start_point
        C = self.wire[0][len(self.wire[0]) - 1]
        D = self.wire[0][0]

        # C
        n_x, n_y, n_z = C.getNormal()
        x, y = self.Texture.getTexCoord(1, len(self.wire[0]) - 1)
        self.addInArr(
            [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
        )
        # A
        n_x, n_y, n_z = A.getNormal()
        x, y = self.Texture.getTexCoord(-1, len(self.wire[0]) - 1)
        self.addInArr(
            [A.x, A.y, A.z, r, g, b, n_x, n_y, n_z, x, y]
        )

        # B
        n_x, n_y, n_z = B.getNormal()
        x, y = self.Texture.getTexCoord(-1, len(self.wire[0]))
        self.addInArr(
            [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
        )

        # B
        n_x, n_y, n_z = B.getNormal()
        x, y = self.Texture.getTexCoord(-1, len(self.wire[0]))
        self.addInArr(
            [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
        )

        # D
        n_x, n_y, n_z = D.getNormal()
        x, y = self.Texture.getTexCoord(0, len(self.wire[0]))
        self.addInArr(
            [D.x, D.y, D.z, r, g, b, n_x, n_y, n_z, x, y]
        )

        # C
        n_x, n_y, n_z = C.getNormal()
        x, y = self.Texture.getTexCoord(0, len(self.wire[0]) - 1)
        self.addInArr(
            [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
        )

    def GetAnimation(self):
        self.start_point, self.wire, self.end_point = self.Animation.animation()
        self.prepareVertex()
        self.makeVertexBuffer()

    def addInArr(self, vertex_attr):  # для буфера
        for elem in vertex_attr:
            self.vertex.append(elem)

    def midVertexBuffer(self):  # опять таки буфер
        for i in range(0, len(self.wire) - 1):
            r, g, b = 1, 1, 1
            AB = self.wire[i]
            CD = self.wire[i + 1]
            for j in range(0, len(AB) - 1):
                A = AB[j]
                B = AB[j + 1]
                C = CD[j]
                D = CD[j + 1]
                # print(A.count_normal, B.count_normal, C.count_normal, D.count_normal)

                # C
                n_x, n_y, n_z = C.getNormal()
                x, y = self.Texture.getTexCoord(i + 1, j)
                self.addInArr(
                    [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
                )

                # A
                n_x, n_y, n_z = A.getNormal()
                x, y = self.Texture.getTexCoord(i, j)
                self.addInArr(
                    [A.x, A.y, A.z, r, g, b, n_x, n_y, n_z, x, y]
                )

                # D
                n_x, n_y, n_z = D.getNormal()
                x, y = self.Texture.getTexCoord(i + 1, j + 1)
                self.addInArr(
                    [D.x, D.y, D.z, r, g, b, n_x, n_y, n_z, x, y]
                )

                # D
                n_x, n_y, n_z = D.getNormal()
                x, y = self.Texture.getTexCoord(i + 1, j + 1)
                self.addInArr(
                    [D.x, D.y, D.z, r, g, b, n_x, n_y, n_z, x, y]
                )

                # A
                n_x, n_y, n_z = A.getNormal()
                x, y = self.Texture.getTexCoord(i, j)
                self.addInArr(
                    [A.x, A.y, A.z, r, g, b, n_x, n_y, n_z, x, y]
                )

                # B
                n_x, n_y, n_z = B.getNormal()
                x, y = self.Texture.getTexCoord(i, j + 1)
                self.addInArr(
                    [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
                )

            A = AB[len(AB) - 1]
            B = AB[0]
            C = CD[len(CD) - 1]
            D = CD[0]

            # C
            n_x, n_y, n_z = C.getNormal()
            x, y = self.Texture.getTexCoord(i + 1, len(CD) - 1)
            self.addInArr(
                [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
            )
            # A
            n_x, n_y, n_z = A.getNormal()
            x, y = self.Texture.getTexCoord(i, len(AB) - 1)
            self.addInArr(
                [A.x, A.y, A.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # D
            n_x, n_y, n_z = D.getNormal()
            x, y = self.Texture.getTexCoord(i + 1, len(CD))
            self.addInArr(
                [D.x, D.y, D.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # D
            n_x, n_y, n_z = D.getNormal()
            x, y = self.Texture.getTexCoord(i + 1, len(CD))
            self.addInArr(
                [D.x, D.y, D.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # A
            n_x, n_y, n_z = A.getNormal()
            x, y = self.Texture.getTexCoord(i, len(AB) - 1)
            self.addInArr(
                [A.x, A.y, A.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # B
            n_x, n_y, n_z = B.getNormal()
            x, y = self.Texture.getTexCoord(i, len(AB))
            self.addInArr(
                [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
            )

    def endVertexBuffer(self):
        r, g, b = 1, 1, 1
        size = len(self.wire[len(self.wire) - 1])
        for i in range(0, size - 1):
            A = self.wire[len(self.wire) - 1][i]
            B = self.wire[len(self.wire) - 1][i + 1]
            C = D = self.end_point

            # C
            n_x, n_y, n_z = C.getNormal()
            x, y = self.Texture.getTexCoord(len(self.wire) + 1, i)
            self.addInArr(
                [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # A
            n_x, n_y, n_z = A.getNormal()
            x, y = self.Texture.getTexCoord(len(self.wire), i)
            self.addInArr(
                [A.x, A.y, A.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # B
            n_x, n_y, n_z = B.getNormal()
            x, y = self.Texture.getTexCoord(len(self.wire), i + 1)
            self.addInArr(
                [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # B
            n_x, n_y, n_z = B.getNormal()
            x, y = self.Texture.getTexCoord(len(self.wire), i + 1)
            self.addInArr(
                [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # D
            n_x, n_y, n_z = D.getNormal()
            x, y = self.Texture.getTexCoord(len(self.wire) + 1, i + 1)
            self.addInArr(
                [D.x, D.y, D.z, r, g, b, n_x, n_y, n_z, x, y]
            )

            # C
            n_x, n_y, n_z = C.getNormal()
            x, y = self.Texture.getTexCoord(len(self.wire) + 1, i)
            self.addInArr(
                [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
            )

        A = self.wire[len(self.wire) - 1][size - 1]
        B = self.wire[len(self.wire) - 1][0]
        C = D = self.end_point

        # C
        n_x, n_y, n_z = C.getNormal()
        x, y = self.Texture.getTexCoord(len(self.wire) + 1, len(self.wire))
        self.addInArr(
            [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
        )

        # A
        n_x, n_y, n_z = A.getNormal()
        x, y = self.Texture.getTexCoord(len(self.wire), len(self.wire) - 1)
        self.addInArr(
            [A.x, A.y, A.z, r, g, b, n_x, n_y, n_z, x, y]
        )

        # B
        n_x, n_y, n_z = B.getNormal()
        x, y = self.Texture.getTexCoord(len(self.wire), len(self.wire))
        self.addInArr(
            [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
        )

        # B
        n_x, n_y, n_z = B.getNormal()
        x, y = self.Texture.getTexCoord(len(self.wire), len(self.wire))
        self.addInArr(
            [B.x, B.y, B.z, r, g, b, n_x, n_y, n_z, x, y]
        )

        # D
        n_x, n_y, n_z = D.getNormal()
        x, y = self.Texture.getTexCoord(len(self.wire) + 1, len(self.wire))
        self.addInArr(
            [D.x, D.y, D.z, r, g, b, n_x, n_y, n_z, x, y]
        )

        # C
        n_x, n_y, n_z = C.getNormal()
        x, y = self.Texture.getTexCoord(len(self.wire) + 1, len(self.wire) - 1)
        self.addInArr(
            [C.x, C.y, C.z, r, g, b, n_x, n_y, n_z, x, y]
        )

    def makeVertexBuffer(self):  # буфер
        self.vertex = []
        self.startVertexBuffer()
        self.midVertexBuffer()
        self.endVertexBuffer()


class TwiningAnimation:

    def __init__(self, start, end):

        self.start = copy.deepcopy(start)

        self.end = copy.deepcopy(end)

        self.t = 0

        self.reverse = True

        self.wire = []

        self.start_point = 0

        self.end_point = 0

    def changeVal(self, start, end):
        self.start = copy.deepcopy(start)
        self.end = copy.deepcopy(end)
        self.wire = []
        self.start_point = 0
        self.end_point = 0

    def B(self, t, p0, p1, p2, p3):
        x = ((1 - t) ** 3) * p0.x + p1.x * (3 * t * ((1 - t) ** 2)) + p2.x * (3 * (t ** 2) * (1 - t)) + (t ** 3) * p3.x
        y = ((1 - t) ** 3) * p0.y + p1.y * (3 * t * ((1 - t) ** 2)) + p2.y * (3 * (t ** 2) * (1 - t)) + (t ** 3) * p3.y
        z = ((1 - t) ** 3) * p0.z + p1.z * (3 * t * ((1 - t) ** 2)) + p2.z * (3 * (t ** 2) * (1 - t)) + (t ** 3) * p3.z
        return Point(x, y, z)

    def animationStartPoint(self, t, point_end):
        s1 = self.start.start_point
        s2 = Point(s1.x + 0.1, s1.y + 0.1, s1.z)
        s3 = Point(s1.x + 0.2, s1.y + 0.1, s1.z)
        s4 = point_end
        s = self.B(t, s1, s2, s3, s4)
        self.start_point = s

    def animationEndPoint(self, t, point_end):
        s1 = self.start.end_point
        s2 = Point(s1.x + 0.1, s1.y + 0.1, s1.z)
        s3 = Point(s1.x + 0.2, s1.y + 0.1, s1.z)
        s4 = point_end
        s = self.B(t, s1, s2, s3, s4)
        self.end_point = s

    def animation_wall(self, t, a_wire):
        for k in range(len(self.start.wire)):
            wire1 = self.start.wire[k]
            arr = []
            for j in range(len(wire1)):
                p1 = wire1[j]
                p2 = Point(p1.x + 0.1, p1.y + 0.1, p1.z)
                p3 = Point(p1.x + 0.2, p1.y + 0.1, p1.z)
                p4 = a_wire[k][j]
                arr.append(self.B(t, p1, p2, p3, p4))
            self.wire.append(arr)

    def animation(self):
        self.wire = []
        self.start_point = 0
        self.end_point = 0
        self.animationStartPoint(self.t, self.end.start_point)
        self.animationEndPoint(self.t, self.end.end_point)
        self.animation_wall(self.t, self.end.wire)
        if self.reverse:
            self.t += 0.01
        else:
            self.t -= 0.01
        if self.t >= 1 or self.t <= 0:
            self.reverse = not self.reverse
        return self.start_point, self.wire, self.end_point
