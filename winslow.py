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

class Winslow(TheHead):
    @staticmethod
    def get_sound_effect_path():
        return "snowball.wav"
    
    @property
    def _reply_options(self):
        return [
            "You wot, mate?",
            "Speak up, you sad wanker.",
            "I am not your butler.",
            "Oy, don't speak of me mum that way."
        ]
    
    @property
    def _voice_name(self):
        return 'bm_lewis'
    
    @property
    def llm_model(self):
        return "gpt-oss:20b"

    @property
    def sys_prompt_path(self):
        return f"{Winslow._prompts_dir}/prompt_winslow.txt"
