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

import openmesh as om
import numpy as np
from OpenGL.GL import *


class MeshViewer:
    def __init__(self, filename: str):
        self.mesh = om.read_trimesh(filename)
        if self.mesh is None:
            raise ValueError(f"Could not read mesh from file: {filename}")

        print(f"Loaded mesh with {self.mesh.n_vertices()} vertices, {self.mesh.n_faces()} faces")
        indices = []
        for fh in self.mesh.faces():
            vs = [vh.idx() for vh in self.mesh.fv(fh)]
            if len(vs) == 3:
                indices.extend(vs)
        self.indices = np.array(indices, dtype=np.uint32)

        self.n_verts = self.mesh.n_vertices()
        self.positions = np.zeros((self.n_verts, 3), dtype=np.float32)
        self.normals   = np.zeros((self.n_verts, 3), dtype=np.float32)
        self.valences = self.calc_valences()
        self.colors = self.color_coding()

        for vh in self.mesh.vertices():
            idx = vh.idx()
            p = self.mesh.point(vh)
            self.positions[idx] = [p[0], p[1], p[2]]
        self.compute_normals()

        self._setup_gl_buffers()

    def compute_normals(self):
        self.normals.fill(0)

        for fh in self.mesh.faces():
            vertices = [self.mesh.point(vh) for vh in self.mesh.fv(fh)]
            edge1 = vertices[1] - vertices[0]
            edge2 = vertices[2] - vertices[0]

            face_normal = np.cross(edge1, edge2)
            face_normal /= np.linalg.norm(face_normal)

            for vh in self.mesh.fv(fh):
                self.normals[vh.idx()] += face_normal

        for i in range(self.normals.shape[0]):
            self.normals[i] /= np.linalg.norm(self.normals[i])

    def calc_valences(self):
        # Compute valence of every vertex of "self.mesh"
        ### Your code starts from here ###
        colors    = np.zeros((self.n_verts, 3), dtype=np.float32)
        ### End of your code ###
        return colors

    def color_coding(self):
        # Implement a color visualization of your choice that shows the valence of
        # each vertex of "self.mesh". 
        ### Your code starts from here ###
        valences    = np.zeros((self.n_verts, 3), dtype=np.float32)
        ### End of your code ###
        return valences

    def _setup_gl_buffers(self):
        n_verts = len(self.positions)
        interleaved = np.concatenate([
            self.positions, self.normals, self.colors
        ], axis=1).astype(np.float32).ravel()

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, interleaved.nbytes, interleaved, GL_STATIC_DRAW)

        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        stride = 9 * np.dtype(np.float32).itemsize

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(24))

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glBindVertexArray(0)

    def destroy(self):
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])
        glDeleteBuffers(1, [self.ebo])
