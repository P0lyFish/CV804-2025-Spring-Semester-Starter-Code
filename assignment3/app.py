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


from enum import Enum
import glfw
import numpy as np
from numpy.typing import NDArray
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import time

from railway_entity import RailwayEntity
from world_box_entity import WorldBoxEntity


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

class RollerCoasterApp:
    SPEED = 0.1

    def __init__(
        self,
        sky_texture_path: str,
        ground_texture_path: str,
        ties_texture_path: str,
        railway_path: str,
        window_width: int,
        window_height: int
    ):
        self._control_state: ControlState = ControlState.IDLE
        self._drawing_mode: DrawingMode = DrawingMode.TRIANGLE
        self._cursor_pos: NDArray[np.float32] = np.array([0., 0.], dtype=np.float32)
        self._rotate_value: NDArray[np.float32] = np.array([0., 0.], dtype=np.float32)
        self._translate_value: NDArray[np.float32] = np.array([0., 0.], dtype=np.float32)
        self._scale_value: float = 1.
        self._last_time_restart = None
        self._train_view_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        self._create_window(window_width, window_height)
        self._init_projection_transform(window_width, window_height)

        self._world_box = WorldBoxEntity(
            sky_texture_path,
            ground_texture_path,
            texture_unit=0
        )
        self._world_box._update_projection_transform(self._projection_transform)

        self._railway = RailwayEntity(ties_texture_path, railway_path, texture_unit=1)
        self._railway._update_projection_transform(self._projection_transform)

    def run(self):
        self._main_loop()

    def _init_projection_transform(self, window_width: int, window_height: int):
        self._projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=30,
            aspect=window_width / window_height,
            near=0.01,
            far=100,
            dtype=np.float32
        )

    def _create_window(self, window_width: int, window_height: int):
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
        glfw.set_key_callback(self.window, self._keyboard_callback)

    def _cursor_pos_callback(self, window: glfw._GLFWwindow, x: float, y: float):
        new_cursor_pos = np.array([x, y], dtype=np.float32)
        cursor_delta = new_cursor_pos - self._cursor_pos
        self._cursor_pos = new_cursor_pos

        match self._control_state:
            case ControlState.ROTATE:
                self._rotate_value += cursor_delta
            case ControlState.IDLE:
                pass

        self._update_view_transform()

    def _mouse_button_callback(self, window: glfw._GLFWwindow, button: int, action: int, mods: int):
        match button:
            case glfw.MOUSE_BUTTON_LEFT:
                if action == glfw.PRESS:
                    self._control_state = ControlState.ROTATE
                elif action == glfw.RELEASE:
                    self._control_state = ControlState.IDLE

    def _keyboard_callback(self, window: glfw._GLFWwindow, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_W:
                self._drawing_mode = self._drawing_mode.next()

    def _update_view_transform(self):
        view_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        view_transform = pyrr.matrix44.multiply(m1=view_transform, m2=self._train_view_transform)

        view_transform = pyrr.matrix44.multiply(
            m1=view_transform, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = [0, 1, 0],
                theta = np.radians(self._rotate_value[0]),
                dtype = np.float32
            )
        )

        view_transform = pyrr.matrix44.multiply(
            m1=view_transform, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = [1, 0, 0],
                theta = np.radians(self._rotate_value[1]),
                dtype = np.float32
            )
        )

        self._world_box._update_view_transform(view_transform)
        self._railway._update_view_transform(view_transform)

    def _main_loop(self):
        while not glfw.window_should_close(self.window):
            if self._last_time_restart is None:
                self._last_time_restart = time.time()
            time_passed = (time.time() - self._last_time_restart) / self._railway.total_length * self.SPEED;
            time_passed = min(time_passed, 0.999)
            self._train_view_transform = self._railway.get_camera_along_railway(time_passed)
            self._update_view_transform()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

            self._world_box.draw()

            self._railway.draw()
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()

    def quit(self):
        self._world_box.destroy()
        self._railway.destroy()

