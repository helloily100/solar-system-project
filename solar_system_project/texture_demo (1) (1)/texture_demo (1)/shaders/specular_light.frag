#version 330
in vec3 Normal;
in vec2 TexCoord;
in vec3 FragPos;

// This is the proper way to set the color of the fragment, NOT using gl_FragColor.
layout (location=0) out vec4 FragColor;

uniform sampler2D ourTexture;
// Lighting parameters for ambient light, and a single point light w/ no attenuation.
uniform vec3 ambientColor;
uniform vec3 pointPosition;
uniform vec3 pointColor;

uniform vec3 cameraPosition;


void main() {

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(pointPosition - FragPos);  
    float cosineLight = max(dot(norm, lightDir), 0.0);

    //view reflection and specular reflection
    vec3 viewDirection = normalize(cameraPosition - FragPos);

    vec3 reflectDirection = reflect(-lightDir, norm);
    float specular = pow(max(dot(viewDirection, reflectDirection), 0.0), 32.0);

    // Compute the ambient and diffuse components.
    vec3 ambient = ambientColor;
    vec3 diffuse = cosineLight * pointColor;

    vec3 specularColor = vec3(1, 1, 1);

    // Assemble the final fragment color.
    FragColor = vec4((diffuse + ambient) * texture(ourTexture, TexCoord).rgb + specular * specularColor, 1);




}
