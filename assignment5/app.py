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

import os
import glfw
import openmesh as om
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from viewer import Viewer
from registration import Registration
from closest_point import ClosestPoint
from transformation import Transformation

class RegistrationViewerApp(Viewer):
    def __init__(self, title, width, height):
        super().__init__(title, width, height)
        self.meshes = []
        self.transformations = []
        self.indices = []
        self.cur_index = 0
        self.num_processed = 0
        self.sampled_points = []
        self.output_filename = ""
        self.average_vertex_distance = 0.0
        self.mode = "VIEW"
        self.registration = Registration()
        self.setup_shaders()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)

    def load_shader_file(self, filename):
        try:
            with open(filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise RuntimeError(f"Shader file '{filename}' not found")
        except Exception as e:
            raise RuntimeError(f"Error loading shader file '{filename}': {e}")

    def setup_shaders(self):
        shader_dir = os.path.join(os.path.dirname(__file__), 'shaders')
        
        # Mesh shader
        vertex_shader_path = os.path.join(shader_dir, 'mesh.vert')
        fragment_shader_path = os.path.join(shader_dir, 'mesh.frag')
        vertex_source = self.load_shader_file(vertex_shader_path)
        fragment_source = self.load_shader_file(fragment_shader_path)
        
        temp_vao = glGenVertexArrays(1)
        glBindVertexArray(temp_vao)
        self.mesh_shader = compileProgram(
            compileShader(vertex_source, GL_VERTEX_SHADER),
            compileShader(fragment_source, GL_FRAGMENT_SHADER)
        )
        if not glGetProgramiv(self.mesh_shader, GL_LINK_STATUS):
            print(glGetProgramInfoLog(self.mesh_shader))
            raise RuntimeError("Shader linking failed")
        glBindVertexArray(0)
        glDeleteVertexArrays(1, [temp_vao])
        
        glUseProgram(self.mesh_shader)
        self.mesh_model_loc = glGetUniformLocation(self.mesh_shader, "model")
        self.mesh_view_loc = glGetUniformLocation(self.mesh_shader, "view")
        self.mesh_projection_loc = glGetUniformLocation(self.mesh_shader, "projection")
        self.enable_lighting_loc = glGetUniformLocation(self.mesh_shader, "enableLighting")
        glUseProgram(0)

        # Point shader
        point_vertex_path = os.path.join(shader_dir, 'point.vert')
        point_fragment_path = os.path.join(shader_dir, 'point.frag')
        point_vertex_source = self.load_shader_file(point_vertex_path)
        point_fragment_source = self.load_shader_file(point_fragment_path)
        
        temp_vao = glGenVertexArrays(1)
        glBindVertexArray(temp_vao)
        self.point_shader = compileProgram(
            compileShader(point_vertex_source, GL_VERTEX_SHADER),
            compileShader(point_fragment_source, GL_FRAGMENT_SHADER)
        )
        glBindVertexArray(0)
        glDeleteVertexArrays(1, [temp_vao])
        
        glUseProgram(self.point_shader)
        self.point_modelview_loc = glGetUniformLocation(self.point_shader, "modelview")
        self.point_projection_loc = glGetUniformLocation(self.point_shader, "projection")
        glUseProgram(0)

    def set_output(self, filename):
        self.output_filename = filename

    def open_meshes(self, filenames):
        for fname in filenames:
            print(f"Loading mesh: {fname}")
            mesh = om.read_trimesh(fname)
            # Center the mesh
            vertices = np.array([mesh.point(vh) for vh in mesh.vertices()])
            center = np.mean(vertices, axis=0)
            for vh in mesh.vertices():
                mesh.set_point(vh, mesh.point(vh) - center)
            mesh.request_vertex_normals()
            mesh.request_face_normals()
            mesh.update_normals()
            self.meshes.append(mesh)
            self.transformations.append(Transformation())
            # Calculate average vertex distance
            edges = np.array([[mesh.point(mesh.from_vertex_handle(mesh.halfedge_handle(eh, 0))),
                   mesh.point(mesh.to_vertex_handle(mesh.halfedge_handle(eh, 0)))] for eh in mesh.edges()])
            self.average_vertex_distance = np.mean(np.linalg.norm(edges[:, 0] - edges[:, 1], axis=1))
            print(f"Mesh vertices: {mesh.n_vertices()}, faces: {mesh.n_faces()}")

        self.update_indices()
        self.num_processed = min(2, len(self.meshes))
        self.cur_index = max(0, self.num_processed - 1)
        bb_min = np.min([np.min(np.array([mesh.point(vh) for vh in m.vertices()]), axis=0) for m in self.meshes], axis=0)
        bb_max = np.max([np.max(np.array([mesh.point(vh) for vh in m.vertices()]), axis=0) for m in self.meshes], axis=0)
        center = (bb_min + bb_max) / 2
        radius = np.linalg.norm(bb_max - bb_min)
        self.set_scene(center, radius * 0.5)

    def update_indices(self):
        self.indices = []
        for mesh in self.meshes:
            idx = []
            for fh in mesh.faces():
                idx.extend([vh.idx() for vh in mesh.fv(fh)])
            self.indices.append(np.array(idx, dtype=np.uint32))

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.mesh_shader)
        glUniformMatrix4fv(self.mesh_projection_loc, 1, GL_FALSE, self.projection.T)
        glUniformMatrix4fv(self.mesh_view_loc, 1, GL_FALSE, self.modelview.T)

        glUniform1i(self.enable_lighting_loc, 1)
        glUniform1i(glGetUniformLocation(self.mesh_shader, "shadingMode"), 0)

        light_positions = [
            np.array([0.1, 0.1, 0.5], dtype=np.float32),
            np.array([-0.1, 0.1, 0.5], dtype=np.float32),
            np.array([0.0, 0.0, 0.5], dtype=np.float32)
        ]
        light_colors = [
            (0.7, 0.7, 0.7),
            (0.8, 0.5, 0.5),
            (0.5, 0.5, 0.5)
        ]

        view_matrix = self.modelview
        for i in range(3):
            light_pos_view = (view_matrix @ np.append(light_positions[i], 1.0))[:3]
            glUniform3fv(glGetUniformLocation(self.mesh_shader, f"lights[{i}].position"), 1, light_pos_view)
            glUniform3f(glGetUniformLocation(self.mesh_shader, f"lights[{i}].ambient"),
                        light_colors[i][0] * 0.4, light_colors[i][1] * 0.4, light_colors[i][2] * 0.4)
            glUniform3f(glGetUniformLocation(self.mesh_shader, f"lights[{i}].diffuse"),
                        light_colors[i][0] * 0.6, light_colors[i][1] * 0.6, light_colors[i][2] * 0.6)
            glUniform3f(glGetUniformLocation(self.mesh_shader, f"lights[{i}].specular"),
                        light_colors[i][0] * 0.8, light_colors[i][1] * 0.8, light_colors[i][2] * 0.8)

        for i in range(self.num_processed):
            transform = self.transformations[i].to_matrix()
            glUniformMatrix4fv(self.mesh_model_loc, 1, GL_FALSE, transform.T)

            if i != self.cur_index:
                glUniform3f(glGetUniformLocation(self.mesh_shader, "material.ambient"), 0.4, 0.4, 0.4)
                glUniform3f(glGetUniformLocation(self.mesh_shader, "material.diffuse"), 0.6, 0.6, 0.9)
                glUniform3f(glGetUniformLocation(self.mesh_shader, "material.specular"), 0.8, 0.8, 0.8)
            else:
                glUniform3f(glGetUniformLocation(self.mesh_shader, "material.ambient"), 0.1, 0.1, 0.1)
                glUniform3f(glGetUniformLocation(self.mesh_shader, "material.diffuse"), 0.3, 0.9, 0.3)
                glUniform3f(glGetUniformLocation(self.mesh_shader, "material.specular"), 0.7, 0.7, 0.9)

            glUniform1f(glGetUniformLocation(self.mesh_shader, "material.shininess"), 32.0)
            self.draw_mesh(i)

        if self.sampled_points:
            glUseProgram(self.point_shader)
            glUniformMatrix4fv(self.point_projection_loc, 1, GL_FALSE, self.projection.T)
            self.draw_points()

        glUseProgram(0)

    def draw_mesh(self, index):
        mesh = self.meshes[index]
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        # Vertex positions
        vertices = np.array([mesh.point(vh) for vh in mesh.vertices()], dtype=np.float32)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        pos_loc = glGetAttribLocation(self.mesh_shader, "position")
        glVertexAttribPointer(pos_loc, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(pos_loc)

        # Vertex normals
        normals = np.array([mesh.normal(vh) for vh in mesh.vertices()], dtype=np.float32)
        normal_loc = glGetAttribLocation(self.mesh_shader, "normal")
        if normal_loc != -1:
            normal_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, normal_vbo)
            glBufferData(GL_ARRAY_BUFFER, normals, GL_STATIC_DRAW)
            glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(normal_loc)

        ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices[index], GL_STATIC_DRAW)

        glDrawElements(GL_TRIANGLES, len(self.indices[index]), GL_UNSIGNED_INT, None)

        glBindVertexArray(0)
        glDeleteVertexArrays(1, [vao])
        glDeleteBuffers(1, [vbo])
        if normal_loc != -1:
            glDeleteBuffers(1, [normal_vbo])
        glDeleteBuffers(1, [ibo])

    def draw_points(self):
        mesh = self.meshes[self.cur_index]
        vertices = np.array([mesh.point(vh) for vh in mesh.vertices()], dtype=np.float32)
        points = np.array([self.transformations[self.cur_index].transform_point(
            vertices[idx]) for idx in self.sampled_points], dtype=np.float32)
        
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, points, GL_STATIC_DRAW)
        pos_loc = glGetAttribLocation(self.point_shader, "position")
        glVertexAttribPointer(pos_loc, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(pos_loc)

        glUniformMatrix4fv(self.point_modelview_loc, 1, GL_FALSE, self.modelview.T)

        glPointSize(10)
        glDrawArrays(GL_POINTS, 0, len(self.sampled_points))

        glBindVertexArray(0)
        glDeleteVertexArrays(1, [vao])
        glDeleteBuffers(1, [vbo])

    def keyboard(self, window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_EQUAL:
            self.modelview[2, 3] += 0.01
        elif key == glfw.KEY_MINUS:
            self.modelview[2, 3] -= 0.01
        elif key == glfw.KEY_SPACE:
            print("Register point-2-surface...")
            self.perform_registration(True)
        elif key == glfw.KEY_R:
            print("Register point-2-point...")
            self.perform_registration(False)
        elif key == glfw.KEY_N:
            self.sampled_points.clear()
            self.num_processed = min(self.num_processed + 1, len(self.meshes))
            self.cur_index = (self.cur_index + 1) % len(self.meshes)
            print(f"Process scan {self.cur_index} of {len(self.meshes)}")
        elif key == glfw.KEY_S:
            self.save_points()
        super().keyboard(window, key, scancode, action, mods)

    def mouse(self, window, button, action, mods):
        self.mode = "MOVE" if (mods & glfw.MOD_SHIFT) else "VIEW"
        super().mouse(window, button, action, mods)

    def motion(self, window, x, y):
        if self.mode == "MOVE":
            if self.button_down[0] and self.button_down[1]:  # Zoom
                dy = y - self.last_y
                tr = Transformation(0, 0, self.radius * dy * 2. / self.height)
                self.transformations[self.cur_index] = tr * self.transformations[self.cur_index]
            elif self.button_down[0]:  # Rotate
                last_point = self.map_to_sphere(self.last_x, self.last_y)
                new_point = self.map_to_sphere(x, y)
                axis = np.cross(last_point, new_point)
                cos_angle = np.dot(last_point, new_point)
                if abs(cos_angle) < 1.0:
                    angle = 1. * np.degrees(np.arccos(cos_angle))
                    tr = Transformation(angle, axis)
                    self.transformations[self.cur_index] = tr * self.transformations[self.cur_index]
        else:
            super().motion(window, x, y)

    def perform_registration(self, tangential_motion):
        mesh = self.meshes[self.cur_index]
        src_pts = np.array([mesh.point(vh) for vh in mesh.vertices()])
        self.sampled_points = self.subsample(src_pts)
        src = [self.transformations[self.cur_index].transform_point(src_pts[i]) for i in self.sampled_points]
        target_mesh = self.meshes[0]
        target = np.array([target_mesh.point(vh) for vh in target_mesh.vertices()])
        target_normals = np.array([target_mesh.normal(vh) for vh in target_mesh.vertices()])

        cp = ClosestPoint()
        cp.init(target)
        src_f, target_f, target_n_f = [], [], []
        self.calculate_correspondences(src, target, target_normals, cp, src_f, target_f, target_n_f)

        tr = (self.registration.register_point2surface(src_f, target_f, target_n_f) if tangential_motion
              else self.registration.register_point2point(src_f, target_f))
        self.transformations[self.cur_index] = tr * self.transformations[self.cur_index]
    
    def subsample(self, pts):
        """
        Task 1: Sample points uniformly on the source mesh.
        Goal: Average distance between sampled points should be ~subsample_radius.
        """
        subsample_radius = self.average_vertex_distance * 8 #You can change subsample_radius by the parameter equal 8
        sampled = []
        indices = list(range(len(pts)))

        # ----------------------------Insert your code here----------------------------------
        # - Start with all vertices and randomly shuffle them.
        # - Use a distance check to keep points ~subsample_radius apart.
        # ----------------------------End of code---------------------------------------------
        return sampled

    def calculate_correspondences(self, src, target, target_normals, cp, src_f, target_f, target_n_f):
        """
        Task 2: Find closest points and reject bad pairs.
        """
        distances = []
        mesh = self.meshes[0]

        # ----------------------------Insert your code here----------------------------------
        # - Check if vertex has neighbors
        # - Compute dot product of normals; reject if angle > 60 degrees.
        # - Reject pairs where distance > 3 * median distance.
        # - Update filtered arrays: src_f, target_f, target_n_f.
        # ----------------------------End of code---------------------------------------------
        pass

    def save_points(self):
        with open(self.output_filename, 'w') as f:
            for i, mesh in enumerate(self.meshes):
                pts = np.array([mesh.point(vh) for vh in mesh.vertices()]) 
                normals = np.array([mesh.normal(vh) for vh in mesh.vertices()])
                transformed_pts = self.transformations[i].transform_points(pts)

                rotation_matrix = self.transformations[i].rotation
                transformed_normals = np.dot(normals, rotation_matrix.T)

                for pt, normal in zip(transformed_pts, transformed_normals):
                    f.write(f"v {pt[0]} {pt[1]} {pt[2]} vn {normal[0]} {normal[1]} {normal[2]}\n")
        print(f"Saved points to {self.output_filename}")