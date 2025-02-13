'''
                                                
   Code framework for the lecture

   "CV804: 3D Geometry Processing"

   Lecturer: Hao Li
   TAs: Phong Tran, Long Nhat Ho, Ekaterina Radionova

   Copyright (C) 2025 by  Metaverse Lab, MBZUAI
                                                                         
-----------------------------------------------------------------------------
                                                                            
                                License                                     
                                                                            
   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License
   as published by the Free Software Foundation; either version 2
   of the License, or (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, 
   Boston, MA  02110-1301, USA.
'''


from OpenGL.GL import *
import numpy as np
import pyrr

from base_entity import BaseEntity


class BoxFaceEntity(BaseEntity):
    VERTEX_SHADER_PATH = './shaders/box_face.vert'
    FRAGMENT_SHADER_PATH = './shaders/box_face.frag'

    def __init__(self, texture_path, texture_unit):
        super().__init__()

        self.texture_unit = texture_unit
        self._build_vertex_data()
        self._shader_program = self._create_shader(self.VERTEX_SHADER_PATH, self.FRAGMENT_SHADER_PATH)

        # Pass texture to fragment shader
        self.texture = self._load_texture(texture_path, texture_unit)
        glUseProgram(self._shader_program)
        glUniform1i(glGetUniformLocation(self._shader_program, "texture0"), texture_unit)

    def _build_vertex_data(self):
        '''
            Build vertex data, including position, texture coordinate, and the drawing indices.
            
            Hint:
                - Step 1: Create the vertices. It should be the vertices of 2 triangles that combined into a square. Each tuple in the vertices should contain 6 values: xyz coordinate of the vertex and st coordinate of the texture
                - Step 2: Create the drawing indices. If you use GL_TRIANGLES, it has 6 values. On the other hand, if you use GL_TRIANGLE_STRIP, it only has 4 values.
                - Step 3: Create VAO.
                - Step 4: Create VBO.
                - Step 5: Create EBO using the created indices.
        '''

        self.vertices = np.array([
        # Position      # Tex Coords.
        ])
        self._indices = np.empty((6,), dtype=np.uint32)


    def draw(self):
        glUseProgram(self._shader_program)
        glBindVertexArray(self.vao)
        glActiveTexture(GL_TEXTURE0 + self.texture_unit)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glDrawElements(GL_TRIANGLES, len(self._indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(2, (self.vbo, self.ebo))


class WorldBoxEntity:
    def __init__(self, sky_texture_path: str, ground_texture_path: str, texture_unit: int):
        super().__init__()
        '''
            This code already created the sky and the ground. The world is implemented by a closed box for simplicity. The sky is composite of the top, left, right, front, back box faces. The ground is the bottom face.

            This code is already load the sky and the ground entities. There are only two faces for the sky and the ground. You need to draw the sky face 5 times by calculating the below model transforms to transform the sky face into front, back, left, right, and top positions. Please read the draw function for more details.
        '''

        self._sky_face = BoxFaceEntity(sky_texture_path, texture_unit + 0)
        self._sky_face.model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self._sky_face.view_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        self._ground = BoxFaceEntity(ground_texture_path, texture_unit + 1)
        self._ground.model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self._ground.view_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        '''
        Your code starts from here. Need to replace these matrices.
        '''
        self._front_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self._back_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self._left_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self._right_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self._top_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        self._bottom_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        '''
        Your code ends here
        '''

    def _update_projection_transform(self, projection_transform):
        self._sky_face.projection_transform = projection_transform
        self._ground.projection_transform = projection_transform

    def _update_view_transform(self, view_transform):
        self._sky_face.view_transform = view_transform
        self._ground.view_transform = view_transform

    def draw(self):
        # Sky front
        self._sky_face.model_transform = self._front_transform
        self._sky_face.draw()

        # Sky back
        self._sky_face.model_transform = self._back_transform
        self._sky_face.draw()

        # Sky left
        self._sky_face.model_transform = self._left_transform
        self._sky_face.draw()
        
        # Sky right
        self._sky_face.model_transform = self._right_transform
        self._sky_face.draw()

        # Sky top
        self._sky_face.model_transform = self._top_transform
        self._sky_face.draw()

        # Ground
        self._ground.model_transform = self._bottom_transform
        self._ground.draw()

    def destroy(self):
        self._sky_face.destroy()
        self._ground.destroy()
