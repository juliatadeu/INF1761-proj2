#version 410 core

in vec3 surfacePosition;
in vec3 surfaceNormal;
in vec2 surfaceUV;

uniform sampler2D decal;

out vec4 FragColor;

void main()
{
    vec3 base = texture(decal, surfaceUV).rgb;
    vec3 warmTint = vec3(1.0, 0.87, 0.64);

    FragColor = vec4(base * warmTint, 1.0);
}
