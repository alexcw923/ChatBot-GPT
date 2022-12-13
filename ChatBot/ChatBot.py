import os
import openai




class Bot:
    def __init__(self, name, ai_name = "AI", access = False, personality = "", scenario = "", age = 0) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.personality = personality
        self.scenario = scenario
        self.age = age
        self.chat_log = ""
        self.user_name = name
        self.ai_name = ai_name
        self.access = access
        
    
    def response(self, question) -> str:
        self.chat_log += f"{self.user_name}: {question}\n"
        prompt = f"{self.scenario}\n{self.personality}\n{self.chat_log}{self.ai_name}:"
        
        if self.access:
            text = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=100,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=2,
                stop = f"\n{self.user_name}: ")
        else:
            text = f"I love you!"
        
        self.chat_log += f"{self.ai_name}: {text}\n"
        return text
    
    def chat(self):
        
        while True:
            question = input(f'{self.user_name}: ')
            if question == "stop":
                print("Have a great day!")
                break
            
            print(f"{self.ai_name}: ", self.response(question))
    
    
