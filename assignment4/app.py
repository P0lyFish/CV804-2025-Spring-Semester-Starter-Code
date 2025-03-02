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

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glfw
from PIL import Image
from scene import Scene
from utils import compile_shader, create_program, Vec3

class RaytracerApp:
    def __init__(self, scene_path, save_path=None, window_width=640, window_height=480):
        self.scene_path = scene_path
        self.save_path = save_path
        self.window_width = window_width
        self.window_height = window_height
        self.window = None
        self.program = None
        self.scene = None

    def run(self):
        if not glfw.init():
            print("Failed to initialize GLFW")
            return

        # If you use macOS request OpenGL 3.3 core profile for macOS compatibility, if you use Linux just skip it
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)  # Required for macOS

        self.window = glfw.create_window(self.window_width, self.window_height, "Ray Tracer", None, None)
        if not self.window:
            glfw.terminate()
            print("Failed to create GLFW window")
            return

        glfw.make_context_current(self.window)

        quad = np.array([-1, -1, 1, -1, -1, 1, 1, 1], dtype=np.float32)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, quad.nbytes, quad, GL_STATIC_DRAW)

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)

        # Compile shaders from files
        self.program = create_program("shaders/vertex_shader.vert", "shaders/fragment_shader.frag")
        if not self.program:
            glfw.terminate()
            return
        glUseProgram(self.program)

        # Load scene
        self.scene = Scene()
        self.scene.load_scene(self.scene_path)

        width, height = glfw.get_framebuffer_size(self.window)
        glViewport(0, 0, width, height)

        # Set uniforms
        glUniform3fv(glGetUniformLocation(self.program, "camera_pos"), 1, self.scene.camera_pos.to_list())
        glUniform1f(glGetUniformLocation(self.program, "aspect_ratio"), self.window_height / self.window_width)
        # ----------------------------Insert your code here----------------------------------
        # Set the fov_tan uniform using the provided 80-degree FOV
        # Hint: Use np.tan and np.radians to convert 80 degrees to the tangent of half the FOV
        # ----------------------------End of code---------------------------------------------

        glUniform3fv(glGetUniformLocation(self.program, "ambient_light.pos"), 1, self.scene.ambient.pos.to_list())
        glUniform3fv(glGetUniformLocation(self.program, "ambient_light.color"), 1, self.scene.ambient.color.to_list())

        glUniform1i(glGetUniformLocation(self.program, "num_lights"), len(self.scene.lights))
        for i, light in enumerate(self.scene.lights):
            glUniform3fv(glGetUniformLocation(self.program, f"lights[{i}].pos"), 1, light.pos.to_list())
            glUniform3fv(glGetUniformLocation(self.program, f"lights[{i}].color"), 1, light.color.to_list())

        glUniform1i(glGetUniformLocation(self.program, "num_spheres"), len(self.scene.spheres))
        for i, sphere in enumerate(self.scene.spheres):
            glUniform3fv(glGetUniformLocation(self.program, f"spheres[{i}].pos"), 1, sphere.pos.to_list())
            glUniform1f(glGetUniformLocation(self.program, f"spheres[{i}].radius"), sphere.radius)
            glUniform3fv(glGetUniformLocation(self.program, f"spheres[{i}].diffuse"), 1, sphere.diffuse.to_list())
            glUniform3fv(glGetUniformLocation(self.program, f"spheres[{i}].specular"), 1, sphere.specular.to_list())
            glUniform1f(glGetUniformLocation(self.program, f"spheres[{i}].shininess"), sphere.shininess)

        glUniform1i(glGetUniformLocation(self.program, "num_triangles"), len(self.scene.triangles))
        for i, tri in enumerate(self.scene.triangles):
            for j, v in enumerate(tri.vertices):
                glUniform3fv(glGetUniformLocation(self.program, f"triangles[{i}].v{j}"), 1, v.pos.to_list())
                glUniform3fv(glGetUniformLocation(self.program, f"triangles[{i}].n{j}"), 1, v.normal.to_list())
                glUniform3fv(glGetUniformLocation(self.program, f"triangles[{i}].diffuse{j}"), 1, v.diffuse.to_list())
                glUniform3fv(glGetUniformLocation(self.program, f"triangles[{i}].specular{j}"), 1, v.specular.to_list())
                glUniform1f(glGetUniformLocation(self.program, f"triangles[{i}].shininess{j}"), v.shininess)

        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)
            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

            # Save the image if save_path is provided
            if self.save_path:
                glPixelStorei(GL_PACK_ALIGNMENT, 1)
                glFinish()
                data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
                image = Image.frombytes("RGB", (width, height), data)
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
                # Resize to 640x480
                image = image.resize((640, 480), Image.Resampling.LANCZOS)
                image.save(self.save_path)
                print(f"Image saved to {self.save_path}")
                break

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()