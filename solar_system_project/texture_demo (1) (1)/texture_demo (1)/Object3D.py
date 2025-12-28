from OpenGL.GL import *
import glm
import math

# An object in 3D space, with a mesh, position, orientation (yaw/pitch/roll),
# and scale.
class Object3D:
    def __init__(
        self,
        mesh,
        position: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        orientation: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        center: glm.vec3 = glm.vec3(0, 0, 0)
    ):
        self.mesh = mesh
        self.position = position
        self.orientation = orientation
        self.scale = scale
        self.center = center
        self._refresh_model_matrix()

    def move(self, offset: glm.vec3):
        """
        Moves the object along the given vector.
        """
        self.position = self.position + offset
        self._refresh_model_matrix()

    def rotate(self, rot: glm.vec3):
        """
        Adds the given yaw,pitch,roll values to the object's current orientation.
        """
        self.orientation = self.orientation + rot
        self._refresh_model_matrix()

    def grow(self, sc: glm.vec3):
        """
        Multiplies the object's current scale by the given x,y,z scale values.
        """
        self.scale = self.scale * sc
        self._refresh_model_matrix()

    def center_point(self, center: glm.vec3):
        self.center = center
        self._refresh_model_matrix()

    def get_position(self):
        return self.position + self.center

    def get_orientation(self):
        return self.orientation

    def set_orientation(self, orientation: glm.vec3):
        self.orientation = orientation
        self._refresh_model_matrix()


    def set_position(self, position: glm.vec3):
        self.position = position
        self._refresh_model_matrix()

    def get_model_matrix(self):
        """
        Retrieve the object's current Model transformation matrix.
        """
        return self.model_matrix

    def _refresh_model_matrix(self):
        m = glm.translate(glm.mat4(1), self.position)
        m = glm.rotate(m, self.orientation[1], glm.vec3(0, 1, 0))
        m = glm.rotate(m, self.orientation[0], glm.vec3(1, 0, 0))
        m = glm.rotate(m, self.orientation[2], glm.vec3(0, 0, 2))
        m = glm.scale(m, self.scale)
        m = glm.translate(m, -1 * self.center)
        self.model_matrix = m
        # self.model_matrix = glm.translate(
        #     glm.rotate(
        #         glm.rotate(
        #             glm.rotate(
        #                 glm.scale(glm.mat4(1), self.scale),
        #                 self.orientation[1],
        #                 glm.vec3(0, 1, 0),
        #             ),
        #             self.orientation[0],
        #             glm.vec3(1, 0, 0),
        #         ),
        #         self.orientation[2],
        #         glm.vec3(0, 0, 1),
        #     ),
        #     self.position,
        # )
        # self.model_matrix = glm.scale(
        #     glm.rotate(
        #         glm.rotate(
        #             glm.rotate(
        #                 glm.translate(glm.mat4(1), self.position),
        #                 math.radians(self.orientation[2]),
        #                 glm.vec3(0, 0, 1),
        #             ),
        #             math.radians(self.orientation[0]),
        #             glm.vec3(1, 0, 0),
        #         ),
        #         math.radians(self.orientation[1]),
        #         glm.vec3(0, 1, 0),
        #     ),
        #     self.position,
        # )


    def draw(self):
        self.mesh.draw()
