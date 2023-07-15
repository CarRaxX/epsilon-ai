# Carga del modelo de whisper
def load_whisper_model(model_type: str):
    from Config.dependencies import whisper
    return whisper.load_model(model_type)

# Carga el modelo de vicunia
def load_vicunia_model(llama_cpp_model_path):
    from llama_cpp import Llama
    return Llama(model_path=llama_cpp_model_path)

# Carga el modelo de vicunia por comandos
def load_vicunia_model_cmd(llama_cpp_model_path):
    import subprocess
    return 1