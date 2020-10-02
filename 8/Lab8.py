from pyglet.gl import *
import OpenGL.GL.shaders as glShaders
import ctypes
from ShaderCode import *


class Object:
    def __init__(self, vertex):
        self.vertex = vertex
        self.transl_x = 0
        self.transl_y = 0
        self.transl_z = 0
        self.size = len(self.vertex)
        shader_code = ShaderCode()

        self.vertex_shader_source = shader_code.vertex_shader

        self.fragment_shader_source = shader_code.fragment_shader

        self.shaderProgram = glShaders.GL.shaders.compileProgram(
            glShaders.GL.shaders.compileShader(self.vertex_shader_source, GL_VERTEX_SHADER),
            glShaders.GL.shaders.compileShader(self.fragment_shader_source, GL_FRAGMENT_SHADER))

        self.use()

    def use(self):
        glUseProgram(self.shaderProgram)

        vertex_buffer_object = GLuint(0)

        glGenBuffers(1, vertex_buffer_object)

        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)

        glBufferData(GL_ARRAY_BUFFER,
                     4 * self.size,
                     (GLfloat * self.size)(*self.vertex),
                     GL_STATIC_DRAW)

        # positions
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # colors
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        # normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(36))
        glEnableVertexAttribArray(3)

    def updateScale(self, scale):
        Scale_location = glGetUniformLocation(self.shaderProgram, bytes('Scale', encoding='utf - 8'))
        glUniform1f(Scale_location, scale)

    def updateRotateValue(self, angle, ort_x, ort_y, ort_z):
        if ort_x:
            rotateAngle_x_location = glGetUniformLocation(self.shaderProgram, bytes('rotateAngle_x', encoding='utf - 8'))
            glUniform1f(rotateAngle_x_location, angle)
        if ort_y:
            rotateAngle_y_location = glGetUniformLocation(self.shaderProgram, bytes('rotateAngle_y', encoding='utf - 8'))
            glUniform1f(rotateAngle_y_location, angle)
        if ort_z:
            rotateAngle_z_location = glGetUniformLocation(self.shaderProgram, bytes('rotateAngle_z', encoding='utf - 8'))
            glUniform1f(rotateAngle_z_location, angle)

    def updateTranslate(self, x, y, z):
        self.transl_x += x
        self.transl_y += y
        self.transl_z += z
        translate_location_x = glGetUniformLocation(self.shaderProgram, bytes('Translate_x', encoding='utf - 8'))
        glUniform1f(translate_location_x, self.transl_x)
        translate_location_y = glGetUniformLocation(self.shaderProgram, bytes('Translate_y', encoding='utf - 8'))
        glUniform1f(translate_location_y, self.transl_y)
        translate_location_z = glGetUniformLocation(self.shaderProgram, bytes('Translate_z', encoding='utf - 8'))
        glUniform1f(translate_location_z, self.transl_z)

    def changeBuffer(self, vertex):
        self.vertex = vertex
        self.size = len(vertex)
        self.use()

    def changeTexture(self, texture):
        Texture_location = glGetUniformLocation(self.shaderProgram, bytes('texture', encoding='utf - 8'))
        glUniform1i(Texture_location, 0)

    def chagneTextureFlag(self, flag):
        Texture_on = glGetUniformLocation(self.shaderProgram, bytes('texture_on', encoding='utf - 8'))
        glUniform1i(Texture_on, flag)

    def changeLightflag(self, flag):
        Light_on = glGetUniformLocation(self.shaderProgram, bytes('light_on', encoding='utf - 8'))
        glUniform1i(Light_on, flag)
