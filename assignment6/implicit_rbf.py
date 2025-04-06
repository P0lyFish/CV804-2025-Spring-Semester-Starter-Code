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
import numpy.typing as npt
import scipy


class ImplicitRBF:
    def __init__(self, points: npt.NDArray[np.float32], normals: npt.NDArray[np.float32]) -> None:
        ######################################################################
        ## INSERT CODE:
        ## 1) collect constraints (on-surface and off-surface)
        ## get bounding box, recalculate because do not want to change reconstruct.cc

        ## 2) setup matrix
        ## Check the slides for the formula

        ## 3) solve linear system for self._weights
        
        ######################################################################
        N = points.shape[0]
        M = np.zeros((N, N))
        d = np.zeros(N)

        self._weights = np.linalg.solve(M, d)

    def __call__(self, P: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
        '''
        Calculating the signed distances of the input batched points P using implicit hoppe algorithm.
        Do not use any for-loop here.

        Parameters:
            - P(NDArray[float32]): input points Nx3.
        Returns:
            - dist(NDArray[float32]): signed distance values with shape N.
        '''

        pass
