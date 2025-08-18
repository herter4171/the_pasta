from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
import io

from base_has_logs import BaseHasLogs

class TheVoice(BaseHasLogs):
    def __init__(self):
        super().__init__()  
        self._client = OpenAI(base_url="http://192.168.68.75:8880/v1", api_key="not-needed")

    def speak(self, text):
        with self._client.audio.speech.with_streaming_response.create(
            model="kokoro",
            voice="am_adam", #single or multiple voicepack combo
            input=text
        ) as response:
            audio_bytes = response.read()

        audio_buffer = io.BytesIO(audio_bytes)
        
        # Load the audio from the buffer using pydub.
        # It automatically decodes the MP3 data.
        audio_segment = AudioSegment.from_mp3(audio_buffer)
        
        # Play the loaded audio segment.
        play(audio_segment)

if __name__ == "__main__":
     v = TheVoice()
     v.speak("Hello world")
