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
from OpenGL.GL.shaders import compileProgram, compileShader
import cv2
import numpy as np
import pyrr


class BaseEntity:
    def __init__(self):
        pass

    @staticmethod
    def _load_texture(texture_path, texture_unit):
        image = cv2.imread(texture_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        tex = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0 + texture_unit)
        glBindTexture(GL_TEXTURE_2D, tex)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.shape[0], image.shape[1], 0, GL_RGB, GL_UNSIGNED_BYTE, image)
        glGenerateMipmap(GL_TEXTURE_2D)

        return tex

    @staticmethod
    def _create_shader(vertex_shader_path, fragment_shader_path):
        with open(vertex_shader_path, 'r') as f:
            vertex_shader_src = f.readlines()
        with open(fragment_shader_path, 'r') as f:
            fragment_shader_src = f.readlines()

        shader_program = compileProgram(
            compileShader(vertex_shader_src, GL_VERTEX_SHADER),
            compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)
        )

        return shader_program

    @property
    def model_transform(self):
        return self._model_transform

    @model_transform.setter
    def model_transform(self, value):
        self._model_transform = value

        glUseProgram(self._shader_program)
        glUniformMatrix4fv(
            glGetUniformLocation(self._shader_program, 'model'),
            1,
            GL_FALSE,
            self._model_transform
        )

    @property
    def view_transform(self):
        return self._view_transform

    @view_transform.setter
    def view_transform(self, value):
        self._view_transform = value

        glUseProgram(self._shader_program)
        glUniformMatrix4fv(
            glGetUniformLocation(self._shader_program, 'view'),
            1,
            GL_FALSE,
            self._view_transform
        )

    @property
    def projection_transform(self):
        return self._projection_transform

    @projection_transform.setter
    def projection_transform(self, value):
        self._projection_transform = value

        glUseProgram(self._shader_program)
        glUniformMatrix4fv(
            glGetUniformLocation(self._shader_program, 'projection'),
            1,
            GL_FALSE,
            self._projection_transform
        )

    def draw(self):
        raise NotImplementedError(f"{type(self)}'s Draw function is not implemented!")
