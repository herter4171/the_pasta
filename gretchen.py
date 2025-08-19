import threading
from colorama import Fore, Style
from gpiozero import LED
from os.path import basename
import openwakeword
import random

from chatgpt import ChatGPT
from ear import TheEar
from the_voice import TheVoice
from print_wrapper import PrintWrapper
from the_head import TheHead

class Gretchen(TheHead):
    @staticmethod
    def get_sound_effect_path():
        return "beep5.wav"
    
    @property
    def _reply_options(self):
        return [
            "Child, what did you just say to me?",
            "Excuse me?",
            "You couldn't speak up to save your life.",
            "Say what now?",
            "I didn't catch that.",
            "Speak into the microphone or at least towards it.",
            "What's all that racket?"
        ]
    
    @property
    def _voice_name(self):
        return 'af_bella'
    
    @property
    def llm_model(self):
        return "gpt-oss:20b"

    @property
    def sys_prompt_path(self):
        return f"{Gretchen._prompts_dir}/prompt_gretchen.txt"