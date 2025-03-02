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
out vec4 FragColor;
in vec2 uv;

uniform vec3 camera_pos;
uniform float aspect_ratio;
uniform float fov_tan;

struct Light {
    vec3 pos;
    vec3 color;
};
uniform Light ambient_light;
uniform Light lights[32];
uniform int num_lights;

struct Sphere {
    vec3 pos;
    float radius;
    vec3 diffuse;
    vec3 specular;
    float shininess;
};
uniform Sphere spheres[32];
uniform int num_spheres;

struct Triangle {
    vec3 v0, v1, v2;
    vec3 n0, n1, n2;
    vec3 diffuse0, diffuse1, diffuse2;
    vec3 specular0, specular1, specular2;
    float shininess0, shininess1, shininess2;
};
uniform Triangle triangles[32];
uniform int num_triangles;

const float EPS = 1e-6;
const vec3 BACKGROUND_COLOR = vec3(1.0, 1.0, 1.0);

float sphere_intersect(vec3 ro, vec3 rd, vec3 center, float radius) {
    // ----------------------------Insert your code here----------------------------------
    // Calculate the closest intersection of the ray with the sphere
    // Hints:
    // - ro is ray origin, rd is ray direction
    // - Use the quadratic formula to solve for t (ray parameter)
    // - Return -1.0 if no intersection or if t <= 0
    // ----------------------------End of code---------------------------------------------
    return -1.0;
}

vec3 barycentric(vec3 p, vec3 a, vec3 b, vec3 c) {
    // ----------------------------Insert your code here----------------------------------
    // Calculate the barycentric coordinates of point p with respect to triangle abc
    // Hints:
    // - Use cross products or dot products to compute areas
    // - Return vec3(u, v, w) where u + v + w = 1
    // ----------------------------End of code---------------------------------------------
    return vec3(0.0, 0.0, 0.0);
}

float triangle_intersect(vec3 ro, vec3 rd, Triangle tri) {
    // ----------------------------Insert your code here----------------------------------
    // Calculate the closest intersection of the ray with the triangle
    // Hints:
    // - Use the Möller-Trumbore algorithm or plane intersection
    // - Check if the intersection lies within the triangle using barycentric coordinates
    // - Return -1.0 if no valid intersection
    // ----------------------------End of code---------------------------------------------
    return -1.0;
}

vec3 phong_shading(vec3 pos, vec3 normal, vec3 diffuse, vec3 specular, float shininess, vec3 view_dir, Light light) {
    // ----------------------------Insert your code here----------------------------------
    // Calculate the color using the Phong illumination model
    // Hints:
    // - Compute diffuse term
    // - Compute specular term
    // - Multiply by light.color and sum the terms
    // ----------------------------End of code---------------------------------------------
    return vec3(0.0, 0.0, 0.0);
}

void main() {
    vec2 ndc = uv * 2.0 - 1.0;
    ndc.y *= aspect_ratio;
    vec3 ray_dir = normalize(vec3(ndc * fov_tan, -1.0));
    vec3 ray_origin = camera_pos;

    float min_t = -1.0;
    vec3 pos, normal, diffuse, specular;
    float shininess;
    int hit_type = -1;

    for (int i = 0; i < num_spheres; i++) {
        float t = sphere_intersect(ray_origin, ray_dir, spheres[i].pos, spheres[i].radius);
        if (t > 0.0 && (min_t < 0.0 || t < min_t)) {
            min_t = t;
            pos = ray_origin + ray_dir * t;
            normal = normalize(pos - spheres[i].pos);
            diffuse = spheres[i].diffuse;
            specular = spheres[i].specular;
            shininess = spheres[i].shininess;
            hit_type = 0;
        }
    }

    for (int i = 0; i < num_triangles; i++) {
        float t = triangle_intersect(ray_origin, ray_dir, triangles[i]);
        if (t > 0.0 && (min_t < 0.0 || t < min_t)) {
            min_t = t;
            pos = ray_origin + ray_dir * t;
            vec3 b = barycentric(pos, triangles[i].v0, triangles[i].v1, triangles[i].v2);
            normal = normalize(triangles[i].n0 * b.x + triangles[i].n1 * b.y + triangles[i].n2 * b.z);
            diffuse = triangles[i].diffuse0 * b.x + triangles[i].diffuse1 * b.y + triangles[i].diffuse2 * b.z;
            specular = triangles[i].specular0 * b.x + triangles[i].specular1 * b.y + triangles[i].specular2 * b.z;
            shininess = triangles[i].shininess0 * b.x + triangles[i].shininess1 * b.y + triangles[i].shininess2 * b.z;
            hit_type = 1;
        }
    }

    if (min_t < 0.0) {
        FragColor = vec4(BACKGROUND_COLOR, 1.0);
        return;
    }

    vec3 color = ambient_light.color;
    vec3 view_dir = normalize(ray_origin - pos);

    for (int i = 0; i < num_lights; i++) {
        vec3 shadow_dir = normalize(lights[i].pos - pos);
        vec3 shadow_origin = pos + shadow_dir * EPS;
        bool in_shadow = false;

        for (int j = 0; j < num_spheres && !in_shadow; j++) {
            float t = sphere_intersect(shadow_origin, shadow_dir, spheres[j].pos, spheres[j].radius);
            if (t > 0.0 && t < length(lights[i].pos - pos)) in_shadow = true;
        }
        for (int j = 0; j < num_triangles && !in_shadow; j++) {
            float t = triangle_intersect(shadow_origin, shadow_dir, triangles[j]);
            if (t > 0.0 && t < length(lights[i].pos - pos)) in_shadow = true;
        }

        if (!in_shadow) {
            color += phong_shading(pos, normal, diffuse, specular, shininess, view_dir, lights[i]);
        }
    }

    FragColor = vec4(clamp(color, 0.0, 1.0), 1.0);
}