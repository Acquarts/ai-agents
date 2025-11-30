from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from agent import Agent

load_dotenv()

client = OpenAI()
agent = Agent()

while True:
    user_input = input("Tú: ").strip()
    
    # VALIDACIONES DE ENTRADA DEL USUARIO
    if not user_input:
        continue
    if user_input.lower() in {"salir", "exit", "quit", "Taluego!"}:
        print("Asistente: ¡Hasta luego!")
        break
    
    # AGREGAR NUESTRO MENSAJE AL HISTORIAL
    agent.messages.append({"role": "user", "content": user_input})
    
    while True:
        response = client.responses.create(
            model="gpt-5-nano",
            input=agent.messages,
            tools=agent.tools
        )  
    
        called_tool = agent.process_response(response)
        # SI NO HUBO LLAMADA A HERRAMIENTA, MOSTRAR RESPUESTA AL USUARIO
        if not called_tool:
            break