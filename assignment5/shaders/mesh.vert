#version 330 core
in vec3 position;
in vec3 normal;

out vec3 fragPos;
flat out vec3 flatNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    vec4 worldPos = model * vec4(position, 1.0);
    fragPos = vec3(view * worldPos);
    flatNormal = normalize(mat3(transpose(inverse(view * model))) * normal);
    gl_Position = projection * view * worldPos;
}