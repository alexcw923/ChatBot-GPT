import os
import openai
import whisper
import pyaudio
import wave
import time

class Bot:
    def __init__(self, name, ai_name = "AI", access = False, personality = "", scenario = "", age = 0, text_option = 0) -> None:
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.personality = personality
        self.scenario = scenario
        self.age = age
        self.chat_log = ""
        self.user_name = name
        self.ai_name = ai_name
        self.access = access
        self.text_option = text_option
        
    
    def response(self, question) -> str:
        self.chat_log += f"{self.user_name}: {question}\n"
        prompt = f"{self.scenario}\n{self.personality}\n{self.chat_log}{self.ai_name}:"
        
        if self.access:
            completion = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=100,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=2,
                stop = f"\n{self.user_name}: ")
            text = completion.choices[0].text
        else:
            text = f"Echo: {question}"
        
        self.chat_log += f"{self.ai_name}: {text}\n"
        return text
    
    def recordAudio(self):
        print("Start in 5 seconds...")
        time.sleep(5)
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "question.wav"
        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, 
                            channels=CHANNELS,
                            rate=RATE, 
                            input=True,
                            frames_per_buffer=CHUNK)
        print("recording started")
        Recordframes = []
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        print("recording stopped")
        
        # stream.stop_stream()
        stream.close()
        # audio.terminate()
        
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()
    
    def chat(self):
        model = whisper.load_model("base")
        
        while True:
            if self.text_option == 1:
                question = input(f'{self.user_name}: ')
            else:
                self.recordAudio()
                # load audio and pad/trim it to fit 30 seconds
                result = model.transcribe("question.wav", fp16 =False)
                question = result["text"]
                print(question)
                
            if question == "stop" or len(question) == 0:
                print("Have a great day!")
                break
            
            print(f"{self.ai_name}: ", self.response(question))
if __name__ == "__main__":
    bot = Bot(name = "bot", access = False, personality = "I am a bot", scenario = "I am a scenario", age = 0, text_option = 0)
    bot.chat()
    
    
