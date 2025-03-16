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

class Transformation:
    def __init__(self, angle=None, axis=None, translation=None):
        if angle is not None and axis is not None:
            angle_rad = np.radians(angle)
            c, s = np.cos(angle_rad), np.sin(angle_rad)
            if np.linalg.norm(axis) > 1e-6:
                n = axis / np.linalg.norm(axis)
                self.rotation = (
                    c * np.eye(3) + (1 - c) * np.outer(n, n) + s * np.cross(np.eye(3), n)
                )
                self.translation = np.zeros(3) if translation is None else translation
            else:
                self.rotation = np.eye(3)
                self.translation = np.zeros(3)
        else:
            self.rotation = np.eye(3)
            self.translation = np.zeros(3) if translation is None else translation

    @classmethod
    def from_angles_and_translation(cls, angles, translation):
        tr = cls()
        alpha, beta, gamma = angles
        sa, ca = np.sin(alpha), np.cos(alpha)
        sb, cb = np.sin(beta), np.cos(beta)
        sr, cr = np.sin(gamma), np.cos(gamma)
        tr.rotation = np.array([
            [cb * cr, -cb * sr, sb],
            [sa * sb * cr + ca * sr, -sa * sb * sr + ca * cr, -sa * cb],
            [-ca * sb * cr + sa * sr, ca * sb * sr + sa * cr, ca * cb]
        ])
        tr.translation = translation
        return tr

    def to_matrix(self):
        mat = np.eye(4)
        mat[:3, :3] = self.rotation
        mat[:3, 3] = self.translation
        return mat

    def transform_point(self, p):
        return self.rotation @ p + self.translation

    def transform_points(self, ps):
        return (self.rotation @ ps.T).T + self.translation

    def __mul__(self, other):
        result = Transformation()
        result.rotation = self.rotation @ other.rotation
        result.translation = self.rotation @ other.translation + self.translation
        return result

    def inverse(self):
        result = Transformation()
        result.rotation = self.rotation.T
        result.translation = -self.rotation.T @ self.translation
        return result