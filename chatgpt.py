from openai import OpenAI
import time
import tiktoken
import threading
from datetime import datetime

from base_has_logs import BaseHasLogs
from the_memory import TheMemory


class ChatGPT(BaseHasLogs):

    def __init__(self, api_key: str):
        super().__init__()
        self._client = OpenAI(api_key=api_key, base_url="https://dsui.twr.church/api/v1")
        self._mem = TheMemory()

        f = open('prompt.txt')
        sys_prompt = '\n'.join(f.readlines())
        f.close()

        # Either issue system prompt to get it in there or ensure it's current
        if self._mem.is_first_message:
            self.send_prompt(sys_prompt, input_role="system")
        else:
            self._mem._update_system_prompt(sys_prompt)

    def send_prompt(self, prompt: str, input_role="user"):
        # Record to Redis
        full_prompt = f"{self._get_time_stamp()} {prompt}" if input_role == "user" else prompt
        self._mem.add_message(input_role, full_prompt)

        # Get all messages
        messages = self._mem.get_messages()

        # Start thread for log token count
        thread = threading.Thread(target=self._log_token_count, args=(messages,))
        thread.start()

        # Send prompt
        self._logger.info("Prompt is issued")
        stream = self._client.chat.completions.create(
            model="mistral-small3.1:24b",
            messages=messages,
            stream=True
        )

        full_reply = ""

        # Parse reply stream
        for chunk in stream:
            real_content = chunk.choices[0].delta.content

            if real_content is not None:
                full_reply += real_content
        
        self._logger.info(f"Response: {full_reply}")
        self._mem.add_message("assistant", full_reply)
        thread.join()

        return full_reply
    
    def _log_token_count(self, messages: list) -> str:
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = 0
        
        for curr_msg in messages:
            num_tokens += 3

            for v in curr_msg.values():
                num_tokens += len(encoding.encode(v))
        
        self._logger.info(f"Token usage: {num_tokens:.2e}")

    def _get_time_stamp(self):
        now = datetime.now()
        timestamp = now.strftime("%A, %B %d, %Y, %I:%M:%S %p")

        return f"[{timestamp}]"
    
if __name__ == "__main__":
    gpt = ChatGPT("sk-16d7cf8ffea74d25bf1ced61c80563d3")
    gpt.send_prompt("5+2")
    #gpt.send_prompt("Did you get my second message, or am I sending too fast?")