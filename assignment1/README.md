# Assignment #1

<div align="center">
  <img src="./assets/teaser.gif" alt="Teaser" title="Placeholder" />
</div>

## Introduction
This assignment is intended as a hands-on introduction to OpenGL and programming in three dimensions. The starter code we provide is minimal, giving only the functionality to read and write an  image and handle mouse and keyboard input. You must write the code to create a window, handle camera transformations, perform rendering, and handle any other functionality you may desire. 

A height field is a visual representation of a function which takes as input a two-dimensional point and returns a scalar value ("height") as output. In other words, a function f takes x and y coordinates and returns a z coordinate.

Rendering a height field over arbitrary coordinates is somewhat tricky--we will simplify the problem by making our function piece-wise. Visually, the domain of our function is a two-dimensional grid of points, and a height value is defined at each point. We can render this data using only a point at each defined value, or use it to approximate a surface by connecting the points with triangles in 3D.

## Installing Dependencies
We highly recommend using conda to install the depenencies:
```
conda env create -f environment.yml
```

## Run Your Code
you can run the code by the following command:
```
python main.py --height_map_path './data/OhioPyle-256.jpg' \
               --window_width 800 \
               --window_height 600
```
This command will load the height map `./data/OhioPyle-256.jpg` and create a window of size `800x600`.

## Tasks
Your final goal is to build a height field rendering application. The input of the program is a height field map which is represented as a gray image. Your program needs to have the following features:
- Be able to handle at least a 768x768 image for your height field at interactive frame rates (window size of 1980x1280). Height field manipulations should run smoothly.
- Be able to render the height field as points, lines("wireframe"), or solid triangles (with keys for the user to switch between the three).
- Render as a perspective view, utilizing GL's depth buffer for hidden surface removal.
- Use input from the mouse to spin the heightfield around.
- Use input from the mouse to move the heightfield around.
- Use input from the mouse to scale of the heightfield.
- Color the vertices using the height or some smooth gradients.
- Be reasonably commented and written in an understandable manner--we will read your code.

You may choose to implement any combination of the following for extra credit:
- Experiment with material and lighting properties.
- Render wireframe on top of solid triangles (use glPolygonOffset to avoid z-buffer fighting).
- Color the vertices based on color values taken from another image of equal size. However, your code should still support also smooth color gradients as per the core requirements.
- Texturemap the surface with an arbitrary image.
- Allow the user to interactively deform the landscape.

***Please note that the amount of extra credit awarded will not exceed 10% of the assignment's total value.***


## Starter Code Instructions
Here we provide you a starter code to make your life easier. All you need to do is filling the missing functions:

- Height map and texture loading (`_load_height_map` method in `height_map.py`).
- Building vertex data (`_build_vertex_data` method in `height_map.py`).
- Updating model transformation (`update_model_transformation` method in `height_map.py`).
- Drawing the height map (`draw` method in `height_map.py`).
- Cleaning the buffers of the height map object (`destroy` method in `height_map.py`).
- Creating the window (`_create_window` method in `height_map.py`).
- Creating shader program (`_create_shader` method in `app.py`).
- Creating the camera projection transformation matrix and passing it to the vertex shader (`_init_projection_transform` method in `height_map.py`).
- Passing the modelview transformation matrix from height map object to the vertex shader (`_update_modelview_transform` in `height_map.py`).
- The main loop of GLFW (`_main_loop` method in `height_map.py`).

We highly recommend checking all the code before starting your implementation. After finish your implementation, your program should look like the teaser above.


## Free Tips
- Make sure the starter code works on your machine.
- Familiarize yourself with GL's viewing transformations before attempting to render the height field itself. Try rendering a simple object first. You can use `pyrr` library to create projection and modelview transformation matrices.
- In the projection transformation, the near and far values for clipping plane have to be positive. You will see weird problems if they are zero or negative.
- Finish your program completely before worrying about the animation.
- Don't try to do this at the last minute. This assignment is supposed to be fun and relatively easy, but time pressure has a way of ruining that notion.
- Don't over-stretch the z-buffer. It has only finite precision. For this assignment, a good range of the near and far planes is [0.01, 10].
- When creating a numpy array, always remember to set the data type (dtype) of the array, otherwise you can encounter very weird bugs.
- ***If you stuck somewhere, contact the TAs for necessary assistance.***


## Show People What You Got!!!
There is a large amount of room for creatitiy in terms of how you choose to show your results in the animation. You can use our provided input images, or modify them with any software you wish, or use your own input images. You may also use your animation to show off any extra features you choose to implement. Your animation will receive credit based on its artistic content, whether pretty, funny, or just interesting in some manner.

We recommend to use builtin record application of your OS (e.g. [MacOS](https://support.apple.com/en-ae/102618), [Ubuntu](https://help.ubuntu.com/stable/ubuntu-help/screen-shot-record.html)) to record your animation. We will compile a video of all student submissions and show it in class.
