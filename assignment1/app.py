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

from enum import Enum
import glfw
import numpy as np
from numpy.typing import NDArray
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

from height_map import HeightMap


class ControlState(Enum):
    TRANSLATE = 0
    ROTATE = 1
    IDLE = 2
    SCALE = 3


class DrawingMode(Enum):
    POINT = 0
    TRIANGLE = 1
    WIREFRAME = 2

    def next(self):
        members = list(type(self))
        index = (members.index(self) + 1) % len(members)
        return members[index]


class HeightMapApp:
    def __init__(self, height_map_path: str, window_width: int, window_height: int):
        self._control_state: ControlState = ControlState.IDLE
        self._drawing_mode: DrawingMode = DrawingMode.TRIANGLE
        self._cursor_pos: NDArray[np.float32] = np.array([0., 0.], dtype=np.float32)
        self._rotate_value: NDArray[np.float32] = np.array([0., 0.], dtype=np.float32)
        self._translate_value: NDArray[np.float32] = np.array([0., 0.], dtype=np.float32)
        self._scale_value: float = 1.

        self._create_window(window_width, window_height)
        self._height_map = HeightMap(height_map_path)

        self._shader_program = self._create_shader(
            './shaders/basic_transformation.vert', 
            './shaders/basic_color.frag'
        )
        self._init_projection_transform(window_width, window_height)

    @staticmethod
    def _create_shader(vertex_shader_path: str, fragment_shader_path: str) -> int:
        """
        Create OpenGL shader program.

        hint:
            - Step 1: read the shaders from the input paths.
            - Step 2: Compile the vertex and fragment shaders.
            - Step 3: Compile the shader program.

        Parameters:
            - vertext_shader_path (str): Path to the vertex shader
            - fragment_shader_path (str): Path to the fragment shader
        Returns:
            - shader_program (int): The integer handle of the shader program
        """

        shader_program = -1
        ### Your code start from here ###

        ### End of your code ###

        return shader_program

    def run(self):
        self._main_loop()

    def _init_projection_transform(self, window_width: int, window_height: int):
        """
        Iniitlize the projection matrix for the vertex shader.

        hint:
            - Step 1: Create the projection matrix using pyrr.
            - Step 2: Bind the shader program using glUseProgram.
            - Step 2: Pass it to the shader using glUniformMatrix4fv and glGetUniformLocation.

        Parameters:
            - window_width (int): Window width
            - window_height (int): Window height
        """
        self._projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45,
            aspect=window_width / window_height,
            near=0.1,
            far=10,
            dtype=np.float32
        )

        ### Your code start from here ###

        ### End of your code ###

    def _create_window(self, window_width: int, window_height: int):
        """
        Create a window using GLFW. You do not have to modify this method.

        Parameters:
            - window_width (int): Window width
            - window_height (int): Window height
        """

        if not glfw.init():
            print("Failed to initialize GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(window_width, window_height, "Height Map Visualization", None, None)
        if not self.window:
            print("Failed to create GLFW window")
            glfw.terminate()
            return

        glfw.make_context_current(self.window)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        glfw.set_mouse_button_callback(self.window, self._mouse_button_callback)
        glfw.set_cursor_pos_callback(self.window, self._cursor_pos_callback)
        glfw.set_scroll_callback(self.window, self._scroll_callback)
        glfw.set_key_callback(self.window, self._keyboard_callback)

    def _cursor_pos_callback(self, window: glfw._GLFWwindow, x: float, y: float):
        new_cursor_pos = np.array([x, y], dtype=np.float32)
        cursor_delta = new_cursor_pos - self._cursor_pos
        self._cursor_pos = new_cursor_pos

        match self._control_state:
            case ControlState.TRANSLATE:
                cursor_delta[1] *= -1
                self._translate_value += cursor_delta * 0.01
            case ControlState.ROTATE:
                self._rotate_value += cursor_delta
            case ControlState.SCALE:
                pass  # cursor position does not affect scaling
            case ControlState.IDLE:
                pass

        self._update_modelview_transform()

    def _mouse_button_callback(self, window: glfw._GLFWwindow, button: int, action: int, mods: int):
        match button:
            case glfw.MOUSE_BUTTON_LEFT:
                if action == glfw.PRESS:
                    self._control_state = ControlState.ROTATE
                elif action == glfw.RELEASE:
                    self._control_state = ControlState.IDLE
            case glfw.MOUSE_BUTTON_RIGHT:
                if action == glfw.PRESS:
                    self._control_state = ControlState.TRANSLATE
                elif action == glfw.RELEASE:
                    self._control_state = ControlState.IDLE

    def _scroll_callback(self, window: glfw._GLFWwindow, xoffset: float, yoffset: float):
        self._scale_value *= (1 - yoffset * 0.01)

        self._update_modelview_transform()

    def _keyboard_callback(self, window: glfw._GLFWwindow, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_W:
                self._drawing_mode = self._drawing_mode.next()

    def _update_modelview_transform(self):
        """
        Update the model transformation matrix in the vertex shader.
        Hint:
            - Use glUnfiformMatrix4fv and glGetUniformLocation as in the projection transformation initialization.
        """

        self._height_map.update_model_transform(
            self._translate_value,
            self._rotate_value,
            self._scale_value
        )

        ### Your code start from here ###

        ### End of your code ###

    def _main_loop(self):
        """
        GLFW main loop. This method will draw the height map to the window.        

        hint:
            - Step 1: Clear the buffers.
            - Step 2: Bind the shader program.
            - Step 3: Draw the height map.
            - Step 4: Swap buffers.
            - Step 5: Poll the events.
        """
        while not glfw.window_should_close(self.window):
            gl_drawing_mode = GL_POINT
            match self._drawing_mode:
                case DrawingMode.TRIANGLE:
                    gl_drawing_mode = GL_FILL
                case DrawingMode.WIREFRAME:
                    gl_drawing_mode = GL_LINE
                case _:
                    gl_drawing_mode = GL_POINT
            glPolygonMode(GL_FRONT_AND_BACK, gl_drawing_mode)

            ### Your code start from here ###

            ### End of your code ###

        glfw.terminate()

    def quit(self):
        self._height_map.destroy()
        glDeleteProgram(self._shader_program)
