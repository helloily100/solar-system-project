import glm
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Mesh3D_normals import *
from Object3D import *
from OpenGL.arrays import vbo
from numpy import array
from OpenGL.GL import shaders
import os
import assimp_py

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

def mesh_to_object3d(mesh, scene, filename, texture_path):
    material = scene.materials[mesh.material_index]

    if texture_path is None:
        if mesh.material_index > 0 and len(material["TEXTURES"]) == 0:
            material = scene.materials[0]

        if mesh.material_index < 0 or len(material["TEXTURES"]) == 0:
            raise Exception("You must provide a texture_path because the OBJ file has no .mtl file, or there is no texture set in the .mtl file")

        # Load the texture information from the obj file's material file.
        textures = material["TEXTURES"][1]
        objpath = os.path.dirname(filename)
        texture_path = os.path.join(objpath, textures[0])

    obj = Object3D(
        Mesh3D.load_assimp_mesh(
            mesh, pygame.image.load(texture_path)
        )
    )

    return obj

def assimp_load_object(filename, texture_path=None, assimp_options = assimp_py.Process_Triangulate) -> Object3D:
    scene = assimp_py.ImportFile(filename, assimp_options)

    if len(scene.meshes) == 1:
        return mesh_to_object3d(scene.meshes[0], scene, filename, texture_path)

    root = Object3D(None)
    for mesh in scene.meshes:
        obj = mesh_to_object3d(mesh, scene, filename, texture_path)
        root.add_child(obj)
    return root

def load_shader_source(filename):
    with open(filename) as f:
        return f.read()


def get_program(vertex_source_filename, fragment_source_filename):
    vertex_shader = shaders.compileShader(
        load_shader_source(vertex_source_filename), GL_VERTEX_SHADER
    )
    fragment_shader = shaders.compileShader(
        load_shader_source(fragment_source_filename), GL_FRAGMENT_SHADER
    )
    return shaders.compileProgram(vertex_shader, fragment_shader)


if __name__ == "__main__":
    pygame.init()
    screen_width = 1100
    screen_height = 600
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        DOUBLEBUF | OPENGL,
    )
    pygame.display.set_caption("OpenGL in Python")

    # mesh = load_textured_obj("models/dice.obj", "models/dice.png")

    #Sun
    #sun = load_textured_obj("models/sphere.obj", "models/Solarsystemscope_texture_2k_sun.jpg")
    sun = assimp_load_object("models/sphere.obj", "models/Solarsystemscope_texture_2k_sun.jpg")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    sun.center = glm.vec3(0, 0, 0)
    sun.move(glm.vec3(1, 1, 1))
    sun.grow(glm.vec3(0.01, 0.01, 0.01))

    # Mercury
    mercury = assimp_load_object("models/sphere.obj", "models/mercury_redo.jpg")
    # mercury.center = glm.vec3(sun.get_position()[0] + 1, sun.get_position()[1] + 1, sun.get_position()[2] +1)
    mercury.move(glm.vec3(2, 1, 1))
    mercury.grow(glm.vec3(0.002, 0.002, 0.002))

    # Venus
    venus = assimp_load_object("models/sphere.obj", "models/venus_redo.jpg")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    venus.center = glm.vec3(-0.03, 0.06, 0)
    #venus.move(glm.vec3(-0.6, 0, -1))
    venus.move(glm.vec3(2.5, 1, 1))
    venus.grow(glm.vec3(0.004, 0.004, 0.004))

    # Earth
    #earth = load_textured_obj("models/sphere.obj", "models/earth albedo.jpg")
    earth = assimp_load_object("models/sphere.obj", "models/earth albedo.jpg")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    earth.center = glm.vec3(-0.03, 0.06, 0)
    #earth.move(glm.vec3(-0.32, 0, -1))
    earth.move(glm.vec3(3, 1, 1))
    earth.grow(glm.vec3(0.004, 0.004, 0.004))
    #earth.grow(glm.vec3(0.1, 0.1, 0.1))

    # Moon
    moon = assimp_load_object("models/sphere.obj", "models/moon_texture.jpg")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    moon.center = glm.vec3(-0.03, 0.06, 0)
    #moon.move(glm.vec3(-0.32, 0.4, -1))
    moon.move(glm.vec3(3, 1.5, 1))
    moon.grow(glm.vec3(0.002, 0.002, 0.002))

    # Mars
    mars = assimp_load_object("models/sphere.obj", "models/mars_texture.jpg")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    mars.center = glm.vec3(-0.03, 0.06, 0)
    #mars.move(glm.vec3(-0.09, 0, -1))
    mars.move(glm.vec3(3.5, 1, 1))

    mars.grow(glm.vec3(0.003, 0.003, 0.003))

    # Asteroid belt
    '''
    asteroid = load_textured_obj("models/rock_by_dommk.obj", "models/rock_Base_Color.png")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    asteroid.center = glm.vec3(-0.03, 0.06, 0)
    asteroid.move(glm.vec3(0.2, 0, -1))
    asteroid.grow(glm.vec3(0.001, 0.001, 0.001))
    '''

    # Jupiter
    jupiter = assimp_load_object("models/sphere.obj", "models/jupiter_texture.jpg")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    jupiter.center = glm.vec3(-0.03, 0.06, 0)
    #jupiter.move(glm.vec3(0.5, 0, -1))
    jupiter.move(glm.vec3(4, 1, 1))
    jupiter.grow(glm.vec3(0.005, 0.005, 0.005))

    # Saturn
    saturn = assimp_load_object("models/sphere.obj", "models/saturn.jpg")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    saturn.center = glm.vec3(-0.03, 0.06, 0)
    #saturn.move(glm.vec3(0.8, 0, -1))
    saturn.move(glm.vec3(4.5, 1, 1))
    saturn.grow(glm.vec3(0.003, 0.003, 0.003))

    # Uranus
    uranus = assimp_load_object("models/sphere.obj", "models/uranus.png")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    uranus.center = glm.vec3(-0.03, 0.06, 0)
    #uranus.move(glm.vec3(1, 0, -1))
    uranus.move(glm.vec3(5, 1, 1))
    uranus.grow(glm.vec3(0.003, 0.003, 0.003))

    # Neptune
    neptune = assimp_load_object("models/sphere.obj", "models/neptune.png")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    neptune.center = glm.vec3(-0.03, 0.06, 0)
    #neptune.move(glm.vec3(1.2, 0, -1))
    neptune.move(glm.vec3(5.5, 1, 1))
    neptune.grow(glm.vec3(0.003, 0.003, 0.003))

    # Pluto
    pluto = assimp_load_object("models/sphere.obj", "models/pluto.png")
    # mesh = Object3D(Mesh3D.textured_triangle(pygame.image.load("models/wall.jpg")))
    pluto.center = glm.vec3(-0.03, 0.06, 0)
    #pluto.move(glm.vec3(1.5, 0, -1))
    pluto.move(glm.vec3(7, 1, 1))
    pluto.grow(glm.vec3(0.001, 0.001, 0.001))

    #lighting
    light = load_textured_obj("models/sphere.obj", "models/Solarsystemscope_texture_2k_sun.jpg")
    light.center = glm.vec3(0, 0, 0)
    light.move(glm.vec3(1, 1, 1))
    light.grow(glm.vec3(0.01, 0.01, 0.01))
    # mesh = load_textured_obj("models/bunny_textured.obj", "models/bunny_textured.jpg")

    # Load the vertex and fragment shaders for this program.
    vertex_shader = shaders.compileShader(
        load_shader_source("shaders/normal_perspective.vert"), GL_VERTEX_SHADER
    )

    #fragment_shader = shaders.compileShader(
     #   load_shader_source("shaders/ambient_light.frag"), GL_FRAGMENT_SHADER
    #)

    #fragment_shader = shaders.compileShader(
     #   load_shader_source("shaders/diffuse_light.frag"), GL_FRAGMENT_SHADER
    #)

    fragment_shader = shaders.compileShader(
       load_shader_source("shaders/specular_light.frag"), GL_FRAGMENT_SHADER
    )

    shader_lighting = shaders.compileProgram(vertex_shader, fragment_shader)

    # This renderer will keep track of the program and apply uniform values when drawing.
    renderer = RenderProgram(shader_lighting)

    # Define the scene.
    camera = glm.lookAt(glm.vec3(1, 1, 15), glm.vec3(1, 1, 1), glm.vec3(0, 1, 0))
    perspective = glm.perspective(
        math.radians(30), screen_width / screen_height, 0.1, 100
    )
    # In Classic OpenGL, FOVY is given in degrees. It must be radians in Modern OpenGL.

    ambient_color = glm.vec3(1, 1, 1)
    ambient_intensity = 0.70
    point_position = glm.vec3(0, 0, 0)
    renderer.set_uniform("ambientColor", ambient_color * ambient_intensity, glm.vec3)
    renderer.set_uniform("pointPosition", point_position, glm.vec3)
    renderer.set_uniform("pointColor", glm.vec3(1, 1, 1), glm.vec3)

    # Loop
    done = False
    frames = 0
    start = time.perf_counter()

    # camera = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    mouseMove = pygame.mouse.get_rel()
    glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)

    # Only draw wireframes.
    glEnable(GL_DEPTH_TEST)
    keys_down = set()
    spin = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                keys_down.add(event.dict["key"])
            elif event.type == pygame.KEYUP:
                keys_down.remove(event.dict["key"])

        if pygame.K_UP in keys_down:
            sun.rotate(glm.vec3(0, 0, 0.001))
            #earth.rotate(glm.vec3(0, 0, 0.001))
            earth_day = 365

            # mercury values
            mercury_day = earth_day / 88
            mercury_x = (((sun.get_position()[0] * 0.5) * math.cos(sun.get_orientation()[2] * mercury_day)) - (
                        sun.get_position()[1] * 0.5) * math.sin(sun.get_orientation()[2] * mercury_day)) + 1
            mercury_y = (((sun.get_position()[0] * 0.5) * math.cos(sun.get_orientation()[2] * mercury_day)) + (
                        sun.get_position()[1] * 0.5) * math.sin(sun.get_orientation()[2] * mercury_day)) + 1
            z = 1
            mercury.set_position(glm.vec3(mercury_x, mercury_y, z))

            # venus values
            venus_day = earth_day / 225
            venus_x = (((sun.get_position()[0] * 0.8) * math.cos(sun.get_orientation()[2] * venus_day)) - (
                        sun.get_position()[1] * 0.8) * math.sin(sun.get_orientation()[2] * venus_day)) + 1
            venus_y = (((sun.get_position()[0] * 0.8) * math.cos(sun.get_orientation()[2] * venus_day)) + (
                        sun.get_position()[1] * 0.8) * math.sin(sun.get_orientation()[2] * venus_day)) + 1

            venus.set_position(glm.vec3(venus_x, venus_y, z))

            # earth values
            e_day = earth_day / 365
            earth_x = (((sun.get_position()[0] * 1.1) * math.cos(sun.get_orientation()[2] * e_day)) - (
                        sun.get_position()[1] * 1.1) * math.sin(sun.get_orientation()[2] * e_day)) + 1
            earth_y = (((sun.get_position()[0] * 1.1) * math.cos(sun.get_orientation()[2] * e_day)) + (
                        sun.get_position()[1] * 1.1) * math.sin(sun.get_orientation()[2] * e_day)) + 1

            earth.set_position(glm.vec3(earth_x, earth_y, z))

            # moon values
            earth.rotate(glm.vec3(0, 0, 0.01))
            moon_x = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[2] + earth.get_orientation()[2])) - (sun.get_position()[1] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + earth_x
            moon_y = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + (sun.get_position()[1] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + earth_y
            moon_z = 1
            moon.set_position(glm.vec3(moon_x, moon_y, moon_z))

            # mars values
            mars_day = earth_day / 687
            mars_x = (((sun.get_position()[0] * 1.4) * math.cos(sun.get_orientation()[2] * mars_day)) - (
                        sun.get_position()[1] * 1.4) * math.sin(sun.get_orientation()[2] * mars_day)) + 1
            mars_y = (((sun.get_position()[0] * 1.4) * math.cos(sun.get_orientation()[2] * mars_day)) + (
                        sun.get_position()[1] * 1.4) * math.sin(sun.get_orientation()[2] * mars_day)) + 1

            mars.set_position(glm.vec3(mars_x, mars_y, z))

            # jupiter values
            jupiter_day = earth_day / 4333
            jupiter_x = (((sun.get_position()[0] * 1.7) * math.cos(sun.get_orientation()[2] * jupiter_day)) - (
                        sun.get_position()[1] * 1.7) * math.sin(sun.get_orientation()[2] * jupiter_day)) + 1
            jupiter_y = (((sun.get_position()[0] * 1.7) * math.cos(sun.get_orientation()[2] * jupiter_day)) + (
                        sun.get_position()[1] * 1.7) * math.sin(sun.get_orientation()[2] * jupiter_day)) + 1

            jupiter.set_position(glm.vec3(jupiter_x, jupiter_y, z))

            # saturn values
            saturn_day = earth_day /10765
            saturn_x = (((sun.get_position()[0] * 2) * math.cos(sun.get_orientation()[2] * saturn_day)) - (
                        sun.get_position()[1] * 2) * math.sin(sun.get_orientation()[2] * saturn_day)) + 1
            saturn_y = (((sun.get_position()[0] * 2) * math.cos(sun.get_orientation()[2] * saturn_day)) + (
                        sun.get_position()[1] * 2) * math.sin(sun.get_orientation()[2] * saturn_day)) + 1

            saturn.set_position(glm.vec3(saturn_x, saturn_y, z))

            # uranus values
            uranus_day = earth_day / 30687
            uranus_x = (((sun.get_position()[0] * 2.3) * math.cos(sun.get_orientation()[2] * uranus_day)) - (
                        sun.get_position()[1] * 2.3) * math.sin(sun.get_orientation()[2] * uranus_day)) + 1
            uranus_y = (((sun.get_position()[0] * 2.3) * math.cos(sun.get_orientation()[2] * uranus_day)) + (
                        sun.get_position()[1] * 2.3) * math.sin(sun.get_orientation()[2] * uranus_day)) + 1

            uranus.set_position(glm.vec3(uranus_x, uranus_y, z))

            # neptune values
            neptune_day = earth_day / 60190
            neptune_x = (((sun.get_position()[0] * 2.6) * math.cos(sun.get_orientation()[2] * neptune_day)) - (
                        sun.get_position()[1] * 2.6) * math.sin(sun.get_orientation()[2] * neptune_day)) + 1
            neptune_y = (((sun.get_position()[0] * 2.6) * math.cos(sun.get_orientation()[2] * neptune_day)) + (
                        sun.get_position()[1] * 2.6) * math.sin(sun.get_orientation()[2] * neptune_day)) + 1

            neptune.set_position(glm.vec3(neptune_x, neptune_y, z))

            # pluto values
            pluto_day = earth_day / 90560
            pluto_x = (((sun.get_position()[0] * 3.2) * math.cos(sun.get_orientation()[2] * pluto_day)) - (
                        sun.get_position()[1] * 3.2) * math.sin(sun.get_orientation()[2] * pluto_day)) + 1
            pluto_y = (((sun.get_position()[0] * 3.2) * math.cos(sun.get_orientation()[2] * pluto_day)) + (
                        sun.get_position()[1] * 3.2) * math.sin(sun.get_orientation()[2] * pluto_day)) + 1

            pluto.set_position(glm.vec3(pluto_x, pluto_y, z))

        elif pygame.K_DOWN in keys_down:
            sun.rotate(glm.vec3(0, 0, -0.001))
            #change sun.get_position()[0] to change distance from sun
            #change sun.get_position()[1]
            #make sure its all consistent
            '''
            x = (((sun.get_position()[0]/2) * math.cos(sun.get_orientation()[2])) - (sun.get_position()[1]/2) * math.sin(sun.get_orientation()[2])) + 1
            y = (((sun.get_position()[0]/2) * math.cos(sun.get_orientation()[2])) + (sun.get_position()[1]/2) * math.sin(sun.get_orientation()[2])) + 1
            z = 1
            mercury.set_position(glm.vec3(x, y, z))
            '''
            earth_day = 365

            # mercury values
            mercury_day = earth_day / 88
            mercury_x = (((sun.get_position()[0] * 0.5) * math.cos(sun.get_orientation()[2] * mercury_day)) - (
                    sun.get_position()[1] * 0.5) * math.sin(sun.get_orientation()[2] * mercury_day)) + 1
            mercury_y = (((sun.get_position()[0] * 0.5) * math.cos(sun.get_orientation()[2] * mercury_day)) + (
                    sun.get_position()[1] * 0.5) * math.sin(sun.get_orientation()[2] * mercury_day)) + 1
            z = 1
            mercury.set_position(glm.vec3(mercury_x, mercury_y, z))

            # venus values
            venus_day = earth_day / 225
            venus_x = (((sun.get_position()[0] * 0.8) * math.cos(sun.get_orientation()[2] * venus_day)) - (
                    sun.get_position()[1] * 0.8) * math.sin(sun.get_orientation()[2] * venus_day)) + 1
            venus_y = (((sun.get_position()[0] * 0.8) * math.cos(sun.get_orientation()[2] * venus_day)) + (
                    sun.get_position()[1] * 0.8) * math.sin(sun.get_orientation()[2] * venus_day)) + 1

            venus.set_position(glm.vec3(venus_x, venus_y, z))

            # earth values
            e_day = earth_day / 365
            earth_x = (((sun.get_position()[0] * 1.1) * math.cos(sun.get_orientation()[2] * e_day)) - (
                    sun.get_position()[1] * 1.1) * math.sin(sun.get_orientation()[2] * e_day)) + 1
            earth_y = (((sun.get_position()[0] * 1.1) * math.cos(sun.get_orientation()[2] * e_day)) + (
                    sun.get_position()[1] * 1.1) * math.sin(sun.get_orientation()[2] * e_day)) + 1

            earth.set_position(glm.vec3(earth_x, earth_y, z))

            # moon values
            earth.rotate(glm.vec3(0, 0, -0.01))
            moon_x = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[2] + earth.get_orientation()[2])) - (sun.get_position()[1] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + earth_x
            moon_y = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + (sun.get_position()[1] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + earth_y
            moon_z = 1
            moon.set_position(glm.vec3(moon_x, moon_y, moon_z))

            # mars values
            mars_day = earth_day / 687
            mars_x = (((sun.get_position()[0] * 1.4) * math.cos(sun.get_orientation()[2] * mars_day)) - (
                    sun.get_position()[1] * 1.4) * math.sin(sun.get_orientation()[2] * mars_day)) + 1
            mars_y = (((sun.get_position()[0] * 1.4) * math.cos(sun.get_orientation()[2] * mars_day)) + (
                    sun.get_position()[1] * 1.4) * math.sin(sun.get_orientation()[2] * mars_day)) + 1

            mars.set_position(glm.vec3(mars_x, mars_y, z))

            # jupiter values
            jupiter_day = earth_day / 4333
            jupiter_x = (((sun.get_position()[0] * 1.7) * math.cos(sun.get_orientation()[2] * jupiter_day)) - (
                    sun.get_position()[1] * 1.7) * math.sin(sun.get_orientation()[2] * jupiter_day)) + 1
            jupiter_y = (((sun.get_position()[0] * 1.7) * math.cos(sun.get_orientation()[2] * jupiter_day)) + (
                    sun.get_position()[1] * 1.7) * math.sin(sun.get_orientation()[2] * jupiter_day)) + 1

            jupiter.set_position(glm.vec3(jupiter_x, jupiter_y, z))

            # saturn values
            saturn_day = earth_day / 10765
            saturn_x = (((sun.get_position()[0] * 2) * math.cos(sun.get_orientation()[2] * saturn_day)) - (
                    sun.get_position()[1] * 2) * math.sin(sun.get_orientation()[2] * saturn_day)) + 1
            saturn_y = (((sun.get_position()[0] * 2) * math.cos(sun.get_orientation()[2] * saturn_day)) + (
                    sun.get_position()[1] * 2) * math.sin(sun.get_orientation()[2] * saturn_day)) + 1

            saturn.set_position(glm.vec3(saturn_x, saturn_y, z))

            # uranus values
            uranus_day = earth_day / 30687
            uranus_x = (((sun.get_position()[0] * 2.3) * math.cos(sun.get_orientation()[2] * uranus_day)) - (
                    sun.get_position()[1] * 2.3) * math.sin(sun.get_orientation()[2] * uranus_day)) + 1
            uranus_y = (((sun.get_position()[0] * 2.3) * math.cos(sun.get_orientation()[2] * uranus_day)) + (
                    sun.get_position()[1] * 2.3) * math.sin(sun.get_orientation()[2] * uranus_day)) + 1

            uranus.set_position(glm.vec3(uranus_x, uranus_y, z))

            # neptune values
            neptune_day = earth_day / 60190
            neptune_x = (((sun.get_position()[0] * 2.6) * math.cos(sun.get_orientation()[2] * neptune_day)) - (
                    sun.get_position()[1] * 2.6) * math.sin(sun.get_orientation()[2] * neptune_day)) + 1
            neptune_y = (((sun.get_position()[0] * 2.6) * math.cos(sun.get_orientation()[2] * neptune_day)) + (
                    sun.get_position()[1] * 2.6) * math.sin(sun.get_orientation()[2] * neptune_day)) + 1

            neptune.set_position(glm.vec3(neptune_x, neptune_y, z))

            # pluto values
            pluto_day = earth_day / 90560
            pluto_x = (((sun.get_position()[0] * 3.2) * math.cos(sun.get_orientation()[2] * pluto_day)) - (
                    sun.get_position()[1] * 3.2) * math.sin(sun.get_orientation()[2] * pluto_day)) + 1
            pluto_y = (((sun.get_position()[0] * 3.2) * math.cos(sun.get_orientation()[2] * pluto_day)) + (
                    sun.get_position()[1] * 3.2) * math.sin(sun.get_orientation()[2] * pluto_day)) + 1

            pluto.set_position(glm.vec3(pluto_x, pluto_y, z))


        if pygame.K_RIGHT in keys_down:
            sun.rotate(glm.vec3(0, 0.001, 0))
            #mercury.rotate(glm.vec3(0, 0.001, 0))
            earth_day = 365
            # mercury values
            mercury_day = earth_day/ 88
            mercury_x = (((sun.get_position()[0] * 0.5) * math.cos(sun.get_orientation()[1] * mercury_day)) + (
                    sun.get_position()[2] * 0.5) * math.sin(sun.get_orientation()[1] * mercury_day)) + 1
            mercury_y = 1
            mercury_z = ((-(sun.get_position()[0] * 0.5) * math.sin(sun.get_orientation()[2] * mercury_day)) + (
                    sun.get_position()[2] * 0.5) * math.cos(sun.get_orientation()[1] * mercury_day)) + 1
            mercury.set_position(glm.vec3(mercury_x, mercury_y, mercury_z))

            # venus values
            venus_day = earth_day / 255
            venus_x = (((sun.get_position()[0] * 0.8) * math.cos(sun.get_orientation()[1] * venus_day)) + (
                    sun.get_position()[2] * 0.8) * math.sin(sun.get_orientation()[1] * venus_day)) + 1
            venus_y = 1
            venus_z = ((-(sun.get_position()[0] * 0.8) * math.sin(sun.get_orientation()[2] * venus_day)) + (
                    sun.get_position()[2] * 0.8) * math.cos(sun.get_orientation()[1] * venus_day)) + 1
            venus.set_position(glm.vec3(venus_x, venus_y, venus_z))

            # earth values
            e_day = earth_day/ 365
            earth_x = (((sun.get_position()[0] * 1.1) * math.cos(sun.get_orientation()[1] * e_day)) + (
                    sun.get_position()[2] * 1.1) * math.sin(sun.get_orientation()[1] * e_day)) + 1
            earth_y = 1
            earth_z = ((-(sun.get_position()[0] * 1.1) * math.sin(sun.get_orientation()[2] * e_day)) + (
                    sun.get_position()[2] * 1.1) * math.cos(sun.get_orientation()[1] * e_day)) + 1
            earth.set_position(glm.vec3(earth_x, earth_y, earth_z))

            # moon values
            earth.rotate(glm.vec3(0,0.01, 0))
            moon_x = (((sun.get_position()[0] * 0.2 ) * math.cos(sun.get_orientation()[1] + earth.get_orientation()[1])) + (
                        sun.get_position()[2] * 0.2) * math.sin(sun.get_orientation()[1] + earth.get_orientation()[1])) + earth_x
            moon_y = 1
            moon_z = ((-(sun.get_position()[0] * 0.2) * math.sin(sun.get_orientation()[2] + earth.get_orientation()[2])) + (
                        sun.get_position()[2] * 0.2) * math.cos(sun.get_orientation()[1] + earth.get_orientation()[2])) + earth_z
            moon.set_position(glm.vec3(moon_x, moon_y, moon_z))


            # mars values
            mars_day = earth_day/ 687
            mars_x = (((sun.get_position()[0] * 1.4) * math.cos(sun.get_orientation()[1] * mars_day)) + (
                    sun.get_position()[2] * 1.4) * math.sin(sun.get_orientation()[1] * mars_day)) + 1
            mars_y = 1
            mars_z = ((-(sun.get_position()[0] * 1.4) * math.sin(sun.get_orientation()[2] * mars_day)) + (
                    sun.get_position()[2] * 1.4) * math.cos(sun.get_orientation()[1] * mars_day)) + 1
            mars.set_position(glm.vec3(mars_x, mars_y, mars_z))

            # jupiter values
            jupiter_day = earth_day / 4333
            jupiter_x = (((sun.get_position()[0] * 1.7) * math.cos(sun.get_orientation()[1] * jupiter_day)) + (
                    sun.get_position()[2] * 1.7) * math.sin(sun.get_orientation()[1] * jupiter_day)) + 1
            jupiter_y = 1
            jupiter_z = ((-(sun.get_position()[0] * 1.7) * math.sin(sun.get_orientation()[2] * jupiter_day)) + (
                    sun.get_position()[2] * 1.7) * math.cos(sun.get_orientation()[1] * jupiter_day)) + 1
            jupiter.set_position(glm.vec3(jupiter_x, jupiter_y, jupiter_z))

            # saturn values
            saturn_day = earth_day / 10765
            saturn_x = (((sun.get_position()[0] * 2) * math.cos(sun.get_orientation()[1] * saturn_day)) + (
                    sun.get_position()[2] * 2) * math.sin(sun.get_orientation()[1] * saturn_day)) + 1
            saturn_y = 1
            saturn_z = ((-(sun.get_position()[0] * 2) * math.sin(sun.get_orientation()[2] * saturn_day)) + (
                    sun.get_position()[2] * 2) * math.cos(sun.get_orientation()[1] * saturn_day)) + 1
            saturn.set_position(glm.vec3(saturn_x, saturn_y, saturn_z))

            # uranus values
            uranus_day = earth_day / 30687
            uranus_x = (((sun.get_position()[0] * 2.3) * math.cos(sun.get_orientation()[1] * uranus_day)) + (
                    sun.get_position()[2] * 2.3) * math.sin(sun.get_orientation()[1] * uranus_day)) + 1
            uranus_y = 1
            uranus_z = ((-(sun.get_position()[0] * 2.3) * math.sin(sun.get_orientation()[2] * uranus_day)) + (
                    sun.get_position()[2] * 2.3) * math.cos(sun.get_orientation()[1] * uranus_day)) + 1
            uranus.set_position(glm.vec3(uranus_x, uranus_y, uranus_z))

            # neptune values
            neptune_day = earth_day / 60190
            neptune_x = (((sun.get_position()[0] * 2.6) * math.cos(sun.get_orientation()[1] * neptune_day)) + (
                        sun.get_position()[2] * 2.6) * math.sin(sun.get_orientation()[1] * neptune_day)) + 1
            neptune_y = 1
            neptune_z = ((-(sun.get_position()[0] * 2.6) * math.sin(sun.get_orientation()[2] * neptune_day)) + (
                        sun.get_position()[2] * 2.6) * math.cos(sun.get_orientation()[1] * neptune_day)) + 1
            neptune.set_position(glm.vec3(neptune_x, neptune_y, neptune_z))

            # pluto values
            pluto_day = earth_day / 90560
            pluto_x = (((sun.get_position()[0] * 3.2) * math.cos(sun.get_orientation()[1] * pluto_day)) + (
                        sun.get_position()[2] * 3.2) * math.sin(sun.get_orientation()[1] * pluto_day)) + 1
            pluto_y = 1
            pluto_z = ((-(sun.get_position()[0] * 3.2) * math.sin(sun.get_orientation()[2] * pluto_day)) + (
                        sun.get_position()[2] * 3.2) * math.cos(sun.get_orientation()[1] * pluto_day)) + 1
            pluto.set_position(glm.vec3(pluto_x, pluto_y, pluto_z))

        elif pygame.K_LEFT in keys_down:
            sun.rotate(glm.vec3(0, -0.001, 0))
            # mercury.rotate(glm.vec3(0, 0.001, 0))
            earth_day = 365
            # mercury values
            mercury_day = earth_day / 88
            mercury_x = (((sun.get_position()[0] * 0.5) * math.cos(sun.get_orientation()[1] * mercury_day)) + (
                    sun.get_position()[2] * 0.5) * math.sin(sun.get_orientation()[1] * mercury_day)) + 1
            mercury_y = 1
            mercury_z = ((-(sun.get_position()[0] * 0.5) * math.sin(sun.get_orientation()[2] * mercury_day)) + (
                    sun.get_position()[2] * 0.5) * math.cos(sun.get_orientation()[1] * mercury_day)) + 1
            mercury.set_position(glm.vec3(mercury_x, mercury_y, mercury_z))

            # venus values
            venus_day = earth_day / 255
            venus_x = (((sun.get_position()[0] * 0.8) * math.cos(sun.get_orientation()[1] * venus_day)) + (
                    sun.get_position()[2] * 0.8) * math.sin(sun.get_orientation()[1] * venus_day)) + 1
            venus_y = 1
            venus_z = ((-(sun.get_position()[0] * 0.8) * math.sin(sun.get_orientation()[2] * venus_day)) + (
                    sun.get_position()[2] * 0.8) * math.cos(sun.get_orientation()[1] * venus_day)) + 1
            venus.set_position(glm.vec3(venus_x, venus_y, venus_z))

            # earth values
            e_day = earth_day / 365
            earth_x = (((sun.get_position()[0] * 1.1) * math.cos(sun.get_orientation()[1] * e_day)) + (
                    sun.get_position()[2] * 1.1) * math.sin(sun.get_orientation()[1] * e_day)) + 1
            earth_y = 1
            earth_z = ((-(sun.get_position()[0] * 1.1) * math.sin(sun.get_orientation()[2] * e_day)) + (
                    sun.get_position()[2] * 1.1) * math.cos(sun.get_orientation()[1] * e_day)) + 1
            earth.set_position(glm.vec3(earth_x, earth_y, earth_z))

            # moon values
            earth.rotate(glm.vec3(0, -0.01, 0))
            moon_x = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[1] + earth.get_orientation()[1])) + (
                              sun.get_position()[2] * 0.2) * math.sin(
                sun.get_orientation()[1] + earth.get_orientation()[1])) + earth_x
            moon_y = 1
            moon_z = ((-(sun.get_position()[0] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + (
                              sun.get_position()[2] * 0.2) * math.cos(
                sun.get_orientation()[1] + earth.get_orientation()[2])) + earth_z
            moon.set_position(glm.vec3(moon_x, moon_y, moon_z))

            # mars values
            mars_day = earth_day / 687
            mars_x = (((sun.get_position()[0] * 1.4) * math.cos(sun.get_orientation()[1] * mars_day)) + (
                    sun.get_position()[2] * 1.4) * math.sin(sun.get_orientation()[1] * mars_day)) + 1
            mars_y = 1
            mars_z = ((-(sun.get_position()[0] * 1.4) * math.sin(sun.get_orientation()[2] * mars_day)) + (
                    sun.get_position()[2] * 1.4) * math.cos(sun.get_orientation()[1] * mars_day)) + 1
            mars.set_position(glm.vec3(mars_x, mars_y, mars_z))

            # jupiter values
            jupiter_day = earth_day / 4333
            jupiter_x = (((sun.get_position()[0] * 1.7) * math.cos(sun.get_orientation()[1] * jupiter_day)) + (
                    sun.get_position()[2] * 1.7) * math.sin(sun.get_orientation()[1] * jupiter_day)) + 1
            jupiter_y = 1
            jupiter_z = ((-(sun.get_position()[0] * 1.7) * math.sin(sun.get_orientation()[2] * jupiter_day)) + (
                    sun.get_position()[2] * 1.7) * math.cos(sun.get_orientation()[1] * jupiter_day)) + 1
            jupiter.set_position(glm.vec3(jupiter_x, jupiter_y, jupiter_z))

            # saturn values
            saturn_day = earth_day / 10765
            saturn_x = (((sun.get_position()[0] * 2) * math.cos(sun.get_orientation()[1] * saturn_day)) + (
                    sun.get_position()[2] * 2) * math.sin(sun.get_orientation()[1] * saturn_day)) + 1
            saturn_y = 1
            saturn_z = ((-(sun.get_position()[0] * 2) * math.sin(sun.get_orientation()[2] * saturn_day)) + (
                    sun.get_position()[2] * 2) * math.cos(sun.get_orientation()[1] * saturn_day)) + 1
            saturn.set_position(glm.vec3(saturn_x, saturn_y, saturn_z))

            # uranus values
            uranus_day = earth_day / 30687
            uranus_x = (((sun.get_position()[0] * 2.3) * math.cos(sun.get_orientation()[1] * uranus_day)) + (
                    sun.get_position()[2] * 2.3) * math.sin(sun.get_orientation()[1] * uranus_day)) + 1
            uranus_y = 1
            uranus_z = ((-(sun.get_position()[0] * 2.3) * math.sin(sun.get_orientation()[2] * uranus_day)) + (
                    sun.get_position()[2] * 2.3) * math.cos(sun.get_orientation()[1] * uranus_day)) + 1
            uranus.set_position(glm.vec3(uranus_x, uranus_y, uranus_z))

            # neptune values
            neptune_day = earth_day / 60190
            neptune_x = (((sun.get_position()[0] * 2.6) * math.cos(sun.get_orientation()[1] * neptune_day)) + (
                    sun.get_position()[2] * 2.6) * math.sin(sun.get_orientation()[1] * neptune_day)) + 1
            neptune_y = 1
            neptune_z = ((-(sun.get_position()[0] * 2.6) * math.sin(sun.get_orientation()[2] * neptune_day)) + (
                    sun.get_position()[2] * 2.6) * math.cos(sun.get_orientation()[1] * neptune_day)) + 1
            neptune.set_position(glm.vec3(neptune_x, neptune_y, neptune_z))

            # pluto values
            pluto_day = earth_day / 90560
            pluto_x = (((sun.get_position()[0] * 3.2) * math.cos(sun.get_orientation()[1] * pluto_day)) + (
                    sun.get_position()[2] * 3.2) * math.sin(sun.get_orientation()[1] * pluto_day)) + 1
            pluto_y = 1
            pluto_z = ((-(sun.get_position()[0] * 3.2) * math.sin(sun.get_orientation()[2] * pluto_day)) + (
                    sun.get_position()[2] * 3.2) * math.cos(sun.get_orientation()[1] * pluto_day)) + 1
            pluto.set_position(glm.vec3(pluto_x, pluto_y, pluto_z))

        #more key commands

        if pygame.K_1 in keys_down:
            sun.rotate(glm.vec3(0, 0, 0.001))
            # earth.rotate(glm.vec3(0, 0, 0.001))
            earth_day = 365  # making the value the base to calculate the speed of the planets around the sun
            # since the sun is at the origin (in the simulation) it will be the base for calculating the distance of each planet from the sun
            # the distance is miles
            num = 100000000  # help distance values smaller for simulation
            # num2 = 1000000000
            # num3 = 10000000000
            # mercury values
            mercury_day = earth_day / 88
            mercury_distance = 29000000 / num
            x = (((sun.get_position()[0] * mercury_distance) * math.cos(sun.get_orientation()[2] * mercury_day)) - (
                        sun.get_position()[1] * mercury_distance) * math.sin(
                sun.get_orientation()[2] * mercury_day)) + 1
            y = (((sun.get_position()[0] * mercury_distance) * math.cos(sun.get_orientation()[2] * mercury_day)) + (
                        sun.get_position()[1] * mercury_distance) * math.sin(
                sun.get_orientation()[2] * mercury_day)) + 1
            z = 1
            mercury.set_position(glm.vec3(x, y, z))

            # venus values
            venus_day = earth_day / 225
            venus_distance = 67000000 / num
            venus_x = (((sun.get_position()[0] * venus_distance) * math.cos(sun.get_orientation()[2] * venus_day)) - (
                        sun.get_position()[1] * venus_distance) * math.sin(sun.get_orientation()[2] * venus_day)) + 1
            venus_y = (((sun.get_position()[0] * venus_distance) * math.cos(sun.get_orientation()[2] * venus_day)) + (
                        sun.get_position()[1] * venus_distance) * math.sin(sun.get_orientation()[2] * venus_day)) + 1

            venus.set_position(glm.vec3(venus_x, venus_y, z))

            # earth values
            e_day = earth_day / 365
            earth_distance = 94000000 / num
            earth_x = (((sun.get_position()[0] * earth_distance) * math.cos(sun.get_orientation()[2] * e_day)) - (
                        sun.get_position()[1] * earth_distance) * math.sin(sun.get_orientation()[2] * e_day)) + 1
            earth_y = (((sun.get_position()[0] * earth_distance) * math.cos(sun.get_orientation()[2] * e_day)) + (
                        sun.get_position()[1] * earth_distance) * math.sin(sun.get_orientation()[2] * e_day)) + 1

            earth.set_position(glm.vec3(earth_x, earth_y, z))

            # moon values
            earth.rotate(glm.vec3(0, 0, 0.01))
            moon_x = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[2] + earth.get_orientation()[2])) - (sun.get_position()[1] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + earth_x
            moon_y = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + (sun.get_position()[1] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + earth_y
            moon_z = 1
            moon.set_position(glm.vec3(moon_x, moon_y, moon_z))

            # mars values
            mars_day = earth_day / 687
            mars_distance = 156000000 / num
            mars_x = (((sun.get_position()[0] * mars_distance) * math.cos(sun.get_orientation()[2] * mars_day)) - (
                        sun.get_position()[1] * mars_distance) * math.sin(sun.get_orientation()[2] * mars_day)) + 1
            mars_y = (((sun.get_position()[0] * mars_distance) * math.cos(sun.get_orientation()[2] * mars_day)) + (
                        sun.get_position()[1] * mars_distance) * math.sin(sun.get_orientation()[2] * mars_day)) + 1

            mars.set_position(glm.vec3(mars_x, mars_y, z))

            # jupiter values
            jupiter_day = earth_day / 4333
            jupiter_distance = 461000000 / num  # 4.61
            jupiter_x = (((sun.get_position()[0] * jupiter_distance) * math.cos(
                sun.get_orientation()[2] * jupiter_day)) - (sun.get_position()[1] * jupiter_distance) * math.sin(
                sun.get_orientation()[2] * jupiter_day)) + 1
            jupiter_y = (((sun.get_position()[0] * jupiter_distance) * math.cos(
                sun.get_orientation()[2] * jupiter_day)) + (sun.get_position()[1] * jupiter_distance) * math.sin(
                sun.get_orientation()[2] * jupiter_day)) + 1

            jupiter.set_position(glm.vec3(jupiter_x, jupiter_y, z))

            # saturn values
            saturn_day = earth_day / 10765
            saturn_distance = 909000000 / num  # 9.09
            saturn_x = (((sun.get_position()[0] * saturn_distance) * math.cos(
                sun.get_orientation()[2] * saturn_day)) - (sun.get_position()[1] * saturn_distance) * math.sin(
                sun.get_orientation()[2] * saturn_day)) + 1
            saturn_y = (((sun.get_position()[0] * saturn_distance) * math.cos(
                sun.get_orientation()[2] * saturn_day)) + (sun.get_position()[1] * saturn_distance) * math.sin(
                sun.get_orientation()[2] * saturn_day)) + 1

            saturn.set_position(glm.vec3(saturn_x, saturn_y, z))

            # uranus values
            uranus_day = earth_day / 30687
            uranus_distance = 1800000000 / num  # 18
            uranus_x = (((sun.get_position()[0] * uranus_distance) * math.cos(
                sun.get_orientation()[2] * uranus_day)) - (sun.get_position()[1] * uranus_distance) * math.sin(
                sun.get_orientation()[2] * uranus_day)) + 1
            uranus_y = (((sun.get_position()[0] * uranus_distance) * math.cos(
                sun.get_orientation()[2] * uranus_day)) + (sun.get_position()[1] * uranus_distance) * math.sin(
                sun.get_orientation()[2] * uranus_day)) + 1

            uranus.set_position(glm.vec3(uranus_x, uranus_y, z))

            # neptune values
            neptune_day = earth_day / 60190
            neptune_distance = 2780000000 / num  # 27.8
            neptune_x = (((sun.get_position()[0] * neptune_distance) * math.cos(
                sun.get_orientation()[2] * neptune_day)) - (sun.get_position()[1] * neptune_distance) * math.sin(
                sun.get_orientation()[2] * neptune_day)) + 1
            neptune_y = (((sun.get_position()[0] * neptune_distance) * math.cos(
                sun.get_orientation()[2] * neptune_day)) + (sun.get_position()[1] * neptune_distance) * math.sin(
                sun.get_orientation()[2] * neptune_day)) + 1

            neptune.set_position(glm.vec3(neptune_x, neptune_y, z))

            # pluto values
            pluto_day = earth_day / 90560
            pluto_distance = 3700000000 / num  # 37
            pluto_x = (((sun.get_position()[0] * pluto_distance) * math.cos(sun.get_orientation()[2] * pluto_day)) - (
                        sun.get_position()[1] * pluto_distance) * math.sin(sun.get_orientation()[2] * pluto_day)) + 1
            pluto_y = (((sun.get_position()[0] * pluto_distance) * math.cos(sun.get_orientation()[2] * pluto_day)) + (
                        sun.get_position()[1] * pluto_distance) * math.sin(sun.get_orientation()[2] * pluto_day)) + 1

            pluto.set_position(glm.vec3(pluto_x, pluto_y, z))

        elif pygame.K_2 in keys_down:
            sun.rotate(glm.vec3(0, 0, -0.001))
            # earth.rotate(glm.vec3(0, 0, 0.001))
            earth_day = 365  # making the value the base to calculate the speed of the planets around the sun
            # since the sun is at the origin (in the simulation) it will be the base for calculating the distance of each planet from the sun
            # the distance is miles
            num = 100000000  # help distance values smaller for simulation
            # num2 = 1000000000
            # num3 = 10000000000
            # mercury values
            mercury_day = earth_day / 88
            mercury_distance = 29000000 / num
            x = (((sun.get_position()[0] * mercury_distance) * math.cos(sun.get_orientation()[2] * mercury_day)) - (
                    sun.get_position()[1] * mercury_distance) * math.sin(
                sun.get_orientation()[2] * mercury_day)) + 1
            y = (((sun.get_position()[0] * mercury_distance) * math.cos(sun.get_orientation()[2] * mercury_day)) + (
                    sun.get_position()[1] * mercury_distance) * math.sin(
                sun.get_orientation()[2] * mercury_day)) + 1
            z = 1
            mercury.set_position(glm.vec3(x, y, z))

            # venus values
            venus_day = earth_day / 225
            venus_distance = 67000000 / num
            venus_x = (((sun.get_position()[0] * venus_distance) * math.cos(sun.get_orientation()[2] * venus_day)) - (
                    sun.get_position()[1] * venus_distance) * math.sin(sun.get_orientation()[2] * venus_day)) + 1
            venus_y = (((sun.get_position()[0] * venus_distance) * math.cos(sun.get_orientation()[2] * venus_day)) + (
                    sun.get_position()[1] * venus_distance) * math.sin(sun.get_orientation()[2] * venus_day)) + 1

            venus.set_position(glm.vec3(venus_x, venus_y, z))

            # earth values
            e_day = earth_day / 365
            earth_distance = 94000000 / num
            earth_x = (((sun.get_position()[0] * earth_distance) * math.cos(sun.get_orientation()[2] * e_day)) - (
                    sun.get_position()[1] * earth_distance) * math.sin(sun.get_orientation()[2] * e_day)) + 1
            earth_y = (((sun.get_position()[0] * earth_distance) * math.cos(sun.get_orientation()[2] * e_day)) + (
                    sun.get_position()[1] * earth_distance) * math.sin(sun.get_orientation()[2] * e_day)) + 1

            earth.set_position(glm.vec3(earth_x, earth_y, z))

            # moon values
            earth.rotate(glm.vec3(0, 0, -0.01))
            moon_x = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[2] + earth.get_orientation()[2])) - (sun.get_position()[1] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + earth_x
            moon_y = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + (sun.get_position()[1] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + earth_y
            moon_z = 1
            moon.set_position(glm.vec3(moon_x, moon_y, moon_z))

            # mars values
            mars_day = earth_day / 687
            mars_distance = 156000000 / num
            mars_x = (((sun.get_position()[0] * mars_distance) * math.cos(sun.get_orientation()[2] * mars_day)) - (
                    sun.get_position()[1] * mars_distance) * math.sin(sun.get_orientation()[2] * mars_day)) + 1
            mars_y = (((sun.get_position()[0] * mars_distance) * math.cos(sun.get_orientation()[2] * mars_day)) + (
                    sun.get_position()[1] * mars_distance) * math.sin(sun.get_orientation()[2] * mars_day)) + 1

            mars.set_position(glm.vec3(mars_x, mars_y, z))

            # jupiter values
            jupiter_day = earth_day / 4333
            jupiter_distance = 461000000 / num  # 4.61
            jupiter_x = (((sun.get_position()[0] * jupiter_distance) * math.cos(
                sun.get_orientation()[2] * jupiter_day)) - (sun.get_position()[1] * jupiter_distance) * math.sin(
                sun.get_orientation()[2] * jupiter_day)) + 1
            jupiter_y = (((sun.get_position()[0] * jupiter_distance) * math.cos(
                sun.get_orientation()[2] * jupiter_day)) + (sun.get_position()[1] * jupiter_distance) * math.sin(
                sun.get_orientation()[2] * jupiter_day)) + 1

            jupiter.set_position(glm.vec3(jupiter_x, jupiter_y, z))

            # saturn values
            saturn_day = earth_day / 10765
            saturn_distance = 909000000 / num  # 9.09
            saturn_x = (((sun.get_position()[0] * saturn_distance) * math.cos(
                sun.get_orientation()[2] * saturn_day)) - (sun.get_position()[1] * saturn_distance) * math.sin(
                sun.get_orientation()[2] * saturn_day)) + 1
            saturn_y = (((sun.get_position()[0] * saturn_distance) * math.cos(
                sun.get_orientation()[2] * saturn_day)) + (sun.get_position()[1] * saturn_distance) * math.sin(
                sun.get_orientation()[2] * saturn_day)) + 1

            saturn.set_position(glm.vec3(saturn_x, saturn_y, z))

            # uranus values
            uranus_day = earth_day / 30687
            uranus_distance = 1800000000 / num  # 18
            uranus_x = (((sun.get_position()[0] * uranus_distance) * math.cos(
                sun.get_orientation()[2] * uranus_day)) - (sun.get_position()[1] * uranus_distance) * math.sin(
                sun.get_orientation()[2] * uranus_day)) + 1
            uranus_y = (((sun.get_position()[0] * uranus_distance) * math.cos(
                sun.get_orientation()[2] * uranus_day)) + (sun.get_position()[1] * uranus_distance) * math.sin(
                sun.get_orientation()[2] * uranus_day)) + 1

            uranus.set_position(glm.vec3(uranus_x, uranus_y, z))

            # neptune values
            neptune_day = earth_day / 60190
            neptune_distance = 2780000000 / num  # 27.8
            neptune_x = (((sun.get_position()[0] * neptune_distance) * math.cos(
                sun.get_orientation()[2] * neptune_day)) - (sun.get_position()[1] * neptune_distance) * math.sin(
                sun.get_orientation()[2] * neptune_day)) + 1
            neptune_y = (((sun.get_position()[0] * neptune_distance) * math.cos(
                sun.get_orientation()[2] * neptune_day)) + (sun.get_position()[1] * neptune_distance) * math.sin(
                sun.get_orientation()[2] * neptune_day)) + 1

            neptune.set_position(glm.vec3(neptune_x, neptune_y, z))

            # pluto values
            pluto_day = earth_day / 90560
            pluto_distance = 3700000000 / num  # 37
            pluto_x = (((sun.get_position()[0] * pluto_distance) * math.cos(sun.get_orientation()[2] * pluto_day)) - (
                    sun.get_position()[1] * pluto_distance) * math.sin(sun.get_orientation()[2] * pluto_day)) + 1
            pluto_y = (((sun.get_position()[0] * pluto_distance) * math.cos(sun.get_orientation()[2] * pluto_day)) + (
                    sun.get_position()[1] * pluto_distance) * math.sin(sun.get_orientation()[2] * pluto_day)) + 1

            pluto.set_position(glm.vec3(pluto_x, pluto_y, z))

        if pygame.K_3 in keys_down:
            sun.rotate(glm.vec3(0, 0.001, 0))
            # mercury.rotate(glm.vec3(0, 0.001, 0))
            earth_day = 365
            num = 100000000

            # mercury values
            mercury_day = earth_day / 88
            mercury_distance = 29000000 / num
            mercury_x = (((sun.get_position()[0] * mercury_distance) * math.cos(sun.get_orientation()[1] * mercury_day)) + (
                    sun.get_position()[2] * mercury_distance) * math.sin(sun.get_orientation()[1] * mercury_day)) + 1
            mercury_y = 1
            mercury_z = ((-(sun.get_position()[0] * mercury_distance) * math.sin(sun.get_orientation()[2] * mercury_day)) + (
                    sun.get_position()[2] * mercury_distance) * math.cos(sun.get_orientation()[1] * mercury_day)) + 1
            mercury.set_position(glm.vec3(mercury_x, mercury_y, mercury_z))

            # venus values
            venus_day = earth_day / 255
            venus_distance = 67000000 / num
            venus_x = (((sun.get_position()[0] * venus_distance) * math.cos(sun.get_orientation()[1] * venus_day)) + (
                    sun.get_position()[2] * venus_distance) * math.sin(sun.get_orientation()[1] * venus_day)) + 1
            venus_y = 1
            venus_z = ((-(sun.get_position()[0] * venus_distance) * math.sin(sun.get_orientation()[2] * venus_day)) + (
                    sun.get_position()[2] * venus_distance) * math.cos(sun.get_orientation()[1] * venus_day)) + 1
            venus.set_position(glm.vec3(venus_x, venus_y, venus_z))

            # earth values
            e_day = earth_day / 365
            earth_distance = 94000000 / num
            earth_x = (((sun.get_position()[0] * earth_distance) * math.cos(sun.get_orientation()[1] * e_day)) + (
                    sun.get_position()[2] * earth_distance) * math.sin(sun.get_orientation()[1] * e_day)) + 1
            earth_y = 1
            earth_z = ((-(sun.get_position()[0] * earth_distance) * math.sin(sun.get_orientation()[2] * e_day)) + (
                    sun.get_position()[2] * earth_distance) * math.cos(sun.get_orientation()[1] * e_day)) + 1
            earth.set_position(glm.vec3(earth_x, earth_y, earth_z))

            # moon values
            earth.rotate(glm.vec3(0, 0.01, 0))
            moon_x = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[1] + earth.get_orientation()[1])) + (
                              sun.get_position()[2] * 0.2) * math.sin(
                sun.get_orientation()[1] + earth.get_orientation()[1])) + earth_x
            moon_y = 1
            moon_z = ((-(sun.get_position()[0] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + (
                              sun.get_position()[2] * 0.2) * math.cos(
                sun.get_orientation()[1] + earth.get_orientation()[2])) + earth_z
            moon.set_position(glm.vec3(moon_x, moon_y, moon_z))

            # mars values
            mars_day = earth_day / 687
            mars_distance = 156000000 / num
            mars_x = (((sun.get_position()[0] * mars_distance) * math.cos(sun.get_orientation()[1] * mars_day)) + (
                    sun.get_position()[2] * mars_distance) * math.sin(sun.get_orientation()[1] * mars_day)) + 1
            mars_y = 1
            mars_z = ((-(sun.get_position()[0] * mars_distance) * math.sin(sun.get_orientation()[2] * mars_day)) + (
                    sun.get_position()[2] * mars_distance) * math.cos(sun.get_orientation()[1] * mars_day)) + 1
            mars.set_position(glm.vec3(mars_x, mars_y, mars_z))

            # jupiter values
            jupiter_day = earth_day / 4333
            jupiter_distance = 461000000 / num  # 4.61
            jupiter_x = (((sun.get_position()[0] * jupiter_distance) * math.cos(sun.get_orientation()[1] * jupiter_day)) + (
                    sun.get_position()[2] * jupiter_distance) * math.sin(sun.get_orientation()[1] * jupiter_day)) + 1
            jupiter_y = 1
            jupiter_z = ((-(sun.get_position()[0] * jupiter_distance) * math.sin(sun.get_orientation()[2] * jupiter_day)) + (
                    sun.get_position()[2] * jupiter_distance) * math.cos(sun.get_orientation()[1] * jupiter_day)) + 1
            jupiter.set_position(glm.vec3(jupiter_x, jupiter_y, jupiter_z))

            # saturn values
            saturn_day = earth_day / 10765
            saturn_distance = 909000000 / num  # 9.09
            saturn_x = (((sun.get_position()[0] * saturn_distance) * math.cos(sun.get_orientation()[1] * saturn_day)) + (
                    sun.get_position()[2] * saturn_distance) * math.sin(sun.get_orientation()[1] * saturn_day)) + 1
            saturn_y = 1
            saturn_z = ((-(sun.get_position()[0] * saturn_distance) * math.sin(sun.get_orientation()[2] * saturn_day)) + (
                    sun.get_position()[2] * saturn_distance) * math.cos(sun.get_orientation()[1] * saturn_day)) + 1
            saturn.set_position(glm.vec3(saturn_x, saturn_y, saturn_z))

            # uranus values
            uranus_day = earth_day / 30687
            uranus_distance = 1800000000 / num  # 18
            uranus_x = (((sun.get_position()[0] * uranus_distance) * math.cos(sun.get_orientation()[1] * uranus_day)) + (
                    sun.get_position()[2] * uranus_distance) * math.sin(sun.get_orientation()[1] * uranus_day)) + 1
            uranus_y = 1
            uranus_z = ((-(sun.get_position()[0] * uranus_distance) * math.sin(sun.get_orientation()[2] * uranus_day)) + (
                    sun.get_position()[2] * uranus_distance) * math.cos(sun.get_orientation()[1] * uranus_day)) + 1
            uranus.set_position(glm.vec3(uranus_x, uranus_y, uranus_z))

            # neptune values
            neptune_day = earth_day / 60190
            neptune_distance = 2780000000 / num  # 27.8
            neptune_x = (((sun.get_position()[0] * neptune_distance) * math.cos(sun.get_orientation()[1] * neptune_day)) + (
                    sun.get_position()[2] * neptune_distance) * math.sin(sun.get_orientation()[1] * neptune_day)) + 1
            neptune_y = 1
            neptune_z = ((-(sun.get_position()[0] * neptune_distance) * math.sin(sun.get_orientation()[2] * neptune_day)) + (
                    sun.get_position()[2] * neptune_distance) * math.cos(sun.get_orientation()[1] * neptune_day)) + 1
            neptune.set_position(glm.vec3(neptune_x, neptune_y, neptune_z))

            # pluto values
            pluto_day = earth_day / 90560
            pluto_distance = 3700000000 / num  # 37
            pluto_x = (((sun.get_position()[0] * pluto_distance) * math.cos(sun.get_orientation()[1] * pluto_day)) + (
                    sun.get_position()[2] * pluto_distance) * math.sin(sun.get_orientation()[1] * pluto_day)) + 1
            pluto_y = 1
            pluto_z = ((-(sun.get_position()[0] * pluto_distance) * math.sin(sun.get_orientation()[2] * pluto_day)) + (
                    sun.get_position()[2] * pluto_distance) * math.cos(sun.get_orientation()[1] * pluto_day)) + 1
            pluto.set_position(glm.vec3(pluto_x, pluto_y, pluto_z))

        elif pygame.K_4 in keys_down:
            sun.rotate(glm.vec3(0, -0.001, 0))
            # mercury.rotate(glm.vec3(0, 0.001, 0))
            earth_day = 365
            num = 100000000

            # mercury values
            mercury_day = earth_day / 88
            mercury_distance = 29000000 / num
            mercury_x = (((sun.get_position()[0] * mercury_distance) * math.cos(
                sun.get_orientation()[1] * mercury_day)) + (
                                 sun.get_position()[2] * mercury_distance) * math.sin(
                sun.get_orientation()[1] * mercury_day)) + 1
            mercury_y = 1
            mercury_z = ((-(sun.get_position()[0] * mercury_distance) * math.sin(
                sun.get_orientation()[2] * mercury_day)) + (
                                 sun.get_position()[2] * mercury_distance) * math.cos(
                sun.get_orientation()[1] * mercury_day)) + 1
            mercury.set_position(glm.vec3(mercury_x, mercury_y, mercury_z))

            # venus values
            venus_day = earth_day / 255
            venus_distance = 67000000 / num
            venus_x = (((sun.get_position()[0] * venus_distance) * math.cos(sun.get_orientation()[1] * venus_day)) + (
                    sun.get_position()[2] * venus_distance) * math.sin(sun.get_orientation()[1] * venus_day)) + 1
            venus_y = 1
            venus_z = ((-(sun.get_position()[0] * venus_distance) * math.sin(sun.get_orientation()[2] * venus_day)) + (
                    sun.get_position()[2] * venus_distance) * math.cos(sun.get_orientation()[1] * venus_day)) + 1
            venus.set_position(glm.vec3(venus_x, venus_y, venus_z))

            # earth values
            e_day = earth_day / 365
            earth_distance = 94000000 / num
            earth_x = (((sun.get_position()[0] * earth_distance) * math.cos(sun.get_orientation()[1] * e_day)) + (
                    sun.get_position()[2] * earth_distance) * math.sin(sun.get_orientation()[1] * e_day)) + 1
            earth_y = 1
            earth_z = ((-(sun.get_position()[0] * earth_distance) * math.sin(sun.get_orientation()[2] * e_day)) + (
                    sun.get_position()[2] * earth_distance) * math.cos(sun.get_orientation()[1] * e_day)) + 1
            earth.set_position(glm.vec3(earth_x, earth_y, earth_z))

            # moon values
            earth.rotate(glm.vec3(0, -0.01, 0))
            moon_x = (((sun.get_position()[0] * 0.2) * math.cos(
                sun.get_orientation()[1] + earth.get_orientation()[1])) + (
                              sun.get_position()[2] * 0.2) * math.sin(
                sun.get_orientation()[1] + earth.get_orientation()[1])) + earth_x
            moon_y = 1
            moon_z = ((-(sun.get_position()[0] * 0.2) * math.sin(
                sun.get_orientation()[2] + earth.get_orientation()[2])) + (
                              sun.get_position()[2] * 0.2) * math.cos(
                sun.get_orientation()[1] + earth.get_orientation()[2])) + earth_z
            moon.set_position(glm.vec3(moon_x, moon_y, moon_z))

            # mars values
            mars_day = earth_day / 687
            mars_distance = 156000000 / num
            mars_x = (((sun.get_position()[0] * mars_distance) * math.cos(sun.get_orientation()[1] * mars_day)) + (
                    sun.get_position()[2] * mars_distance) * math.sin(sun.get_orientation()[1] * mars_day)) + 1
            mars_y = 1
            mars_z = ((-(sun.get_position()[0] * mars_distance) * math.sin(sun.get_orientation()[2] * mars_day)) + (
                    sun.get_position()[2] * mars_distance) * math.cos(sun.get_orientation()[1] * mars_day)) + 1
            mars.set_position(glm.vec3(mars_x, mars_y, mars_z))

            # jupiter values
            jupiter_day = earth_day / 4333
            jupiter_distance = 461000000 / num  # 4.61
            jupiter_x = (((sun.get_position()[0] * jupiter_distance) * math.cos(
                sun.get_orientation()[1] * jupiter_day)) + (
                                 sun.get_position()[2] * jupiter_distance) * math.sin(
                sun.get_orientation()[1] * jupiter_day)) + 1
            jupiter_y = 1
            jupiter_z = ((-(sun.get_position()[0] * jupiter_distance) * math.sin(
                sun.get_orientation()[2] * jupiter_day)) + (
                                 sun.get_position()[2] * jupiter_distance) * math.cos(
                sun.get_orientation()[1] * jupiter_day)) + 1
            jupiter.set_position(glm.vec3(jupiter_x, jupiter_y, jupiter_z))

            # saturn values
            saturn_day = earth_day / 10765
            saturn_distance = 909000000 / num  # 9.09
            saturn_x = (((sun.get_position()[0] * saturn_distance) * math.cos(
                sun.get_orientation()[1] * saturn_day)) + (
                                sun.get_position()[2] * saturn_distance) * math.sin(
                sun.get_orientation()[1] * saturn_day)) + 1
            saturn_y = 1
            saturn_z = ((-(sun.get_position()[0] * saturn_distance) * math.sin(
                sun.get_orientation()[2] * saturn_day)) + (
                                sun.get_position()[2] * saturn_distance) * math.cos(
                sun.get_orientation()[1] * saturn_day)) + 1
            saturn.set_position(glm.vec3(saturn_x, saturn_y, saturn_z))

            # uranus values
            uranus_day = earth_day / 30687
            uranus_distance = 1800000000 / num  # 18
            uranus_x = (((sun.get_position()[0] * uranus_distance) * math.cos(
                sun.get_orientation()[1] * uranus_day)) + (
                                sun.get_position()[2] * uranus_distance) * math.sin(
                sun.get_orientation()[1] * uranus_day)) + 1
            uranus_y = 1
            uranus_z = ((-(sun.get_position()[0] * uranus_distance) * math.sin(
                sun.get_orientation()[2] * uranus_day)) + (
                                sun.get_position()[2] * uranus_distance) * math.cos(
                sun.get_orientation()[1] * uranus_day)) + 1
            uranus.set_position(glm.vec3(uranus_x, uranus_y, uranus_z))

            # neptune values
            neptune_day = earth_day / 60190
            neptune_distance = 2780000000 / num  # 27.8
            neptune_x = (((sun.get_position()[0] * neptune_distance) * math.cos(
                sun.get_orientation()[1] * neptune_day)) + (
                                 sun.get_position()[2] * neptune_distance) * math.sin(
                sun.get_orientation()[1] * neptune_day)) + 1
            neptune_y = 1
            neptune_z = ((-(sun.get_position()[0] * neptune_distance) * math.sin(
                sun.get_orientation()[2] * neptune_day)) + (
                                 sun.get_position()[2] * neptune_distance) * math.cos(
                sun.get_orientation()[1] * neptune_day)) + 1
            neptune.set_position(glm.vec3(neptune_x, neptune_y, neptune_z))

            # pluto values
            pluto_day = earth_day / 90560
            pluto_distance = 3700000000 / num  # 37
            pluto_x = (((sun.get_position()[0] * pluto_distance) * math.cos(sun.get_orientation()[1] * pluto_day)) + (
                    sun.get_position()[2] * pluto_distance) * math.sin(sun.get_orientation()[1] * pluto_day)) + 1
            pluto_y = 1
            pluto_z = ((-(sun.get_position()[0] * pluto_distance) * math.sin(sun.get_orientation()[2] * pluto_day)) + (
                    sun.get_position()[2] * pluto_distance) * math.cos(sun.get_orientation()[1] * pluto_day)) + 1
            pluto.set_position(glm.vec3(pluto_x, pluto_y, pluto_z))

        if pygame.K_w in keys_down:
            (camera.__getitem__(3))[2] += 0.01
        elif pygame.K_s in keys_down:
            (camera.__getitem__(3))[2] += -0.01
        if pygame.K_a in keys_down:
            (camera.__getitem__(3))[0] += 0.01
        elif pygame.K_d in keys_down:
            (camera.__getitem__(3))[0] += -0.01
        if pygame.K_SPACE in keys_down:
            (camera.__getitem__(3))[1] += -0.01
        elif pygame.K_LSHIFT in keys_down:
            (camera.__getitem__(3))[1] += 0.01
        # elif pygame.K_SPACE in keys_down:
        #    spin = not spin

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if spin:
            light.rotate(glm.vec3(0, 0.001, 0))
        renderer.set_uniform("pointPosition", light.get_position(), glm.vec3)

        # mesh.rotate(glm.vec3(0.01, 0.01, 0.01))
        # Render the scene given the perspective and camera matrices.
        renderer.set_uniform("pointColor", glm.vec3(1, 1, 1), glm.vec3)
        renderer.render(perspective, camera,
                        [sun, mercury, venus, earth, moon, mars, jupiter, saturn, uranus, neptune, pluto])
        renderer.set_uniform("pointColor", glm.vec3(0, 0, 0), glm.vec3)
        renderer.render(perspective, camera, [sun])

        pygame.display.flip()
        end = time.perf_counter()
        frames += 1
        # print(f"{frames/(end - start)} FPS")

    pygame.quit()