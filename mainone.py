import os
from pyrr import Vector3, matrix44, Matrix44
import glfw
from OpenGL.GL.shaders import compileProgram, compileShader

from rotation_util import rotation_matrix
from texture_util import uploadTextureToGPU
from object_loader import loadObject
from OpenGL.GL import *
import numpy as np

WIDTH, HEIGHT = 1880, 1000

rotation = 0


def drawModel(index, vertices_count, position):
    glBindVertexArray(VAO[index])
    glBindTexture(GL_TEXTURE_2D, textures[index])

    glUniformMatrix4fv(model_location, 1, GL_FALSE, position)

    glDrawArrays(GL_TRIANGLES, 0, vertices_count)
    glBindTexture(GL_TEXTURE_2D, 0)


def uploadModelToGPU(vertices, vao_idx):
    glBindVertexArray(VAO[vao_idx])
    glBindBuffer(GL_ARRAY_BUFFER, VBO[vao_idx])
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)


def getFileContents(filename):
    p = os.path.join(os.getcwd(), filename)
    return open(p, 'r').read()


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(WIDTH, HEIGHT, "Awesome Logos", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")


def key_input_clb(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


glfw.set_key_callback(window, key_input_clb)

# glfw.set_window_size_callback(window, window_resize)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

glfw.make_context_current(window)

# Initialize OpenGL
glClearColor(0.2, 0.2, 0.2, 1)
glEnable(GL_DEPTH_TEST)

adidas_vertices, adidas_buffer = loadObject("models/adidas.obj")
jordan_indices, jordan_buffer = loadObject("models/jordan.obj")
lamborghini_indices, lamborghini_buffer = loadObject("models/google.obj")
nike_indices, nike_buffer = loadObject("models/nike.obj")
spotify_indices, spotify_buffer = loadObject("models/spotify.obj")

program = compileProgram(compileShader(getFileContents("objects.vertex.shader"), GL_VERTEX_SHADER),
                         compileShader(getFileContents("objects.fragment.shader"), GL_FRAGMENT_SHADER))

VAO = glGenVertexArrays(5)
VBO = glGenBuffers(5)

uploadModelToGPU(adidas_buffer, 0)
uploadModelToGPU(jordan_buffer, 1)
uploadModelToGPU(lamborghini_buffer, 2)
uploadModelToGPU(nike_buffer, 3)
uploadModelToGPU(spotify_buffer, 4)

textures = glGenTextures(5)
textures = list(map(uploadTextureToGPU, zip([
    "textures/adidas.png",
    "textures/jordan.png",
    "textures/google.png",
    "textures/nike.png",
    "textures/spotify.png",
], textures)))

glUseProgram(program)

adidas_pos = matrix44.create_from_translation(Vector3([4.5, 2, 0]))
jordan_pos = matrix44.create_from_translation(Vector3([7, -1, 0]))
lamborghini_pos = matrix44.create_from_translation(Vector3([-2.5, 2, 0]))
nike_pos = matrix44.create_from_translation(Vector3([0, -1, 0]))
spotify_pos = matrix44.create_from_translation(Vector3([11, 2, 0]))

model_location = glGetUniformLocation(program, "model")
projection_location = glGetUniformLocation(program, "projection")
view_location = glGetUniformLocation(program, "view")
rotation_loc = glGetUniformLocation(program, "rotation")

projection = matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)
glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)

t = 0

# main loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    dt = t - glfw.get_time()
    t = glfw.get_time()

    rotation += -1 * dt

    view = matrix44.create_look_at(Vector3([-4, 0, 10]), Vector3([2.5, 0, 0]), Vector3([0, 1, 0]))
    rotMat = matrix44.multiply(matrix44.create_from_x_rotation(np.radians(90)), matrix44.create_from_z_rotation(np.radians(rotation)))

    glUniformMatrix4fv(view_location, 1, GL_FALSE, view)
    glUniformMatrix4fv(rotation_loc, 1, GL_TRUE, rotMat)

    drawModel(0, adidas_vertices, adidas_pos)
    drawModel(1, jordan_indices, jordan_pos)
    drawModel(2, lamborghini_indices, lamborghini_pos)
    drawModel(3, nike_indices, nike_pos)
    drawModel(4, spotify_indices, spotify_pos)

    glfw.swap_buffers(window)

glfw.terminate()
