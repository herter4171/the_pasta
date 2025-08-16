from openai import OpenAI
import time

from base_has_logs import BaseHasLogs
from the_memory import TheMemory


class ChatGPT(BaseHasLogs):

    def __init__(self, api_key: str):
        super().__init__()
        self._client = OpenAI(api_key=api_key, base_url="https://dsui.twr.church/api/v1")
        self._mem = TheMemory()

        if self._mem.is_first_message:
            f = open('prompt.txt')
            sys_prompt = '\n'.join(f.readlines())
            f.close()
            self.send_prompt(sys_prompt, input_role="system")

    def send_prompt(self, prompt: str, input_role="user"):
        self._mem.add_message(input_role, prompt)
        messages = self._mem.get_messages()

        stream = self._client.chat.completions.create(
            model="gpt-oss:20b",
            messages=messages,
            stream=True
        )

        full_reply = ""

        for chunk in stream:
            real_content = chunk.choices[0].delta.content

            if real_content is not None:
                full_reply += real_content
        
        self._logger.info(f"Response: {full_reply}")
        self._mem.add_message("assistant", full_reply)

        return full_reply

if __name__ == "__main__":
    gpt = ChatGPT("sk-16d7cf8ffea74d25bf1ced61c80563d3")
    gpt.send_prompt("5+2")
    #gpt.send_prompt("Did you get my second message, or am I sending too fast?")