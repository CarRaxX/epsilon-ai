# Imports
from Config.dependencies import logging, os, Queue, whisper, torch, datetime
from Config.dependencies import numpy as np, speech_recognition as sr, soundfile as sf
from Config.dependencies import time
from Config.configuration import global_config

# Función para grabar audio hasta que se detecte silencio


def record_audio(request_audio_queue: Queue, energy: int = 300, pause_threshold: float = 0.8, dynamic_energy: bool = False, save_file: bool = False, file_path: str = os.path.join(os.getcwd(), "Audios"), file_name: str = 'human_to_epsilon_record') -> None:
    # Configuramos los parametros de grabacion
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause_threshold
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        while True:
            logging.info("" + global_config['ai_interpreter'] + " está escuchando...")
            # Obtenemos el audio del micrófono
            audio = r.listen(source)
            # Procesamos el audio
            torch_audio = torch.from_numpy(np.frombuffer(
                audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            # Audio obtenido
            audio_data = torch_audio

            # Guardar la grabación en archivo si se especifica
            if save_file and file_path and file_name:
                save_audio_file(file_path, file_name, audio_data)

            logging.info("" + global_config['ai_interpreter'] + " ha escuchado")
            # Introducimos la petición en la cola de audio
            request_audio_queue.put(audio_data)
            # Dejamos de grabar
            break

# Función que transcribe las colas de audio a texto


def transcribe_audio_queue(request_audio_queue: Queue, request_text_queue: Queue, whisper_model: whisper.load_model, language: str = 'es') -> None:
    # Obtenemos el siguiente fragmento de audio de la cola
    logging.info('Transcribiendo audio...')
    audio_data = request_audio_queue.get()
    # Convertimos el fragmento de audio a texto utilizando Whisper
    verbose_result = whisper_model.transcribe(
        audio_data, language=language)
    # Obtenemos del verbose el texto transcrito
    transcript_result = verbose_result['text']
    # Introducimos la petición en la cola de texto
    request_text_queue.put(transcript_result)

# Función que guarda el audio grabado


def save_audio_file(file_path: str, file_name: str, audio_data: torch) -> None:
    logging.info("Se va a guardar la grabación de audio")
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name_with_date = f"{file_name}_{now}.wav"
    file_full_path = os.path.join(
        file_path, file_name_with_date)
    sf.write(file_full_path, audio_data, 44100)
    logging.info(f"Grabación guardada en {file_full_path}")
