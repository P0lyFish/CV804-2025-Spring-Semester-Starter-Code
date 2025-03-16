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
in vec3 fragPos;
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
uniform vec3 viewPos = vec3(0.0, 0.0, 0.0); // Camera at origin in view space
uniform int shadingMode;
uniform int enableLighting; // 1 to enable, 0 to disable

vec3 calculateLight(Light light, vec3 normal, vec3 fragPos, vec3 viewDir) {
    vec3 ambient = light.ambient * material.ambient;
    
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = light.diffuse * (diff * material.diffuse);
    
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = light.specular * (spec * material.specular);
    
    return ambient + diffuse + specular;
}

void main() {
    if (enableLighting == 0) {
        finalColor = vec4(0.5, 0.5, 0.5, 1.0);
    } else {
        vec3 normal = normalize(flatNormal);
        vec3 viewDir = normalize(viewPos - fragPos);
        vec3 result = vec3(0.0);
        for (int i = 0; i < 3; i++) {
            result += calculateLight(lights[i], normal, fragPos, viewDir);
        }
        finalColor = vec4(result, 1.0);
    }
}