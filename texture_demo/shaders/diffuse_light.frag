#version 450
in vec3 Normal;
in vec2 TexCoord;
in vec3 FragPos;
layout (location=0) out vec4 FragColor;

uniform sampler2D ourTexture;
uniform vec3 ambientColor;
uniform vec3 pointPosition;
uniform vec3 pointColor;

void main() {
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(pointPosition - FragPos);  
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * pointColor;

    vec3 ambient = ambientColor;
    FragColor = vec4(diffuse + ambient, 1) * texture(ourTexture, TexCoord);
    
}