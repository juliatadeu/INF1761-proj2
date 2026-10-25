#version 410

layout (location = 0) in vec3 vertexPosition;

uniform mat4 Mvp;

out vec3 skyDirection;
out vec4 skyTint;

void main()
{
    skyDirection = vertexPosition;
    skyTint = vec4(0.52, 0.45, 0.64, 1.0);

    gl_Position = Mvp * vec4(vertexPosition, 1.0);
}
