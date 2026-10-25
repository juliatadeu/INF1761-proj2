#version 410 core

in vec3 surfacePosition;
in vec2 surfaceUV;
in mat3 tangentBasis;

uniform vec4 lpos;
uniform vec4 lamb;
uniform vec4 ldif;
uniform vec4 lspe;

uniform vec4 mamb;
uniform vec4 mdif;
uniform vec4 mspe;
uniform float mshi;
uniform float mopacity;

uniform vec4 cpos;

uniform sampler2D decal;
uniform sampler2D normalMap;

out vec4 FragColor;

void main()
{
    vec3 mappedNormal = texture(normalMap, surfaceUV).rgb * 2.0 - 1.0;
    vec3 N = normalize(tangentBasis * mappedNormal);

    vec3 L = (lpos.w == 0.0)
        ? normalize(lpos.xyz)
        : normalize(lpos.xyz - surfacePosition);
    vec3 V = normalize(cpos.xyz - surfacePosition);
    vec3 H = normalize(L + V);

    vec4 ambient = lamb * mamb;
    float ndl = max(dot(N, L), 0.0);
    vec4 diffuse = ldif * mdif * ndl;

    float ndh = max(dot(N, H), 0.0);
    vec4 specular = lspe * mspe * pow(ndh, mshi);

    vec4 albedo = texture(decal, surfaceUV);
    FragColor = (ambient + diffuse) * albedo + specular;
    FragColor.a = mopacity;
}
