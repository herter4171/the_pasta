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
from base_has_logs import BaseHasLogs

class TheHead(BaseHasLogs):
    @staticmethod
    def get_sound_effect_path():
        return "blip.wav"
    
    @staticmethod
    def blink_led(stop_event, sleep_sec=0.1):
        led = LED(23) # Pin 17

        while not stop_event.is_set():
            led.on()
            stop_event.wait(sleep_sec)
            led.off()
            stop_event.wait(sleep_sec)
    
    @property
    def _reply_options(self):
        return [
            "What did you just say to me?",
            "I am NOT your butler.",
            "Don't take that tone with me.",
            "Do you talk to your mother with that mouth?",
            "Hey, I'm sorry, I didn't catch that.",
            "Speak up, please.",
            "I'm sorry, you mumbled.",
            "Get your shit together."
        ]
    
    @property
    def _voice_name(self):
        return 'am_adam'
    
    @property
    def llm_model(self):
        return "mistral-small3.1:24b"

    @property
    def sys_prompt_path(self):
        return "prompt.txt"

    def __init__(self, model_name):
        # Show processing
        self._led_stop = threading.Event()
        self._led_thread = threading.Thread(target=TheHead.blink_led, args=(self._led_stop,))
        self._led_thread.start()
    
    def chat(self, msg: str, gpt: ChatGPT):
        pw = PrintWrapper()

        if msg:
            # Start out assuming no printing
            reply = gpt.send_prompt(msg, self.llm_model)
            to_say, to_print = [reply, '']
            print_thread = None

            if pw.print_tag in reply:
                # Split by print tag
                to_say, to_print = reply.split(pw.print_tag)
            
            if to_print:
                # Print in separate thread for efficiency
                print_thread = threading.Thread(
                    target=pw.print,
                    args=(to_print,)
                )
                print_thread.start()
            
            if print_thread:
                print_thread.join()
        else:
            to_say = self._get_non_reply()

        # Verbalize the spoken portion
        voice = TheVoice(self._voice_name)
        voice.speak(to_say)

        # Stop blinking light
        self._led_stop.set()
        self._led_thread.join()
        
    def _get_non_reply(self):
        """"Returns a random reply from given list."""
        opts = self._reply_options
        reply_ind = random.randint(0, len(opts) - 1)

        return opts[reply_ind]