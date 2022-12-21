from ChatBot.JOI import JOI

if __name__ == '__main__':
    debug = input('Debug: \n')
    access = False if debug == 1 else True

        
    name = input("Hi this is your Virtual Girlfriend. Can I have your name please? ")
    while len(name) == 0:
        name = input("I didn't catch you name. Can I have your name please? ")
        
        
    print(f"It's great to know you {name}. My name is JOI. Let me know what you want to talk about today.")
    option = input("(ask question through text or audio)")
    while option not in ["text", "audio"]:
        option = input("(ask question through text or audio)")
    if option == "audio":
        print("(Talk to JOI through your microphone!)")
    elif option == "text":
        print("(Talk to JOI through your terminal!)")
    ai = JOI(name, access = access, input_option = option)
    
    
    
    ai.chat()



