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

in vec3 fragPos;
in vec3 fragNormal;
in vec3 fragColor;

flat in vec3 flatNormal;

out vec4 finalColor;

struct Light {
    vec3 position;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

uniform Light lights[3];
uniform Material material;
uniform vec3 viewPos;
uniform int useValenceColor;
uniform int shadingMode;     // 0 for flat, 1 for smooth
uniform int enableLighting;  // 1 to enable lighting, 0 to disable
uniform vec4 faceColor;      // Color for faces in wireframe/hidden line modes

vec3 calculateLight(Light light, vec3 normal, vec3 fragPos, vec3 viewDir, vec3 baseColor) {
    // Ambient
    vec3 ambient = light.ambient * material.ambient * baseColor;

    // Diffuse
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = light.diffuse * (diff * material.diffuse * baseColor);

    // Specular
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = light.specular * (spec * material.specular);

    return ambient + diffuse + specular;
}

void main()
{
    if (enableLighting == 0) {
        finalColor = faceColor; // Render without lighting
    } else {
        vec3 baseColor = (useValenceColor == 1) ? fragColor : vec3(1.0, 1.0, 1.0);

        // Choose the normal based on the shading mode
        vec3 normal = (shadingMode == 0) ? flatNormal : fragNormal;
        vec3 viewDir = normalize(viewPos - fragPos);

        vec3 result = vec3(0.0);
        for (int i = 0; i < 3; i++) {
            result += calculateLight(lights[i], normal, fragPos, viewDir, baseColor);
        }

        finalColor = vec4(result, 1.0); // Opaque with lighting
    }
}
