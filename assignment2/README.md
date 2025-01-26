# Assignment #2 
<div align="center">
  <img src="./assets/teaser.gif" alt="Teaser" title="Placeholder" />
</div>

## Introduction
The aim of the first exercise sheet is to make yourself familiar with the provided mesh processing framework and to implement a simple vertex valence visualization of a mesh using OpenMesh.

The valence v(x<sub>i</sub>) of a vertex x<sub>i</sub> in a triangle mesh is the number of vertices in the 1-ring neighborhood N(x<sub>i</sub>) of x<sub>i</sub>. In particular, the vertices of N(x<sub>i</sub>) are connected with an edge to x<sub>i</sub>. In this assignment, you will color each vertex using its valence.

To make your life easier, we provide a minimal codebase which already implemented a few basic functionality of a mesh viewer:
- **Zoom in/out**: The user can scale the mesh by scrolling the middle mouse button.
- **Rotation**: User can rotate the mesh by dragging the mouse while holding the left button.
- **Rendering mode (Wireframe/Hidden Line/Solid Flat/Solid Smooth/Vertex Valences)**: The application can render the mesh with different modes. The "vertex valences" mode will be implemented by you. The modes are implemented by buttons `1`, `2`, `3`, `4`. The Vertex Valences mode is supposed to be by `5`.
- **Performance testing**: When pressing `f`, the application will run a performance test.


## Installing Dependencies
We highly recommend to use conda environment. The dependencies are provided in: `requirements.txt`. 

## Run Your Code
You can run the code by the following command:
```
python main.py --mesh_path './data/bunny.off' 
```

## Tasks
Your task is to build the "Vertex Valences" rendering mode. To do so, you have to fill the two missing functions:
- `calc_valences` in `mesh_viewer.py`: This function calculates all the valences of each vertex.
- `color_coding` in `mesh_viewer.py`: Having the valences of all the vertices, now you have to map them to a color map, e.g. Jet Color, or the one we provided in `data/colors.png`.

## Free Tips
- You may need to calculate the maximum and minimum valences.
- You can use any color map that you want, or just use the color map we provided in `data/colors.png`. If you use a customized color map, describe it in the readme file.
- Feel free to modify any part of the code, but remember to describe your changes in the readme file.

## We Value Creativity!
Well, the assignment is pretty simple. Try to find a way to make your homework distinguish. For example, you can add more features to the program, or use another meshes, etc. We will give you some credit scores (up to 10%) if we think your program is intesting.
