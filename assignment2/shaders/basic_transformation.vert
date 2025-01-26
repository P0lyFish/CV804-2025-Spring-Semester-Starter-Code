//=============================================================================
//                                                
//   Code framework for the lecture
//
//   "CV804: 3D Geometry Processing"
//
//   Lecturer: Hao Li
//   TAs: Phong Tran, Long Nhat Ho
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

layout(location = 0) in vec3 vertexPos;
layout(location = 1) in vec3 vertexNormal;
layout(location = 2) in vec3 vertexColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform int shadingMode; // 0 for flat, 1 for smooth

out vec3 fragPos;
out vec3 fragNormal;
out vec3 fragColor;

flat out vec3 flatNormal;

void main()
{
    gl_Position = projection * view * model * vec4(vertexPos, 1.0);

    mat3 normalMatrix = transpose(inverse(mat3(model)));

    // For flat shading, pass the normal as a constant per face
    if (shadingMode == 0) {
        flatNormal = normalize(normalMatrix * vertexNormal);
    }

    // For smooth shading, interpolate the normal
    fragNormal = normalize(normalMatrix * vertexNormal);

    fragPos = (model * vec4(vertexPos, 1.0)).xyz;
    fragColor = vertexColor;
}
