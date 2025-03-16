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

import glfw
from OpenGL.GL import *
import numpy as np

class Viewer:
    def __init__(self, title, width, height):
        self.width, self.height = width, height
        self.title = title
        self.last_x, self.last_y = width / 2, height / 2
        self.button_down = [False] * 3
        self.center = np.zeros(3, dtype=np.float32)
        self.radius = 1.0
        self.modelview = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)
        self.fovy, self.near, self.far = 45.0, 0.2, 100.0

        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self.window)
        glfw.set_window_size_callback(self.window, self.reshape)
        glfw.set_mouse_button_callback(self.window, self.mouse)
        glfw.set_cursor_pos_callback(self.window, self.motion)
        glfw.set_key_callback(self.window, self.keyboard)

        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)

    def run(self):
        while not glfw.window_should_close(self.window):
            self.display()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()

    def reshape(self, window, width, height):
        self.width, self.height = width, height
        glViewport(0, 0, width, height)
        self.update_projection()

    def update_projection(self):
        aspect = self.width / self.height
        self.projection = self.perspective(self.fovy, aspect, self.near, self.far)

    def perspective(self, fovy, aspect, near, far):
        f = 1.0 / np.tan(np.radians(fovy) / 2)
        return np.array([
            [f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), -1],
            [0, 0, (2 * far * near) / (near - far), 0]
        ], dtype=np.float32)

    def set_scene(self, center, radius):
        self.modelview = np.eye(4)
        self.modelview[:3, 3] = -center
        self.modelview[2, 3] -= radius * 1
        self.projection = np.array([
            [1/radius, 0, 0, 0],
            [0, 1/radius, 0, 0],
            [0, 0, -1/radius, -1],
            [0, 0, 0, 1]
        ], dtype=np.float32)

    def view_all(self):
        self.modelview = np.eye(4, dtype=np.float32)
        self.translate([-self.center[0], -self.center[1], -self.center[2] - 3 * self.radius])

    def translate(self, trans):
        trans_mat = np.eye(4, dtype=np.float32)
        trans_mat[:3, 3] = trans
        self.modelview = trans_mat @ self.modelview

    def rotate(self, axis, angle):
        norm = np.linalg.norm(axis)
        if norm < 1e-6:  # Avoid division by zero or very small values
            return
        angle_rad = np.radians(angle)
        c, s = np.cos(angle_rad), np.sin(angle_rad)
        n = axis / norm
        rot_mat = np.eye(4, dtype=np.float32)
        rot_mat[:3, :3] = (
            c * np.eye(3) + (1 - c) * np.outer(n, n) + s * np.cross(np.eye(3), n)
        )
        self.modelview = rot_mat @ self.modelview

    def map_to_sphere(self, x, y):
        x = (x - self.width / 2) / self.width
        y = (self.height / 2 - y) / self.height
        sinx, siny = np.sin(np.pi * x * 0.5), np.sin(np.pi * y * 0.5)
        sinx2siny2 = sinx**2 + siny**2
        if sinx2siny2 < 1.0:
            return np.array([sinx, siny, np.sqrt(1.0 - sinx2siny2)], dtype=np.float32)
        return np.array([sinx, siny, 0.0], dtype=np.float32)

    def mouse(self, window, button, action, mods):
        if action == glfw.PRESS:
            self.button_down[button] = True
            self.last_x, self.last_y = glfw.get_cursor_pos(window)
        elif action == glfw.RELEASE:
            self.button_down[button] = False

    def motion(self, window, x, y):
        if self.button_down[0] and self.button_down[1]:  # Zoom
            dy = y - self.last_y
            self.translate([0, 0, self.radius * dy * 3.0 / self.height])
        elif self.button_down[0]:  # Rotate
            last_point = self.map_to_sphere(self.last_x, self.last_y)
            new_point = self.map_to_sphere(x, y)
            axis = np.cross(last_point, new_point)
            cos_angle = np.dot(last_point, new_point)
            if abs(cos_angle) < 1.0:
                angle = 2.0 * np.degrees(np.arccos(cos_angle))
                self.rotate(axis, angle)
        elif self.button_down[1]:  # Translate
            dx, dy = x - self.last_x, y - self.last_y
            z = -self.modelview[2, 3]
            aspect = self.width / self.height
            up = np.tan(np.radians(self.fovy) / 2) * self.near
            right = aspect * up
            self.translate([2 * dx * right / self.near * z / self.width,
                            -2 * dy * up / self.near * z / self.height, 0])
        self.last_x, self.last_y = x, y

    def keyboard(self, window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(self.window, True)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)