import pyaudio
import numpy as np
from openwakeword.model import Model
from time import sleep
import audioop
from pydub import AudioSegment
from pydub.playback import play
import logging
import sys
import speech_recognition as sr
from colorama import Fore, Style

from base_has_logs import BaseHasLogs
from the_voice import TheVoice

class TheEar(BaseHasLogs):
    def __init__(self, wakeword_model_paths: list, mdl_beep_map: dict):
        super().__init__()
        self._wakeword_model_paths = wakeword_model_paths
        self._mdl_beep_map = mdl_beep_map

        self._audio = pyaudio.PyAudio()
        self._chunk_size = 1280
        self._format = pyaudio.paInt16
        self._rate = 16000

        self._mic_stream = self._audio.open(
            format=self._format, 
            channels=1, 
            rate=self._rate, 
            input=True, 
            frames_per_buffer=self._chunk_size
        )

        self._model = Model(wakeword_models=self._wakeword_model_paths)

    def _play_blip(self, file_path="blip.wav"):
        self._logger.info(f"Playing {file_path}")
        sound = AudioSegment.from_wav(file_path)
        play(sound)

    def listen(self):
        mdl = self._await_invoke()
        file_path = self._mdl_beep_map[mdl]
        self._play_blip(file_path)
        recorded_frames = self._capture_audio()
        msg = self._transcribe_audio(mdl, recorded_frames)

        return mdl, msg

    def _await_invoke(self):
        self._logger.info("Waiting for trigger phrase")
        detected = False
        detected_model = None

        while not detected:
            self._audio = np.frombuffer(self._mic_stream.read(self._chunk_size), dtype=np.int16)
            prediction = self._model.predict(self._audio)

            for mdl in self._model.prediction_buffer.keys():
                # Add scores in formatted table
                scores = list(self._model.prediction_buffer[mdl])

                if scores[-1] >= 0.4:
                    msg = f"Trigger phrase (Model {mdl}, Score {scores[-1]:.2f})"
                    self._logger.info(msg)
                    detected_model = mdl
                    detected = True
                    break
        
        return detected_model
    
    def _capture_audio(self, silent_threshold=1000, silent_sec_cuttof=1.5) -> list:
        recorded_frames = []
        is_speaking = True
        silent_chunks = 0

        num_silent_chunks_required = int(silent_sec_cuttof * self._rate / self._chunk_size)
        self._logger.info("Listening to prompt")

        while is_speaking:
            # Get recorded frames and current volume
            data = self._mic_stream.read(self._chunk_size)
            recorded_frames.append(data)
            rms = audioop.rms(data, 2)

            if rms < silent_threshold:
                silent_chunks += 1

                if silent_chunks >= num_silent_chunks_required:
                    self._logger.info("Prompt is finished")
                    is_speaking = False
            else:
                silent_chunks = 0
        
        return recorded_frames

    def _transcribe_audio(self, mdl: str, recorded_frames: list) -> str:
        # Create an AudioData object
        raw_audio_data = b''.join(recorded_frames)
        recognizer = sr.Recognizer()
        audio_data = sr.AudioData(raw_audio_data, self._rate, pyaudio.PyAudio().get_sample_size(self._format))

        text = ''

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            mdl_pretty = Fore.MAGENTA + f"Prompt [{mdl}]:" + Style.RESET_ALL
            self._logger.info(f"{mdl_pretty} {text}")            
        except sr.UnknownValueError:
            self._logger.error("Google Web Speech API could not understand the audio.")
        except Exception as e:
            self._logger.error(f"Could not request results from Google Web Speech API; {e}")
        finally:
            return text
        