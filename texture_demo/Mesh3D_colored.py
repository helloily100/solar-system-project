from OpenGL.GL import *
from numpy import array
import pygame
import ctypes


class Mesh3D:
    """
    Represents a 3D mesh using an OpenGL vertex buffer + attrib array to
    store the vertices and faces. Stores rgb colors for each vertex.
    """

    # NEW REQUIREMENTS:
    # vertices MUST BE a single-dimension numpy array, the coordinates of each vertex placed one after the next.
    # faces must also be a 1D numpy array, the three indices of the triangle's verices placed one after the next.
    # See cube() and square() below.
    def __init__(self, vertices, faces):
        self.vao = Mesh3D.get_vao(vertices, faces)
        self.fcount = len(faces)

    def draw(self, mode=GL_TRIANGLES):
        """
        Draws the mesh by binding its VAO and then triggering glDrawElements.
        """
        glBindVertexArray(self.vao)
        glDrawElements(mode, self.fcount, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    @staticmethod
    def get_vao(vertices, faces, usage=GL_STATIC_DRAW):
        """
        Gets a Vertex Array Object for this mesh -- an encapsulation of the mesh's vertices
        and the indexes forming its triangle faces.
        """

        # Generate and bind a VAO for this mesh, so that all future calls are associated with this VAO.
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        # Generate and bind a buffer to hold the positions of the vertices.
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)

        # Each vertex has 12 bytes of position and 12 bytes of color.
        stride = 24

        position_location = 0
        glEnableVertexAttribArray(position_location)
        glVertexAttribPointer(
            position_location, 3, GL_FLOAT, False, stride, ctypes.c_void_p(0)
        )

        color_location = 1
        glEnableVertexAttribArray(color_location)
        # Tell OpenGL that the color of each vertex is 3 floats in size,
        # and is found by skipping 12 bytes at the start of the vertex.
        glVertexAttribPointer(
            color_location, 3, GL_FLOAT, False, stride, ctypes.c_void_p(12)
        )

        # Specify the numpy array to use as the source of the vertex data.
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, usage)

        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, usage)

        # Unbind this buffer so no one else messes with it.
        #glBindVertexArray(0)
        #glDisableVertexAttribArray(position_location)
        #glBindBuffer(GL_ARRAY_BUFFER, 0)
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        return vao

    @staticmethod
    def square():
        # fmt: off
        return Mesh3D(
            array(
                [
                    0.5, -0.5, 0.5, 1, 0, 0,
                    -0.5, -0.5,0.5, 1, 0, 0,
                    0.5, 0.5, 0.5, 1, 0, 0,
                    -0.5, 0.5, 0.5, 1, 0, 0,
                    0.5, 0.5, -0.5, 1, 0, 0,
                    -0.5, 0.5, -0.5, 1, 0, 0,
                ],
                dtype="float32",
            ),
            array([[0, 2, 3], [0, 3, 1]], dtype="uint32"),
        )
        # fmt: on

    @staticmethod
    def cube():
        # fmt: off
        verts = [
            0.5, 0.5, -0.5, 1, 0, 0,
            -0.5, 0.5, -0.5, 1, 1, 1,
            -0.5, -0.5, -0.5, 1, 1, 1,
            0.5, -0.5, -0.5, 1, 1, 1, 
            0.5, 0.5, 0.5, 1, 1, 1, 
            -0.5, 0.5, 0.5, 1, 1, 1,
            -0.5, -0.5, 0.5, 1, 1, 1,
            0.5,- 0.5, 0.5, 1, 1, 1,
        ]
        # more colors to the vertices
        # verts = [
        #     0.5, 0.5, -0.5, 1, 0, 0,
        #     -0.5, 0.5, -0.5, 1, 1, 1,
        #     -0.5,
        #     -0.5,
        #     -0.5,
        #     0,
        #     1,
        #     0,
        #     0.5,
        #     -0.5,
        #     -0.5,
        #     0,
        #     0,
        #     1,
        #     0.5,
        #     0.5,
        #     0.5,
        #     1,
        #     1,
        #     1,
        #     -0.5,
        #     0.5,
        #     0.5,
        #     0,
        #     0,
        #     0,
        #     -0.5,
        #     -0.5,
        #     0.5,
        #     1,
        #     1,
        #     0,
        #     0.5,
        #     -0.5,
        #     0.5,
        #     1,
        #     0,
        #     1,
        # ]
        tris = [
            0,
            1,
            2,
            0,
            2,
            3,
            4,
            0,
            3,
            4,
            3,
            7,
            5,
            4,
            7,
            5,
            7,
            6,
            1,
            5,
            6,
            1,
            6,
            2,
            4,
            5,
            1,
            4,
            1,
            0,
            2,
            6,
            7,
            2,
            7,
            3,
        ]

        return Mesh3D(array(verts, "float32"), array(tris, "uint32"))
        # fmt: on

    @staticmethod
    def red_cube():
        verts = [
            0.5,
            0.5,
            -0.5,
            1,
            0,
            0,
            -0.5,
            0.5,
            -0.5,
            1,
            0,
            0,
            -0.5,
            -0.5,
            -0.5,
            1,
            0,
            0,
            0.5,
            -0.5,
            -0.5,
            1,
            0,
            0,
            0.5,
            0.5,
            0.5,
            1,
            0,
            0,
            -0.5,
            0.5,
            0.5,
            1,
            0,
            0,
            -0.5,
            -0.5,
            0.5,
            1,
            0,
            0,
            0.5,
            -0.5,
            0.5,
            1,
            0,
            0,
        ]
        tris = [
            0,
            1,
            2,
            0,
            2,
            3,
            4,
            0,
            3,
            4,
            3,
            7,
            5,
            4,
            7,
            5,
            7,
            6,
            1,
            5,
            6,
            1,
            6,
            2,
            4,
            5,
            1,
            4,
            1,
            0,
            2,
            6,
            7,
            2,
            7,
            3,
        ]

        return Mesh3D(array(verts, "float32"), array(tris, "uint32"))

    @staticmethod
    def load_obj(file) -> "Mesh3D":
        verts = []
        faces = []
        for line in file:
            if line[0] == "#":
                continue
            sp = line.split(" ")
            if line[0] == "v":
                verts.append(float(sp[1]))
                verts.append(float(sp[2]))
                verts.append(float(sp[3]))
                # default color the vertex white
                verts.append(1.0)
                verts.append(1.0)
                verts.append(1.0)
            elif line[0] == "f":
                faces.append(int(sp[1]) - 1)
                faces.append(int(sp[2]) - 1)
                faces.append(int(sp[3]) - 1)
        return Mesh3D(array(verts, "float32"), array(faces, "uint32"))
