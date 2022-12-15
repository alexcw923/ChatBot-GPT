import os
import openai
import whisper

class Bot:
    def __init__(self, name, ai_name = "AI", access = False, personality = "", scenario = "", age = 0, text_option = 1) -> None:
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
    
    def chat(self):
        
        model = whisper.load_model("base")
        
        while True:
            if self.text_option == 1:
                question = input(f'{self.user_name}: ')
            else:
                # load audio and pad/trim it to fit 30 seconds
                audio = whisper.load_audio("audio.mp3")
                audio = whisper.pad_or_trim(audio)

                # make log-Mel spectrogram and move to the same device as the model
                mel = whisper.log_mel_spectrogram(audio).to(model.device)

                # detect the spoken language
                _, probs = model.detect_language(mel)
                print(f"Detected language: {max(probs, key=probs.get)}")

                # decode the audio
                options = whisper.DecodingOptions()
                result = whisper.decode(model, mel, options)

                # print the recognized text
                question = result.text
                print(question)
                
            if question == "stop":
                print("Have a great day!")
                break
            
            print(f"{self.ai_name}: ", self.response(question))
    
    
