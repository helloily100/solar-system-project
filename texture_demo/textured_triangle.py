import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Mesh3D import *
from Object3D import *
from OpenGL.arrays import vbo
from numpy import array
from OpenGL.GL import shaders

from RenderProgram import *
import time
import math


def load_obj(filename) -> Object3D:
    with open(filename) as f:
        return Object3D(Mesh3D.load_obj(f))


def load_textured_obj(filename, texture_filename) -> Object3D:
    with open(filename) as f:
        return Object3D(
            Mesh3D.load_textured_obj(f, pygame.image.load(texture_filename))
        )


def load_shader_source(filename):
    with open(filename) as f:
        return f.read()


if __name__ == "__main__":
    pygame.init()
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("OpenGL in Python")

    # On Mac, we were getting errors when compiling shaders before loading a mesh.
    mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))

    # Load the vertex and fragment shaders for this program.
    vertex_shader = shaders.compileShader(
        load_shader_source("shaders/textured_perspective.vert"), GL_VERTEX_SHADER
    )
    fragment_shader = shaders.compileShader(
        load_shader_source("shaders/texture_mapped.frag"), GL_FRAGMENT_SHADER
    )
    shader_no_transform = shaders.compileProgram(vertex_shader, fragment_shader)

    # This renderer will keep track of the program and apply uniform values when drawing.
    renderer = RenderProgram(shader_no_transform)

    # Define the scene.
    camera = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    perspective = glm.perspective(
        math.radians(30), screen_width / screen_height, 0.1, 100
    )

    # Loop
    done = False
    frames = 0
    start = time.perf_counter()

    glEnable(GL_DEPTH_TEST)
    keys_down = set()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                keys_down.add(event.dict["key"])
            elif event.type == pygame.KEYUP:
                keys_down.remove(event.dict["key"])

        if pygame.K_UP in keys_down:
            mesh.rotate(glm.vec3(-0.1, 0, 0))
        elif pygame.K_DOWN in keys_down:
            mesh.rotate(glm.vec3(0.1, 0, 0))
        if pygame.K_RIGHT in keys_down:
            mesh.rotate(glm.vec3(0, 0.1, 0))
        elif pygame.K_LEFT in keys_down:
            mesh.rotate(glm.vec3(0, -0.1, 0))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # mesh.rotate(glm.vec3(0.01, 0.01, 0.01))
        # Render the scene given the perspective and camera matrices.
        renderer.render(perspective, camera, [mesh])

        pygame.display.flip()
        end = time.perf_counter()
        frames += 1
        print(f"{frames/(end - start)} FPS")

    pygame.quit()
