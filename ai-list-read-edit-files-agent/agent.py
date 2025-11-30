import os
import json

class Agent:
    def __init__(self):
        self.setup_tools()
        self.messages = [
    {"role": "system", "content": "Eres un asistente útil que habla español, eres muy amable y conciso en tus respuestas."},
]
        
        
    def setup_tools(self):
        self.tools = [
            {
                "type": "function",
                "name": "list_files_in_dir",
                "description": "Lista los archivos que existen en un directorio dado (por defecto es el directorio actual)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "Directorio para listar (opcional). Por defecto es el directorio actual"
                        }
                    },
                    "required": []
                }
            },
            {
                "type": "function",
                "name": "read_file",
                "description": "Lee el contenido de un archivo en una ruta especificada",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "La ruta del archivo a leer"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "type": "function",
                "name": "edit_file",
                "description": "Edita el contenido de un archivo reemplazando previous_text por new_text. Crea el archivo si no existe.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "La ruta del archivo a editar"
                        },
                        "previous_text": {
                            "type": "string",
                            "description": "El texto que se va a buscar para reemplazar (puede ser vacío para archivos nuevos)"
                        },
                        "new_text": {
                            "type": "string",
                            "description": "El texto que reemplazará a previous_text (o el texto para un archivo nuevo)"
                        }
                    },
                    "required": ["path", "new_text"]
                }
            }
        ]
        
# DEFINICION DE LAS TOOLS (FUNCIONES)
# TOOL: LISTAR ARCHIVOS EN DIRECTORIO
    def list_files_in_dir(self, directory="."):
        print('📞 Herramienta llamada: list_files_in_dir')
        try:
            files = os.listdir(directory)
            return {'files': files}
        except Exception as e:
            return f"Error al listar archivos: {str(e)}"
        
        
# TOOL: LEER ARCHIVOS
    def read_file(self, path):
        print('📞 Herramienta llamada: read_file')
        try:
            with open(path, encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            error_message = f"Error al leer archivo: {path}"
            print(error_message)
            return error_message
        
# TOOL: EDITAR ARCHIVOS
    def edit_file(self, path, new_text, previous_text):
        print('📞 Herramienta llamada: edit_file')
        try:
            existed = os.path.exists(path)
            if existed and previous_text:
                content = self.read_file(path)
                
                if previous_text not in content:
                    return f"El texto {previous_text} no coincide con el contenido actual del archivo"
                
                content = content.replace(previous_text, new_text)
                
            else:
                # Crear o sobrescribir con el nuevo texto directamente
                dir_name = os.path.dirname(path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)
                    
                content = new_text
                
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
                
            action = "editado" if existed and previous_text else "creado"
            return f"Archivo {path} {action} exitosamente" 
        except Exception as e:
            error_message = f"Error al editar archivo: {path}"
            print(error_message)
            return error_message                                    
        
        
        
    def process_response(self, response):
        # True = si llama a una funcion.False = no hubo llamada.
        
        # ALMACENAR PARA HISTORIAL
        self.messages += response.output
        
        # PROCESAR LLAMADAS A FUNCIONES
        for output in response.output:
            if output.type == 'function_call':
                function_name = output.name
                arguments = json.loads(output.arguments)
                
                print(f'📞 Llamando a la función: {function_name}')
                print(f'📑 Argumentos: {arguments}')
                
                # Ejecutar la función correspondiente
                if function_name == 'list_files_in_dir':
                    result = self.list_files_in_dir(**arguments)
                elif function_name == 'read_file':
                    result = self.read_file(**arguments)
                elif function_name == 'edit_file':
                    result = self.edit_file(**arguments)
                else:
                    result = f"Función desconocida: {function_name}"

                # AGREGAR A LA MEMORIA LA RESPUESTA DE LLAMADO A FUNCIÓN
                self.messages.append({
                    "type": "function_call_output",
                    "call_id": output.call_id,
                    "output": json.dumps(result) if isinstance(result, dict) else result
                })

                return True  # Indica que se hizo una llamada a función
                
            elif output.type == 'message':
                #print(f'Asistente: {output.content}')
                reply = '\n'.join(part.text for part in output.content)
                print(f'Asistente: {reply}')
                
        return False