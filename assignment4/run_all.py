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

import os
from app import RaytracerApp

# Define directories
SCENES_DIR = "./scenes_data"
RESULTS_DIR = "./results"
os.makedirs(RESULTS_DIR, exist_ok=True)

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

def main():
    scene_files = [f for f in os.listdir(SCENES_DIR) if f.endswith(".scene")]
    
    if not scene_files:
        print("No .scene files found in", SCENES_DIR)
        return
    
    # Process each scene file
    for scene_file in scene_files:
        scene_path = os.path.join(SCENES_DIR, scene_file)
        output_filename = scene_file.replace(".scene", ".png")
        save_path = os.path.join(RESULTS_DIR, output_filename)
        
        print(f"Rendering {scene_path} -> {save_path}")
        
        # Create and run the RaytracerApp instance
        app = RaytracerApp(
            scene_path=scene_path,
            save_path=save_path,
            window_width=WINDOW_WIDTH,
            window_height=WINDOW_HEIGHT
        )
        app.run()
        
        print(f"Finished rendering {scene_file}")

if __name__ == "__main__":
    main()