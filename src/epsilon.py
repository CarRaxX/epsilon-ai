# Imports
from Config.dependencies import logging
# Config
from Config.configuration import *
from Config.models import *
# .py Methods
from VoiceToText.transcript import *
from ChatText.chat import *
from LanguageModel.validate_request import *
from LanguageModel.language_model import *
from Dba.DBProcess import *

# Opción de chat de texto


def text_chat_option() -> None:
    # Realizamos la configuración inicial
    logging.info('Configurando ' + global_config['ai_interpreter'] + ' para el chat por texto...')
    # BBDD
    init_db()
    # Seleccionamos el modelo a usar y lo cargamos en memoria
    llm_model = options_models_menu()
    # Inicializamos la configuración...
    # Cola de petición por Texto
    request_text_queue = global_config['request_text_queue']
    # Cola de respuesta por Texto
    response_text_queue = global_config['response_text_queue']
    # Cola de respuesta por Audio
    response_audio_queue = global_config['response_audio_queue']
    logging.info('Se va a hablar con ' + global_config['ai_interpreter'] + ' vía chat de texto')
    # Mientras no se cumpla la condicion de salida seguimos en el bucle
    while not global_config['is_exit_request']:
        # 1.Obtenemos el texto de entrada
        get_input_text(request_text_queue)
        # 2.Comprobamos la petición
        # Comprobamos la petición y Cambiamos los estados
        check_request(
            request_text_queue, config_check['keywords'], config_check['stop_keywords'])
        # Si se da una petición, se formula al modelo de lenguaje
        if global_config['is_epsilon_request']:
            # 4.Formulamos la petición al Modelo de Lenguaje y obtenemos su respuesta
            llama_cpp_model_generate_text(request_text_queue, response_text_queue, llm_model, config_llama_cpp_generate_text['llama_cpp_epsilon_personality'], config_llama_cpp_generate_text['llama_cpp_epsilon_init_chat'], config_llama_cpp_generate_text['llama_cpp_epsilon_ctx_days'], config_llama_cpp_generate_text['llama_cpp_max_predict_tokens'],
                                            config_llama_cpp_generate_text['llama_cpp_temperature'], config_llama_cpp_generate_text['llama_cpp_top_p'], config_llama_cpp_generate_text['llama_cpp_stop'], 
                                            config_llama_cpp_generate_text['llama_cpp_repeat_penalty'], config_llama_cpp_generate_text['llama_cpp_top_k'])
            
            
    exit_option()

# Opción de chat de voz


def voice_chat_option() -> None:
    # Realizamos la configuración inicial
    logging.info('Configurando ' + global_config['ai_interpreter'] + ' para el chat por voz...')
    # Inicializamos la configuración...
    # Cola de petición por Audio
    request_audio_queue = global_config['request_audio_queue']
    # Cola de petición por Texto
    request_text_queue = global_config['request_text_queue']
    # Cola de respuesta por Texto
    response_text_queue = global_config['response_text_queue']
    # Cola de respuesta por Audio
    response_audio_queue = global_config['response_audio_queue']
    # BBDD
    init_db()
    # Seleccionamos el modelo a usar y lo cargamos en memoria
    llm_model = options_models_menu()
    # Cargamos el modelo de Wishper para escuchar
    whisper_model = load_whisper_model(
        config_transcribe['type_model'])  # Modelo de Wishper
    logging.info('Se va a hablar con ' + global_config['ai_interpreter'] + ' vía chat de voz')
    # Mientras no se cumpla la condicion de salida seguimos en el bucle
    while not global_config['is_exit_request']:
        # 1.Grabamos
        # Obtenemos la cola de petición de texto
        record_audio(request_audio_queue, config_record['energy'], config_record['pause_threshold'],
                     config_record['dynamic_energy'], config_record['save_file'], config_record['file_path'], config_record['file_name'])
        # 2.Transcribimos
        # Obtenemos la cola de petición de audio
        transcribe_audio_queue(request_audio_queue, request_text_queue,
                               global_config['request_text_queue'], whisper_model, config_transcribe['language'])
        # 3.Comprobamos la petición
        # Comprobamos la petición y Cambiamos los estados
        check_request(
            request_text_queue, config_check['keywords'], config_check['stop_keywords'])
        # Si se da una petición, se formula al modelo de lenguaje
        if global_config['is_epsilon_request']:
            # 4.Formulamos la petición al Modelo de Lenguaje y obtenemos su respuesta
            llama_cpp_model_generate_text(request_text_queue, response_text_queue, llm_model, config_llama_cpp_generate_text['llama_cpp_epsilon_personality'], config_llama_cpp_generate_text['llama_cpp_epsilon_init_chat'], config_llama_cpp_generate_text['llama_cpp_epsilon_ctx_days'], config_llama_cpp_generate_text['llama_cpp_max_predict_tokens'],
                                            config_llama_cpp_generate_text['llama_cpp_temperature'], config_llama_cpp_generate_text['llama_cpp_top_p'], config_llama_cpp_generate_text['llama_cpp_stop'], 
                                            config_llama_cpp_generate_text['llama_cpp_repeat_penalty'], config_llama_cpp_generate_text['llama_cpp_top_k'])
            
    exit_option()

# Opción de chat de salir


def exit_option() -> None:
    exit_db()
    logging.info('' + global_config['ai_interpreter'] + ' se va a dormir.')
    exit()


def init_config() -> None:
    logging.info('Configurando ')
    

# Opción de las formas de hablar con epsilon
# Opciones asignadas a números
menu_options = {
    "1": text_chat_option,
    "2": voice_chat_option,
    "3": exit_option
}

# Menú de opciones


def options_main_menu() -> None:
    while True:
        logging.info("Menú de opciones para hablar con " + global_config['ai_interpreter'] + ":")
        logging.info("1. Chat por texto")
        logging.info("2. Chat por voz")
        logging.info("3. Salir")
        # Opción del usuario
        option = input("Inserte la opción a ejecutar: ")
        # Realizamos la acción en función de las acciones asignadas a los numeros
        action = menu_options.get(option)
        if action:
            # Ejecutamos la opción seleccionada
            action()
        else:
            logging.info(
                "Opción incorrecta, seleccione una con las teclas 1, 2 o 3.")

# Menú de opciones


def options_models_menu() -> Llama:
    model_directory = config_llama_cpp_generate_text['llama_cpp_model_directory_path']
    model_files = os.listdir(model_directory)
    
    while True:
        logging.info("Menú de Modelos de Lenguaje:")
        
        for i, model_file in enumerate(model_files, start=1):
            logging.info(f"{i}. {model_file}")
        
        logging.info(f"{len(model_files) + 1}. Atrás")
        
        # Opción del usuario
        option = input("Inserte el modelo a ejecutar: ")
        
        if option.isdigit() and int(option) in range(1, len(model_files) + 2):
            # Ejecutamos la opción seleccionada
            if option == str(len(model_files) + 1):
                # Opción "Atrás"
                options_main_menu()
            else:
                selected_file = model_files[int(option) - 1]
                llm_model = load_llama_cpp_model(config_llama_cpp_generate_text['llama_cpp_model_directory_path'], selected_file, config_llama_cpp_generate_text['llama_cpp_max_context_tokens'])
                return llm_model
        else:
            logging.info("Opción incorrecta, seleccione una opción válida.")

# Main
if __name__ == '__main__':
    logging.info("¡" + global_config['ai_interpreter'] + " está despierta!")
    options_main_menu()
