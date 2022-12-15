from ChatBot.JOI import JOI

if __name__ == '__main__':
    debug = input('Debug: \n')
    access = False if debug == 1 else True

        
    name = input("Hi this is your Virtual Girlfriend. Can I have your name please? ")
    print(f"It's great to know you {name}. My name is JOI. Let me know what you want to talk about today.")
    print("(Talk to JOI though your microphone!)")
    ai = JOI(name, access = access)
    
    
    
    ai.chat()



