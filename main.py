import threading
from colorama import Fore, Style
from gpiozero import LED

from chatgpt import ChatGPT
from ear import TheEar
from the_voice import TheVoice
from print_wrapper import PrintWrapper

gpt = ChatGPT("sk-16d7cf8ffea74d25bf1ced61c80563d3")
pw = PrintWrapper()


def print_branding():
    f = open('branding.txt')
    lines = f.readlines()
    f.close()

    print(Fore.CYAN + ''.join(lines) + Style.RESET_ALL, end='')

def blink_led(stop_event, sleep_sec=0.1):
    led = LED(23)

    while not stop_event.is_set():
        led.on()
        stop_event.wait(sleep_sec)
        led.off()
        stop_event.wait(sleep_sec)

printed_branding = False

while True:
    ear = TheEar("hey_percy.tflite")

    if not printed_branding:
        print_branding()
        printed_branding = True

    voice = TheVoice()
    msg = ear.listen(voice)

    # Show we're processing
    led_stop = threading.Event()
    led_thread = threading.Thread(target=blink_led, args=(led_stop,))
    led_thread.start()

    if msg:
        reply = gpt.send_prompt(msg)
        to_say, to_print = [reply, '']
        thread = None

        if pw.print_tag in reply:
            to_say, to_print = reply.split(pw.print_tag)
        
        if to_print:
            thread = threading.Thread(
                target=pw.print,
                args=(to_print,)
            )
            thread.start()

        voice.speak(to_say)
        
        if thread:
            thread.join()
    else:
        voice.speak("Speak up, please.")
    
    led_stop.set()
    led_thread.join()
