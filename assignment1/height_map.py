'''
                                                
   Code framework for the lecture

   "CV804: 3D Geometry Processing"

   Lecturer: Hao Li
   TAs: Phong Tran, Long Nhat Ho

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


import cv2
import numpy as np
from numpy.typing import NDArray
from OpenGL.GL import *
import pyrr
from typing import Tuple


class HeightMap:
    def __init__(self, height_map_path):
        self._num_vertices: int = -1

        self.vao: int = 0
        self.vbo: int = 0
        self.ebo: int = 0
        self._indices: NDArray[np.uint32] = np.empty(0, dtype=np.uint32)

        height_map, texture = self._load_height_map(height_map_path)
        self._build_vertex_data(height_map, texture)

        self._init_model_transform()

    def _load_height_map(self, path: str) -> Tuple[NDArray[np.float32], NDArray[np.float32]]:
        """
        Load the height map and calculate the texture.

        hint:
        - You can use cv2.imread to load an image and cv2.applyColor to calculate the texture based on the heights of the gradient of the heights.

        Parameters:
            - path (str): Path to the height map image
        Returns:
            - height_map (NDArray[np.float32]): The height map. It is the z-coordinate in the model space.
            - texture (NDArray[np.float32]): The rgb texture. Should be normalized to range [0..1]
        """
        height_map = np.zeros((256, 256), np.float32)
        texture = np.zeros_like(height_map)

        ### Your code start from here ###

        ### End of your code ###

        return height_map, texture

    def _build_vertex_data(self, height_map: NDArray[np.float32], texture: NDArray[np.float32]):
        """
        Build the vertex data for rendering, including:
            - Vertex Array Object (VAO)
            - Vertext Buffer Object (VBO)
            - Optionally Element Buffer Object (EBO) if you draw using glDrawElements.

        Parameters:
            - height_map (NDArray[np.float32]): Height map numpy array.
            - texture (NDArray[np.float32]): Texture numpy array.
        """

        H, W = height_map.shape
        self._num_vertices = H * W

        ### Your code start from here ###

        ### End of your code ###


    def _init_model_transform(self):
        self._model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

    def update_model_transform(
        self,
        translation: NDArray[np.float32],
        rotation: NDArray[np.float32],
        scale: float
    ):
        """
        Update the model transformmation matrix.
        Hint:
            - pyrr.multiply: Multiply two transformations.
            - pyrr.create_from_axis_rotation: Create rotation matrix given input angle.
            - pyrr.create_from_translation: Create translation matrix from a given translation vector.
            - pyrr.create_from_scale: Create scaling matrix from a given scaling vector.

        Parameters:
            - translation (NDArray[np.float32]): 3D translation vector.
            - rotation (NDArray[np.float32]): 2D Rotation vector. Only rotate in yaw and pitch angles.
            - scale (float): Scale value. Assuming the scale is uniform in all three dimensions.
        """

        self._model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        ### Your code start from here ###

        ### End of your code ###


    def get_model_transform(self):
        return self._model_transform

    def draw(self):
        """
        OpenGL draw function.
        Hint:
            - Step 1: Bind VAO
            - Step 2: Draw the triangles using either glDrawElements or glDrawArrays.
            - Step 3: Unbind VAO
        """

        ### Your code start from here ###

        ### End of your code ###

    def destroy(self):
        """
        Clean the data, including vao, vbo, and optionally ebo.
        """

        ### Your code start from here ###

        ### End of your code ###
