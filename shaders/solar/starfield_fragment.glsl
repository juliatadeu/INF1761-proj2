#version 410

in vec3 skyDirection;
in vec4 skyTint;

uniform samplerCube skybox;

out vec4 FragColor;

void main()
{
    FragColor = skyTint * texture(skybox, skyDirection);
}
