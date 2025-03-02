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

from light import Light
from primitives import Triangle, Sphere, Vertex
from utils import Vec3

class Scene:
    def __init__(self):
        self.ambient = Light(Vec3(0, 0, 0), Vec3(0.1, 0.1, 0.1))
        self.triangles = []
        self.spheres = []
        self.lights = []
        self.camera_pos = Vec3(0, 0, 0)

    def load_scene(self, path):
        with open(path, 'r') as f:
            num_objects = int(f.readline().strip())
            self.ambient.color = Vec3(*map(float, f.readline().split()[1:4]))
            for _ in range(num_objects):
                line = f.readline().strip().split()
                obj_type = line[0]
                if obj_type == "triangle":
                    vertices = []
                    for _ in range(3):
                        pos = Vec3(*map(float, f.readline().split()[1:4]))
                        normal = Vec3(*map(float, f.readline().split()[1:4])).normalize()
                        diffuse = Vec3(*map(float, f.readline().split()[1:4]))
                        specular = Vec3(*map(float, f.readline().split()[1:4]))
                        shininess = float(f.readline().split()[1])
                        vertices.append(Vertex(pos, diffuse, specular, normal, shininess))
                    self.triangles.append(Triangle(*vertices))
                elif obj_type == "sphere":
                    pos = Vec3(*map(float, f.readline().split()[1:4]))
                    radius = float(f.readline().split()[1])
                    diffuse = Vec3(*map(float, f.readline().split()[1:4]))
                    specular = Vec3(*map(float, f.readline().split()[1:4]))
                    shininess = float(f.readline().split()[1])
                    self.spheres.append(Sphere(pos, radius, diffuse, specular, shininess))
                elif obj_type == "light":
                    pos = Vec3(*map(float, f.readline().split()[1:4]))
                    color = Vec3(*map(float, f.readline().split()[1:4]))
                    self.lights.append(Light(pos, color))