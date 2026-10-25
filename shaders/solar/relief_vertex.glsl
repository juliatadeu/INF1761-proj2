#version 410 core

layout (location = 0) in vec3 vertexPosition;
layout (location = 1) in vec3 vertexNormal;
layout (location = 2) in vec3 vertexTangent;
layout (location = 3) in vec2 vertexUV;

uniform mat4 Mvp;
uniform mat4 Mv;
uniform mat4 Mn;

out vec3 surfacePosition;
out vec2 surfaceUV;
out mat3 tangentBasis;

void main()
{
    vec3 normal = normalize((Mn * vec4(vertexNormal, 0.0)).xyz);
    vec3 tangent = normalize((Mn * vec4(vertexTangent, 0.0)).xyz);
    vec3 bitangent = normalize(cross(normal, tangent));

    tangentBasis = mat3(tangent, bitangent, normal);
    surfacePosition = (Mv * vec4(vertexPosition, 1.0)).xyz;
    surfaceUV = vertexUV;

    gl_Position = Mvp * vec4(vertexPosition, 1.0);
}
