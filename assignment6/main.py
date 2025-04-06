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


import click
import numpy as np
import open3d as o3d
import os
import os.path as osp
import skimage

from implicit_hoppe import ImplicitHoppe
from implicit_rbf import ImplicitRBF


GRID_RESOLUTION = 100


# Modified from https://github.com/NVlabs/eg3d/blob/main/eg3d/shape_utils.py#L40
def convert_sdf_samples_to_ply(
    numpy_3d_sdf_tensor,
    voxel_size,
    voxel_grid_origin=np.array([0, 0, 0], dtype=np.float32),
    offset=None,
    scale=None,
    level=0.0
):
    """
    Convert sdf samples to .ply
    :param pytorch_3d_sdf_tensor: a torch.FloatTensor of shape (n,n,n)
    :voxel_grid_origin: a list of three floats: the bottom, left, down origin of the voxel grid
    :voxel_size: float, the size of the voxels
    :ply_filename_out: string, path of the filename to save to
    This function adapted from: https://github.com/RobotLocomotion/spartan
    """

    verts, faces, normals, values = np.zeros((0, 3)), np.zeros((0, 3)), np.zeros((0, 3)), np.zeros(0)
    verts, faces, normals, values = skimage.measure.marching_cubes(
        numpy_3d_sdf_tensor, level=level, spacing=[voxel_size] * 3
    )

    # transform from voxel coordinates to camera coordinates
    # note x and y are flipped in the output of marching_cubes
    mesh_points = np.zeros_like(verts)
    mesh_points[:, 0] = voxel_grid_origin[0] + verts[:, 0]
    mesh_points[:, 1] = voxel_grid_origin[1] + verts[:, 1]
    mesh_points[:, 2] = voxel_grid_origin[2] + verts[:, 2]

    # apply additional offset and scale
    if scale is not None:
        mesh_points = mesh_points / scale
    if offset is not None:
        mesh_points = mesh_points - offset

    mesh_points = (mesh_points - mesh_points.mean(axis=0)) / mesh_points.max()

    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(mesh_points)
    mesh.triangles = o3d.utility.Vector3iVector(faces[:, [2, 1, 0]])
    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()
    mesh.vertex_normals = o3d.utility.Vector3dVector(normals)

    return mesh


@click.command()
@click.option('--input_path', type=str, required=True, help='Input path (points and normals)')
@click.option('--mesh_save_path', type=str, required=True, help='Mesh save path')
@click.option('--mode', type=click.Choice(['hoppe', 'rbf']), required=True, help='Reconstruction algorithm')
@click.option(
    '--show_input_only', type=bool, is_flag=True, default=False, help='For debugging: Visualize input points and normals'
)
def main(input_path: str, mesh_save_path: str, mode: str, show_input_only: bool):
    assert mesh_save_path.lower().endswith('.ply'), 'Mesh save path must be a ply file'
    assert osp.isfile(input_path), 'The input file does not exist'

    # Load points and normals
    points = []
    normals = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            x, y, z, _, n1, n2, n3 = line.strip().split(' ')  # There are two spaces between points and normals
            points.append((x, y, z))
            normals.append((n1, n2, n3))

    points = np.array(points, dtype=np.float32)
    normals = np.array(normals, dtype=np.float32)

    # For debugging
    if show_input_only:
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.normals = o3d.utility.Vector3dVector(normals)
        o3d.visualization.draw_geometries([pcd], point_show_normal=True)
        return

    recon_class = ImplicitHoppe if mode == 'hoppe' else ImplicitRBF
    recon = recon_class(points, normals)

    bb_min = points.min(axis=0)
    bb_max = points.max(axis=0)
    eps = (bb_max - bb_min) * 0.05
    bb_min = bb_min - eps
    bb_max = bb_max + eps

    grid_positions = np.stack(np.meshgrid(*np.linspace(bb_min, bb_max, GRID_RESOLUTION).transpose()))
    grid_positions = np.transpose(grid_positions, (1, 2, 3, 0)).reshape(-1, 3)

    grid_density = recon(grid_positions).reshape([GRID_RESOLUTION,] * 3)

    mesh = convert_sdf_samples_to_ply(grid_density, voxel_size=0.1, level=0)
    mesh.subdivide_midpoint(number_of_iterations=4)
    mesh = mesh.filter_smooth_simple(number_of_iterations=1)
    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()

    os.makedirs(osp.dirname(mesh_save_path), exist_ok=True)
    o3d.io.write_triangle_mesh(mesh_save_path, mesh)
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)


if __name__ == '__main__':
    main()
