import threading
from colorama import Fore, Style
from gpiozero import LED
from glob import glob
import openwakeword
import random

from chatgpt import ChatGPT
from ear import TheEar
from the_voice import TheVoice
from the_head import TheHead
from gretchen import Gretchen
from winslow import Winslow
from print_wrapper import PrintWrapper

def print_branding():
    f = open('branding.txt')
    lines = f.readlines()
    f.close()
    print(Fore.CYAN + ''.join(lines) + Style.RESET_ALL, end='')

# One-time download of all pre-trained models (or only select models)
openwakeword.utils.download_models()

# TODO: Not in repo if shared
open_web_ui_api_key = "sk-16d7cf8ffea74d25bf1ced61c80563d3"

mdl_head_map = {
    "hey_percy": TheHead,
    "hey_gretchen": Gretchen,
    "hey_winslow": Winslow
}

mdl_beep_map = {k: f"listen_beeps/{HeadType.get_sound_effect_path()}" for k,HeadType in mdl_head_map.items()}

printed_branding = False

while True:
    ear = TheEar(glob("wake_word_models/*.tflite"), mdl_beep_map)

    if not printed_branding:
        print_branding()
        printed_branding = True

    mdl, msg = ear.listen()
    head = mdl_head_map[mdl](mdl)
    gpt = ChatGPT(mdl, open_web_ui_api_key, head.sys_prompt_path)
    head.chat(msg, gpt)
