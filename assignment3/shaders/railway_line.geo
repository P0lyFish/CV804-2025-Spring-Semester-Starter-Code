//=============================================================================
//                                                
//   Code framework for the lecture
//
//   "CV804: 3D Geometry Processing"
//
//   Lecturer: Hao Li
//   TAs: Phong Tran, Long Nhat Ho, Ekaterina Radionova
//
//   Copyright (C) 2025 Metaverse Lab
//                                                                         
//-----------------------------------------------------------------------------
//                                                                            
//                                License                                     
//                                                                            
//   This program is free software; you can redistribute it and/or
//   modify it under the terms of the GNU General Public License
//   as published by the Free Software Foundation; either version 2
//   of the License, or (at your option) any later version.
//   
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//   
//   You should have received a copy of the GNU General Public License
//   along with this program; if not, write to the Free Software
//   Foundation, Inc., 51 Franklin Street, Fifth Floor, 
//   Boston, MA  02110-1301, USA.
//                                                                            
//=============================================================================
//=============================================================================


#version 330 core

#define M_PI 3.1415926535897932384626433832795
#define NUM_SAMPLES 32

layout (lines) in;
layout (triangle_strip, max_vertices = 66) out;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float radius;

in vec3 vNormal[];
in vec3 vForward[];
in vec3 vColor[];
out vec3 gColor;


vec3 rotate(vec3 x, vec3 n, float alpha) {
    // Rotate vector x along the axis of rotation n by an angle of alpha (in radian).
    // Checkout Rodrigues' rotation formula.

    vec3 x_rot = x;
    return x_rot;
}


void main() {
    float radius = 0.0005;

    vec3 p0 = gl_in[0].gl_Position.xyz;
    vec3 n0 = normalize(vNormal[0]) * radius;
    vec3 f0 = vForward[0];

    vec3 p1 = gl_in[1].gl_Position.xyz;
    vec3 n1 = normalize(vNormal[1]) * radius;
    vec3 f1 = vForward[1];
    
    float angle_step = 2 * M_PI / NUM_SAMPLES;
    for (int i = 0; i <= NUM_SAMPLES; ++i) {
        float alpha = angle_step * i;
        vec3 v0 = p0 + rotate(n0, f0, alpha);
        vec3 v1 = p1 + rotate(n1, f1, alpha);

        gl_Position = projection * view * model * vec4(v0, 1.0);
        gColor= vColor[0];
        EmitVertex();

        gl_Position = projection * view * model * vec4(v1, 1.0);
        gColor = vColor[1];
        EmitVertex();
    }
    EndPrimitive();
}
