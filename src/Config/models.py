from Config.dependencies import logging

# Carga del modelo de whisper
def load_whisper_model(model_type: str):
    from Config.dependencies import whisper
    logging.info('Cargando modelo de whisper...')
    return whisper.load_model(model_type)

# Carga el modelo con Llama.Cpp
def load_llama_cpp_model(llama_cpp_model_path, model_name, llama_cpp_max_context_tokens):
    from llama_cpp import Llama
    logging.info('Cargando modelo ' + model_name + ' ...')
    return Llama(model_path=llama_cpp_model_path + model_name, n_ctx = llama_cpp_max_context_tokens)
