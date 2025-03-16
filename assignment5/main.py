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
from app import RegistrationViewerApp
import glfw

@click.command()
@click.option('--output_file', type=str, required=True, help='Path to the output file')
@click.argument('mesh_files', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--window_width', type=int, default=512, help='Window width')
@click.option('--window_height', type=int, default=512, help='Window height')
def main(output_file, mesh_files, window_width, window_height):
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    # Request OpenGL 3.3 core profile
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)  # For macOS compatibility

    viewer = RegistrationViewerApp("Registration Viewer", window_width, window_height)
    viewer.set_output(output_file)
    viewer.open_meshes(mesh_files)
    viewer.run()

    glfw.terminate()

if __name__ == "__main__":
    main()