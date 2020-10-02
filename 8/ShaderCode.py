def getFragmentShader():
    return """
                                    #version 330
                                    in vec3 newColor;
                                    in vec3 Normal;
                                    in vec3 Position;
                                    in vec2 Tex_cord;
                                    
                                    out vec4 outColor;
                                    
                                    
                                    //Light_uniform
                                    uniform vec3 light_ambient = vec3(0.5f, 0.5f, 0.5f);
                                    uniform vec3 model_ambient = vec3(0.3f, 0.3f, 0.3f);
                                    uniform vec3 model_diffuse = vec3(0.6f, 0.6f, 0.6f);
                                    uniform vec3 light_diffuse = vec3(0.4f, 0.4f, 0.4f);
                                    uniform vec3 light_position = vec3(20f, 20f, 0f);
                                    uniform bool light_on = false;
                                    
                                    //View
                                    vec3 v = vec3(0f, 0f, -1f);
                                    
                                    //Texture_uniform
                                    uniform bool texture_on = false; 
                                    uniform sampler2D texture;
                                    
                                    //light
                                    vec3 ambient_intensivity = model_ambient * light_ambient;
                                    
                                    //
                                    vec3 L = normalize(light_position - Position);
                                    vec3 diffuse_intensivity = model_diffuse * max(dot(L, Normal), 0f) * light_diffuse;
                                    //
                                    
                                    vec3 light_specular = vec3(1f, 1f, 1f);
                                    float shiness = 0.2f;
                                    vec3 R = normalize(-L + 2 * max(dot(L, Normal), 0f) * Normal);
                                    float exponent = 32f;
                                    vec3 specular_intensivity = light_specular * shiness * pow( max(dot(R, v), 0f), exponent);
                                    
                                    vec3 light_res = ambient_intensivity  + specular_intensivity + diffuse_intensivity;
                                    
                                    uniform float epsilon = 1f;
                                    uniform float fov = radians(30f);
                                    
                                    void main()
                                    {            
                                        if (!light_on){
                                            light_res = vec3(1f, 1f, 1f);
                                        }
                                        if (texture_on){
                                            outColor =  vec4(newColor * light_res * pow(cos(fov), epsilon), 1f) * texture2D(texture, Tex_cord);
                                        }
                                        else{
                                            outColor =  vec4(newColor * light_res * pow(cos(fov), epsilon), 1f);
                                        }
                                    }
            """


def getVertexShader():
    return """
                                    #version 330
                                    in layout(location = 0) vec3 position;
                                    in layout(location = 1) vec3 color;
                                    in layout(location = 2) vec3 normal;
                                    in layout(location = 3) vec2 tex_cord;
                                                                                 
                                    out vec3 newColor;
                                    out vec3 Normal;
                                    out vec3 Position;
                                    out vec2 Tex_cord;
                                    
                                    uniform float Scale = 1;
                                    uniform float rotateAngle_x = 0;
                                    uniform float rotateAngle_y = 90;
                                    uniform float rotateAngle_z = 0;
                                    uniform float Translate_x = 0;
                                    uniform float Translate_y = 0;
                                    uniform float Translate_z = 0;
                                    
                                    //Projection and ViewPort
                                    uniform mat4 Projection = mat4(
                                        1, 0, 0, 0,
                                        0, 1, 0, 0,
                                        0, 0, 1, 0,
                                        0, 0, 0, 1
                                    );
                                    
                                    
                                    void main()
                                    {  
                                        mat3 rot_x = mat3(  
                                            1.0, 0.0, 0.0,
                                            0.0, cos(rotateAngle_x), -sin(rotateAngle_x),
                                            0.0, sin(rotateAngle_x), cos(rotateAngle_x)
                                        );
                                        
                                        mat3 rot_y = mat3(
                                            cos(rotateAngle_y), 0.0, sin(rotateAngle_y),
                                            0.0, 1.0, 0.0,
                                            -sin(rotateAngle_y), 0.0, cos(rotateAngle_y)
                                        );
                                        
                                        mat3 rot_z = mat3(
                                            cos(rotateAngle_z), -sin(rotateAngle_z), 0.0, 
                                            sin(rotateAngle_z), cos(rotateAngle_z), 0.0, 
                                            0.0, 0.0, 1.0
                                        );
                                        
                                        vec3 translate_vec = vec3(Translate_x, Translate_y, Translate_z);
                                        
                                        vec3 pos = vec3(((((position * Scale) * rot_x) * rot_y) * rot_z) + translate_vec);
                                        vec4 position = vec4(pos, 1f) * Projection;
                                        
                                        gl_Position = position;
                                        
                                        newColor = color;
                                        
                                        Normal = normalize((((normal * rot_x) * rot_y) * rot_z));
                                        
                                        Position = pos;
                                        
                                        Tex_cord = tex_cord;
                                    }
            """


class ShaderCode:
    def __init__(self):
        self.vertex_shader = getVertexShader()
        self.fragment_shader = getFragmentShader()
