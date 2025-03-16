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
from transformation import Transformation

class Registration:
    def register_point2point(self, src, target):
        """
        Task 3: Implement point-to-point registration.
        """
        n = len(src)
        A = np.zeros((n * 3, 6))  # 3 equations per point, 6 unknowns (α, β, γ, tx, ty, tz)
        b = np.zeros(n * 3)       # Residuals for x, y, z per point 
        for i, (s, t) in enumerate(zip(src, target)):
            pass  # Replace with A and b assignments
        # ----------------------------Insert your code here----------------------------------
        # - For each point pair (s, t), set up 3 rows in A for x, y, z residuals.
        # - Set up A matrix (N x 6) and b vector (N x 1) for Ax = b.
        # ----------------------------End of code--------------------------------------------- 
        x = np.linalg.lstsq(A, b, rcond=None)[0]
        return Transformation.from_angles_and_translation(x[:3], x[3:])

    def register_point2surface(self, src, target, target_normals):
        """
        Task 4: Implement point-to-plane registration.
        """
        n = len(src)
        A = np.zeros((n, 6))  # 1 equation per point, 6 unknowns (α, β, γ, tx, ty, tz)
        b = np.zeros(n)       # Residuals (distance to plane)
        for i, (s, t, n) in enumerate(zip(src, target, target_normals)):
            pass  # Replace with A and b assignments
        # ----------------------------Insert your code here----------------------------------
        # - For each triplet (s, t, n), error is n^T (R * s + t - t).
        # - Compute cross product s × n for rotation terms (α, β, γ).
        # - Use normal n directly for translation terms (tx, ty, tz).
        # - b[i] = n^T (t - s), the signed distance from s to the plane at t.
        # ----------------------------End of code--------------------------------------------- 
        
        x = np.linalg.lstsq(A, b, rcond=None)[0]
        return Transformation.from_angles_and_translation(x[:3], x[3:])