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
        to_say = ''

        if pw.print_tag in reply:
            to_say, to_print = reply.split(pw.print_tag)

        TheVoice().speak(to_say)
        pw.print(to_print)
