from chatgpt import ChatGPT
from ear import TheEar
from the_voice import TheVoice

gpt = ChatGPT("sk-16d7cf8ffea74d25bf1ced61c80563d3")

while True:
    ear = TheEar("hey_percy.tflite")
    msg = ear.listen()

    if msg:
        reply = gpt.send_prompt(msg)
        TheVoice().speak(reply)