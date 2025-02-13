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

from app import RollerCoasterApp


@click.command()
@click.option('--sky_texture_path', type=str, default='./assets/textures/sky.png', help='Sky texture path')
@click.option('--ground_texture_path', type=str, default='./assets/textures/ground.jpg', help='Ground texture path')
@click.option('--ties_texture_path', type=str, default='./assets/textures/ties.png', help='Ties texture path')
@click.option('--railway_path', type=str, default='./assets/spline_data/circle.sp', help='Ties texture path')
@click.option('--window_width', type=int, default=800, help='Window width')
@click.option('--window_height', type=int, default=800, help='Window height')
def main(
    sky_texture_path: str,
    ground_texture_path: str,
    ties_texture_path: str,
    railway_path: str,
    window_width: int,
    window_height: int
):
    app = RollerCoasterApp(
        sky_texture_path=sky_texture_path,
        ground_texture_path=ground_texture_path,
        ties_texture_path=ties_texture_path,
        railway_path=railway_path,
        window_width=window_width,
        window_height=window_height
    )
    app.run()
    app.quit()


if __name__ == '__main__':
    main()
