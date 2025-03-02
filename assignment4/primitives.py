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

from utils import Vec3

class Vertex:
    def __init__(self, pos, diffuse, specular, normal, shininess):
        self.pos = pos
        self.diffuse = diffuse
        self.specular = specular
        self.normal = normal
        self.shininess = shininess

class Triangle:
    def __init__(self, v0, v1, v2):
        self.vertices = [v0, v1, v2]

class Sphere:
    def __init__(self, pos, radius, diffuse, specular, shininess):
        self.pos = pos
        self.radius = radius
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess