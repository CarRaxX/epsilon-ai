# Imports
from Config.dependencies import Queue, os, logging
from Config.private_config import *

# Log
# Configuracion de Logs
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# All
global_config = {
    'human_interpreter': human_interpreter,
    'request_audio_queue': Queue(),  # Cola de petición por Audio
    'request_text_queue': Queue(),  # Cola de petición por Texto
    'response_audio_queue': Queue(),  # Cola de respuesta por Audio
    'response_text_queue': Queue(),  # Cola de respuesta por Texto
    'is_epsilon_request': False,  # Define si se ha realizado una consulta al ML
    'is_exit_request': False  # Define si se ha realizado una consulta de parada
}

# Configuración de Datos iniciales
# VoiceToTextModel
# transcript.py
# execute_record_audio
config_record = {
    'energy': 300,  # Parametro que determina la energia que el microfono detecta
    # Segundos que deben pasar en silencio hasta que pare la grabación pare
    'pause_threshold': 0.8,
    'dynamic_energy': False,  # Activar o desactivar la energía dinamica del mic
    # Indica si se guardan ficheros de grabación (Por defecto False)
    'save_file': False,
    # Indica la ruta de los ficheros (Por defecto: ./Audios/)
    'file_path': os.path.join(os.getcwd(), "Audios"),
    # Indica el nombre de los ficheros ((Por defecto: human_to_epsilon_record_%Y-%m-%d_%H-%M-%S.wav))
    'file_name': 'human_to_epsilon_record'
}

# execute_transcribe
config_transcribe = {
    # Tipo de modelo de wishper a usar opciones: ["tiny", "base", "small", "medium", "large"]
    'type_model': 'small',
    'language': 'es'  # Idioma del modelo es = spanish
}

# execute_check
config_check = {
    'keywords': ['epsi'],  # Palabra clave para que inicie la grabación
    # Palabras clave que finalizan el proceso
    'stop_keywords': ['adios', 'chao', 'chau', 'me voy', 'hasta mañana', 'buenas noches', 'hasta luego']
}

# LanguageModel
# language_model.py
# open_ai_model_generate_text
config_open_ai_generate_text = {
    'open_ai_key': open_ai_api_key,
    'open_ai_model': 'text-davinci-003',
    'open_ai_model_personality': open_ai_model_personality,
    'open_ai_model_temperature': 0.8,
    'open_ai_model_max_tokens': 128,
    'open_ai_model_top_p': 1,
    'open_ai_model_frequency_penalty': 1,
    'open_ai_model_presence_penalty': 1
}

config_llama_cpp_generate_text = {
    'llama_cpp_model_path': llama_cpp_model_path,
    'llama_cpp_max_ctx_tokens': 512,
    'llama_cpp_instruccion': llama_cpp_instruccion,
    'llama_cpp_chat_example': llama_cpp_chat_example,
    'llama_cpp_stop': llama_cpp_stop,
    'llama_cpp_max_predict_tokens': 125,
    'llama_cpp_temperature': 0.5,
    'llama_cpp_top_p': 1,
    'llama_cpp_repeat_penalty': 1.1,
    'llama_cpp_top_k': 50
}