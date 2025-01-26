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

import click
from app import ValenceApp

@click.command()
@click.option('--mesh_path', type=str, default='data/bunny.off', help='Mesh path')
@click.option('--window_width', type=int, default=800, help='Window width')
@click.option('--window_height', type=int, default=600, help='Window height')
def main(mesh_path, window_width, window_height):
    app = ValenceApp(mesh_path=mesh_path, width=window_width, height=window_height)
    app.run()

if __name__ == '__main__':
    main()