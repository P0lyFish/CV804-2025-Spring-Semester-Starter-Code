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


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple


ORI_VIS_LEN = 0.3


class Spline:
    def __init__(self, points):
        assert len(points) >= 4

        points = np.array(points)

        # Padding the first and last control points
        self._points = np.zeros([points.shape[0] + 2, 3])
        self._points[1: -1, :] = points
        self._points[0] = points[0]
        self._points[-1] = points[-1]

        self._num_points = self._points.shape[0]
        self._segment_lengths = np.zeros(self._num_points - 1)
        for i in range(self._num_points - 1):
            self._segment_lengths[i] = np.sqrt(((self._points[i + 1] - self._points[i]) ** 2).sum())

        self._total_length = np.sum(self._segment_lengths)

    @staticmethod
    def _catmull_rom(points: NDArray[np.float32], t: float) -> NDArray[np.float32]:
        assert points.shape[0] == 4
        assert t >= 0 and t <= 1
        """
        Calculate and return the coordinate of the point at t. t is normalized to [0, 1] using the length of the spline created using the four input points.

        hint:
            - Check the equation provided in the README.

        parameters:
            points (NDArray[np.float32]): 4 points on the spline.
            t (float):  Normalized position on the spline.
        return:
            q (NDArray[np.float32]): the point at position t.
        """
        q = np.empty((3), dtype=np.float32)

        return q

    def __call__(self, t: float) -> NDArray[np.float32]:
        assert t >= 0 and t <= 1
        """
        Calculate and return the coordinate of the point at t. t is normalized to [0, 1] using the total length of the spline created from all the points.

        hint:
            - The calculated data in __init__ is already enough for this method.
            - Break the task into smaller subtask and use _catmull_rom method.

        Parameters:
            - t (float): The normalized position on the spline.
        Return:
            - q (NDArray[np.float32]): The point at position t.
        """
        q = np.empty((3), dtype=np.float32)

        return q



def sloan_method(
    points: NDArray[np.float32]
) -> Tuple[List[NDArray[np.float32]], List[NDArray[np.float32]], List[NDArray[np.float32]]]:
    '''
        Calculate the TNB frames of the input points.

        Hint:
            - Check the formula given in the README file.

        Paramerers:
            - points (NDArray[np.float32]): The input points.
        Returns:
            - Ts: The list of T vectors (Has equal length with the input points).
            - Ns: The list of N vectors (Has equal length with the input points).
            - Bs: The list of B vectors (Has equal length with the input points).
    '''

    Ts = []
    Ns = []
    Bs = []

    return Ts, Ns, Bs


def animate(frame_idx, particle, orientation_lines, x_railroad, y_railroad, z_railroad, Ts, Ns, Bs):
    p = np.array([x_railroad[frame_idx], y_railroad[frame_idx], z_railroad[frame_idx]])
    T = Ts[frame_idx]
    N = Ns[frame_idx]
    B = Bs[frame_idx]

    assert np.isclose(np.linalg.norm(T), 1 + 1e-6)
    assert np.isclose(np.linalg.norm(B), 1 + 1e-6)
    assert np.isclose(np.linalg.norm(N), 1 + 1e-6)

    # Update particle's position
    particle.set_data(p[0: 1], p[1: 2])
    particle.set_3d_properties(p[2: 3])

    # Update particle's orientations
    for i, vec in enumerate([T, N, B]):
        orientation_lines[i].set_data(
            [p[0], p[0] + ORI_VIS_LEN * vec[0]],
            [p[1], p[1] + ORI_VIS_LEN * vec[1]]
        )
        orientation_lines[i].set_3d_properties([p[2], p[2] + ORI_VIS_LEN * vec[2]])

    return [particle,] + orientation_lines


if __name__ == '__main__':
    with open('assets/spline_data/circle.sp', 'r') as f:
        f.readline()
        points = [list(map(float, line.split(' '))) for line in f]

    spline = Spline(points)

    # Set Seaborn style
    sns.set_theme(style="whitegrid")

    # Create figure and axis
    fig = plt.figure()
    ax = plt.subplot(111, projection='3d')

    # Plot the railroad
    x_railroad, y_railroad, z_railroad = [], [], []
    for t in np.linspace(0, 0.99, 1000):  # Only go to 0.99 to avoid numerical issue
        p = spline(t)
        x_railroad.append(p[0])
        y_railroad.append(p[1])
        z_railroad.append(p[2])
    ax.plot(x_railroad, y_railroad, z_railroad)

    # Prepare the particle and the orientations
    particle, = ax.plot([x_railroad[0]], [y_railroad[0]], [z_railroad[0]], 'ro') # 'ro' creates a red circle marker

    # Generate the orientations
    [Ts, Ns, Bs] = sloan_method(np.stack((x_railroad, y_railroad, z_railroad), axis=1))

    orientation_colors = ['r', 'g', 'b']
    orientation_lines = []
    for i, ori in enumerate([Ts[0], Ns[0], Bs[0]]):
        line, = ax.plot(
            [x_railroad[0], x_railroad[0] + ORI_VIS_LEN * ori[0]],
            [y_railroad[0], y_railroad[0] + ORI_VIS_LEN * ori[1]],
            [z_railroad[0], z_railroad[0] + ORI_VIS_LEN * ori[2]],
            color=orientation_colors[i]
        )
        orientation_lines.append(line)

    # Animate the car
    num_frames = 1000
    ani = FuncAnimation(
        fig,
        lambda frame: animate(
            frame, particle, orientation_lines, x_railroad, y_railroad, z_railroad, Ts, Ns, Bs
        ),
        frames=np.arange(0, num_frames - 1, 2),
        blit=False
    )

    # Show plot
    plt.show()
