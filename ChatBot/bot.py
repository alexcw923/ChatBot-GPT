import os
import openai
import whisper
import pyaudio
import wave
import time

class Bot:
    def __init__(self, name : str, ai_name : str = "AI", personality : str = "", scenario : str = "", input_option : str = "text") -> None:
        """
        Args:
            name (str): The user's name the chatbot will chat with.
            ai_name (str, optional): The chatbot's name. Defaults to "AI".
            personality (str, optional): Chatbot's personality to set up personalize conversation. Defaults to empty string.
            scenario (str, optional): The scenario of the conversation. Could be the summary of the previous conversations. Defaults to empty string.
            input_option (str, optional): The users' input option of the conversation. "text" to chat with entering sentences. "audio" to chat with microphone. Defaults to "text".
        """
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.personality = personality
        self.scenario = scenario
        self.chat_log = ""
        self.user_name = name
        self.ai_name = ai_name
        self.input_option = input_option
        
        #the parameters of openai text completion
        self.param={"model" : "text-ada-001",
                    "temperature" : 0.7,
                    "max_tokens" : 100,
                    "top_p" : 1,
                    "frequency_penalty" :1,
                    "presence_penalty":2}
    
    def response(self, input_text, access=False) -> str:
        """Process the input text and the conversation.

        Args:
            input_text (str): the input text of the user
            access (bool, optional): access to openai text completion. Defaults to False.


        Returns:
            str: _description_
        """
        self.chat_log += f"{self.user_name}: {input_text}\n"
        prompt = f"{self.scenario}\n{self.personality}\n{self.chat_log}{self.ai_name}:"
        
        if access:
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
            text = f"Echo: {input_text}"
        
        self.chat_log += f"{self.ai_name}: {text}\n"
        return text
    
    def recordAudio(self, record_time : int = 5):
        """
        Record chat through microphone within 5 seconds. Output question.wav file into the directory.
        
        Args:
            record_time (int, optional): the recording time of the audio. Defaults to 5 seconds.
        """
        print("Start in 3 seconds...")
        time.sleep(3)
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512
        RECORD_SECONDS = record_time
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
    
    def speechToText(self, file_name : str = "question.wav") -> str:
        """Transcribe speech to text.

        Args:
            file_name (str, optional): the file storing the audio. Defaults to "question.wav".

        Returns:
            str: the speech in string format.
        """
        model = whisper.load_model("base")
        self.recordAudio()
        # load audio and pad/trim it to fit 30 seconds
        result = model.transcribe(file_name, fp16 =False)
        
            
        return result["text"]
        
    def chat(self):
        """Simply call this function to start a conversation
        """
        
        while True:
            question = self.speechToText() if self.input_option == "audio" else input(f'{self.user_name}: ')
            print(f"{self.user_name}: ", question)

            if question == "stop" or len(question) == 0:
                print("Have a great day!")
                break
            
            print(f"{self.ai_name}: ", self.response(question))
            
            
    def __str__(self):
        return self.chat_log
    
    def get_param(self):
        """
        Get the parameters of the text completion model.
        """
        for k, v in self.param.items(): 
            print(k, "= ", v)
    
    def set_param(self, **kwargs):
        """
        Set the parameters of the text completion model.
        """
        for key, value in kwargs.items():
            self.param[key] = value
    
    def set_engine(self, engine):
        """
        Set the engine of the text completion model.
        """
        self.param["model"] = engine

            
if __name__ == "__main__":
    bot = Bot(name = "bot", personality = "I am a bot", scenario = "I am a scenario", input_option = "text")
    bot.chat()
    
    
