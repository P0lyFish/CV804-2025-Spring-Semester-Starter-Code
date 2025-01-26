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

import glfw
import numpy as np
from numpy.typing import NDArray
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import time

from enum import Enum
from mesh_viewer import MeshViewer


class ControlState(Enum):
    TRANSLATE = 0
    ROTATE = 1
    IDLE = 2
    SCALE = 3

class DrawingMode(Enum):
    WIREFRAME = 0
    HIDDEN_LINE = 1
    SOLID_FLAT = 2
    SOLID_SMOOTH = 3
    VALENCE = 4

    def next(self):
        members = list(type(self))
        index = (members.index(self) + 1) % len(members)
        return members[index]

class ValenceApp:
    def __init__(self, mesh_path: str, width: int, height: int):
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        self._width = width
        self._height = height

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(width, height, "Valence Viewer", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self.window)

        self._control_state = ControlState.IDLE
        self._drawing_mode = DrawingMode.SOLID_SMOOTH
        self._cursor_pos = np.array([0., 0.], dtype=np.float32)
        self._rotate_value = np.array([0., 0.], dtype=np.float32)
        self._translate_value = np.array([0., -0.1], dtype=np.float32)
        self._scale_value = 1.

        self._shader_program = self._create_shader(
            'shaders/basic_transformation.vert',
            'shaders/basic_color.frag'
        )

        self.enable_lighting_loc = glGetUniformLocation(self._shader_program, "enableLighting")
        self.face_color_loc = glGetUniformLocation(self._shader_program, "faceColor")

        self._mesh_data = MeshViewer(mesh_path)

        self._init_projection_transform(width, height)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        glfw.set_mouse_button_callback(self.window, self._mouse_button_callback)
        glfw.set_cursor_pos_callback(self.window, self._cursor_pos_callback)
        glfw.set_scroll_callback(self.window, self._scroll_callback)
        glfw.set_key_callback(self.window, self._keyboard_callback)
    
    def _create_shader(self, vertex_path: str, fragment_path: str) -> int:
        with open(vertex_path, 'r') as f:
            vertex_src = f.read()
        with open(fragment_path, 'r') as f:
            fragment_src = f.read()

        local_vao = glGenVertexArrays(1)
        glBindVertexArray(local_vao)

        program = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        glBindVertexArray(0)
        glDeleteVertexArrays(1, [local_vao])

        return program

    def _init_projection_transform(self, width: int, height: int):
        aspect = width / float(height)
        self._projection = pyrr.matrix44.create_perspective_projection(
            fovy=30.0, aspect=aspect, near=0.01, far=10.0, dtype=np.float32
        )
        glUseProgram(self._shader_program)
        proj_loc = glGetUniformLocation(self._shader_program, "projection")
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, self._projection)

        self._model = np.eye(4, dtype=np.float32)
        model_loc = glGetUniformLocation(self._shader_program, "model")
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, self._model)

    def run(self):
        while not glfw.window_should_close(self.window):
            self._update_and_draw()
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        self._mesh_data.destroy()
        glDeleteProgram(self._shader_program)
        glfw.terminate()

    def measure_fps(self):
        frames = 90
        angle = 360.0 / frames
        axis_list = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([0.0, 0.0, 1.0])
        ]

        start_time = time.time()
        for axis in axis_list:
            for _ in range(frames):
                if np.array_equal(axis, [1.0, 0.0, 0.0]):
                    self._rotate_value[1] += angle
                elif np.array_equal(axis, [0.0, 1.0, 0.0]):
                    self._rotate_value[0] += angle
                elif np.array_equal(axis, [0.0, 0.0, 1.0]): 
                    pass

                self._update_and_draw()

        elapsed_time = time.time() - start_time
        total_frames = 3 * frames
        fps = total_frames / elapsed_time
        self._rotate_value = np.array([0.0, 0.0], dtype=np.float32)

        return fps

    def _update_and_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self._drawing_mode == DrawingMode.WIREFRAME:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glUniform1i(self.enable_lighting_loc, 0)
            glUniform4f(self.face_color_loc, 1.0, 1.0, 1.0, 1.0)
            glDisable(GL_DEPTH_TEST)
            self._mesh_data.draw()
            glEnable(GL_DEPTH_TEST)
        elif self._drawing_mode == DrawingMode.HIDDEN_LINE:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glUniform1i(self.enable_lighting_loc, 0)
            glUniform4f(self.face_color_loc, 1.0, 1.0, 1.0, 1.0)
        else:
            glUniform1i(self.enable_lighting_loc, 1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glUseProgram(self._shader_program)

        view_matrix = np.eye(4, dtype=np.float32)
        view_matrix[2, 3] = -0.5

        view_loc = glGetUniformLocation(self._shader_program, "view")
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view_matrix)

        light_positions = [
            np.array([0.1, 0.1, -0.02], dtype=np.float32),
            np.array([-0.1, 0.1, -0.02], dtype=np.float32),
            np.array([0.0, 0.0, 0.1], dtype=np.float32)
        ]

        light_colors = [
            (0.05, 0.05, 0.8),
            (0.6, 0.05, 0.05),
            (1.0, 1.0, 1.0)
        ]

        for i in range(3):
            pos_loc = glGetUniformLocation(self._shader_program, f"lights[{i}].position")
            ambient_loc = glGetUniformLocation(self._shader_program, f"lights[{i}].ambient")
            diffuse_loc = glGetUniformLocation(self._shader_program, f"lights[{i}].diffuse")
            specular_loc = glGetUniformLocation(self._shader_program, f"lights[{i}].specular")

            glUniform3fv(pos_loc, 1, light_positions[i])
            glUniform3f(ambient_loc, light_colors[i][0]*0.1, light_colors[i][1]*0.1, light_colors[i][2]*0.1)
            glUniform3f(diffuse_loc, light_colors[i][0]*0.8, light_colors[i][1]*0.8, light_colors[i][2]*0.8)
            glUniform3f(specular_loc, light_colors[i][0], light_colors[i][1], light_colors[i][2])

        material_ambient_loc = glGetUniformLocation(self._shader_program, "material.ambient")
        material_diffuse_loc = glGetUniformLocation(self._shader_program, "material.diffuse")
        material_specular_loc = glGetUniformLocation(self._shader_program, "material.specular")
        material_shininess_loc = glGetUniformLocation(self._shader_program, "material.shininess")

        glUniform3f(material_ambient_loc, 0.2, 0.2, 0.2)
        glUniform3f(material_diffuse_loc, 0.4, 0.4, 0.4)
        glUniform3f(material_specular_loc, 0.8, 0.8, 0.8)
        glUniform1f(material_shininess_loc, 128.0)

        shading_mode_loc = glGetUniformLocation(self._shader_program, "shadingMode")

        if self._drawing_mode == DrawingMode.SOLID_FLAT:
            glUniform1i(shading_mode_loc, 0)
        else:
            glUniform1i(shading_mode_loc, 1)

        if self._drawing_mode == DrawingMode.HIDDEN_LINE:
            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
            glDepthRange(0.01, 1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            self._mesh_data.draw()

            glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
            glDepthRange(0.0, 1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDepthFunc(GL_LEQUAL)
            self._mesh_data.draw()

            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glDepthFunc(GL_LESS)

        elif self._drawing_mode == DrawingMode.SOLID_FLAT:
            shading_mode_loc = glGetUniformLocation(self._shader_program, "shadingMode")
            color_mode_loc = glGetUniformLocation(self._shader_program, "useValenceColor")
            glUniform1i(color_mode_loc, 0)
            glUniform1i(shading_mode_loc, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            self._mesh_data.draw()

        elif self._drawing_mode == DrawingMode.SOLID_SMOOTH:
            shading_mode_loc = glGetUniformLocation(self._shader_program, "shadingMode")
            color_mode_loc = glGetUniformLocation(self._shader_program, "useValenceColor")
            glUniform1i(color_mode_loc, 0)
            glUniform1i(shading_mode_loc, 1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            self._mesh_data.draw()

        elif self._drawing_mode == DrawingMode.VALENCE:
            glDepthRange(0.01, 1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            color_mode_loc = glGetUniformLocation(self._shader_program, "useValenceColor")
            glUniform1i(color_mode_loc, 1)

            self._mesh_data.draw()

            glDepthRange(0.0, 1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDepthFunc(GL_LEQUAL)

            glUniform1i(color_mode_loc, 0)

            self._mesh_data.draw()

            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glDepthFunc(GL_LESS)

            glDepthRange(0.01, 1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


    def _mouse_button_callback(self, window, button, action, mods):
        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                self._control_state = ControlState.ROTATE
            elif button == glfw.MOUSE_BUTTON_RIGHT:
                self._control_state = ControlState.TRANSLATE
        elif action == glfw.RELEASE:
            self._control_state = ControlState.IDLE

    def _cursor_pos_callback(self, window, x, y):
        new_cursor_pos = np.array([x, y], dtype=np.float32)
        cursor_delta = new_cursor_pos - self._cursor_pos
        self._cursor_pos = new_cursor_pos

        match self._control_state:
            case ControlState.TRANSLATE:
                cursor_delta[1] *= -1
                self._translate_value += cursor_delta * 0.001
            case ControlState.ROTATE:
                self._rotate_value += -cursor_delta*0.5
            case ControlState.SCALE:
                pass
            case ControlState.IDLE:
                pass

        self._update_model_transform()

    def _scroll_callback(self, window, xoffset, yoffset):
        self._scale_value *= (1 - 0.01 * yoffset)
        self._update_model_transform()

    def _keyboard_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_1:
                self._drawing_mode = DrawingMode.WIREFRAME
                print("Drawing mode:", self._drawing_mode)
            elif key == glfw.KEY_2:
                self._drawing_mode = DrawingMode.HIDDEN_LINE
                print("Drawing mode:", self._drawing_mode)
            elif key == glfw.KEY_3:
                self._drawing_mode = DrawingMode.SOLID_FLAT
                print("Drawing mode:", self._drawing_mode)
            elif key == glfw.KEY_4:
                self._drawing_mode = DrawingMode.SOLID_SMOOTH
                print("Drawing mode:", self._drawing_mode)
            elif key == glfw.KEY_5:
                self._drawing_mode = DrawingMode.VALENCE
                print("Drawing mode:", self._drawing_mode)
            elif key == glfw.KEY_F:  # Performance test
                print("Performance test: Running...")
                fps = self.measure_fps()
                print(f"Performance test: {fps:.2f} FPS")

    def _update_model_transform(self):
        rot_x = pyrr.matrix44.create_from_x_rotation(np.radians(self._rotate_value[1]), dtype=np.float32)
        rot_y = pyrr.matrix44.create_from_y_rotation(np.radians(self._rotate_value[0]), dtype=np.float32)
        scale_mat = pyrr.matrix44.create_from_scale([self._scale_value]*3, dtype=np.float32)
        trans_mat = pyrr.matrix44.create_from_translation(
        [self._translate_value[0], self._translate_value[1], -0.5],
        dtype=np.float32
)

        model_mat = pyrr.matrix44.multiply(rot_x, rot_y)
        model_mat = pyrr.matrix44.multiply(model_mat, scale_mat)
        model_mat = pyrr.matrix44.multiply(model_mat, trans_mat)

        self._model = model_mat

        glUseProgram(self._shader_program)
        model_loc = glGetUniformLocation(self._shader_program, "model")
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, self._model)
