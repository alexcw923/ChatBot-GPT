import os
import openai
import whisper
import pyaudio
import wave
import time

class Bot:
    def __init__(self, name, ai_name = "AI", access = False, personality = "", scenario = "", age = 0, input_option = 0) -> None:
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.personality = personality
        self.scenario = scenario
        self.age = age
        self.chat_log = ""
        self.user_name = name
        self.ai_name = ai_name
        self.access = access
        self.input_option = input_option
        
        self.param={"model" : "text-davinci-003",
                    "temperature" : 0.7,
                    "max_tokens" : 100,
                    "top_p" : 1,
                    "frequency_penalty" :1,
                    "presence_penalty":2}
    
    def response(self, question) -> str:
        self.chat_log += f"{self.user_name}: {question}\n"
        prompt = f"{self.scenario}\n{self.personality}\n{self.chat_log}{self.ai_name}:"
        
        if self.access:
            completion = openai.Completion.create(
                model=self.param["model"],
                prompt=prompt,
                temperature=self.param["temperature"],
                max_tokens=self.param["max_tokens"],
                top_p=self.param["top_p"],
                frequency_penalty=self.param["frequency_penalty"],
                presence_penalty=self.param["presence_penalty"],
                stop = f"\n{self.user_name}: ")
            text = completion.choices[0].text
        else:
            text = f"Echo: {question}"
        
        self.chat_log += f"{self.ai_name}: {text}\n"
        return text
    
    def recordAudio(self):
        print("Start in 3 seconds...")
        time.sleep(3)
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
        
        stream.close()
        
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()
    
    def chat(self):
        model = whisper.load_model("base")
        
        while True:
            if self.input_option == "text":
                question = input(f'{self.user_name}: ')
            elif self.input_option == "audio":
                self.recordAudio()
                # load audio and pad/trim it to fit 30 seconds
                result = model.transcribe("question.wav", fp16 =False)
                question = result["text"]
                print(f"{self.user_name}: ", question)

            if question == "stop" or len(question) == 0:
                print("Have a great day!")
                break
            
            print(f"{self.ai_name}: ", self.response(question))
            
            
    def __str__(self):
        return self.chat_log
    
    def get_param(self):
        for k, v in self.param.items(): 
            print(k, "= ", v)
    
    def set_param(self, **kwargs):
        for key, value in kwargs.items():
            self.param[key] = value
    
    def set_engine(self, engine):
        self.param["model"] = engine

            
if __name__ == "__main__":
    bot = Bot(name = "bot", access = False, personality = "I am a bot", scenario = "I am a scenario", age = 0, input_option = "text")
    bot.chat()
    
    
