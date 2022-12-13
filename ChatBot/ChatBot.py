import json
import openai
import torch



# openai.api_key = "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"
class ChatBot():
    def __init__(self, key, train, name) -> None:
        openai.api_key = key
        self.train = train
        self.chat_log = ""
        self.user_name = name
        
    def train(self):
        pass
    
    def response(self, question):
        self.chat_log += f"You: {question}\n"
        prompt = f"{self.chat_log}AI:"
        text = openai.Completion.create(prompt = prompt, 
                            engine =  "davinci", 
                            temperature = 0.85,top_p=1, 
                            frequency_penalty=0, 
                            presence_penalty=0.7, best_of=2,max_tokens=100,
                            stop = "\nHuman: ")
        self.chat_log += f"AI: {text}\n"
        return text
    
    def chat(self):
        while True:
            question = input('You:')
            if question == "stop":
                break
            
            print("AI: ", self.response(question))
    
    