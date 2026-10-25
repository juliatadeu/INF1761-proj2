#version 410 core

layout (location = 0) in vec3 vertexPosition;
layout (location = 1) in vec3 vertexNormal;
layout (location = 3) in vec2 vertexUV;

uniform mat4 Mvp;
uniform mat4 Mv;
uniform mat4 Mn;

out vec3 surfacePosition;
out vec3 surfaceNormal;
out vec2 surfaceUV;

void main()
{
    vec4 eyePosition = Mv * vec4(vertexPosition, 1.0);

    surfacePosition = eyePosition.xyz;
    surfaceNormal = normalize((Mn * vec4(vertexNormal, 0.0)).xyz);
    surfaceUV = vertexUV;

    gl_Position = Mvp * vec4(vertexPosition, 1.0);
}
