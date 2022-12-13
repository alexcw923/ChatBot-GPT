import os
import openai




class ChatBot():
    def __init__(self, access) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.chat_log = ""
        self.user_name = None
        self.access = access
        
    
    def response(self, question) -> str:
        self.chat_log += f"{self.user_name}: {question}\n"
        prompt = f"{self.chat_log}JOI:"
        
        if not self.access:
            text = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=3000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop = f"\n{self.user_name}: ")
        else:
            text = f"I love you!"
        
        self.chat_log += f"JOI: {text}\n"
        return text
    
    def chat(self):
        print("This is your virtual girlfriend. What is your name?")
        self.user_name = input()
        print("JOI: Great! My name is JOI. How can I help you?")
        while True:
            question = input(f'{self.user_name}:')
            if question == "stop":
                break
            
            print("AI: ", self.response(question))
    
    
