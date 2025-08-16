import threading

from chatgpt import ChatGPT
from ear import TheEar
from the_voice import TheVoice
from print_wrapper import PrintWrapper

gpt = ChatGPT("sk-16d7cf8ffea74d25bf1ced61c80563d3")
pw = PrintWrapper()

while True:
    ear = TheEar("hey_percy.tflite")
    msg = ear.listen()

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

        TheVoice().speak(to_say)
        
        if thread:
            thread.join()
