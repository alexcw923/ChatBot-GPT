from ChatBot.JOI import JOI

if __name__ == '__main__':
    name = input("Hi this is your Virtual Girlfriend. Can I have your name please? ")
    print(f"It's great to know you {name}. My name is JOI. Let me know what you want to talk about today.")
    ai = JOI(name)
    ai.chat()