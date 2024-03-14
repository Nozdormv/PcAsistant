import os
import webbrowser
import wikipedia
import random
import platform
import psutil

# ANSI color codes for text styling
class color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'

# Predefined jokes and quotes
jokes = [
    ("Why don't scientists trust atoms?", "Because they make up everything!"),
    ("Did you hear about the mathematician who's afraid of negative numbers?", "He'll stop at nothing to avoid them!"),
    ("Why did the scarecrow win an award?", "Because he was outstanding in his field!"),
    ("What do you call fake spaghetti?", "An impasta!"),
    ("Why did the bicycle fall over?", "Because it was two-tired!")
]

quotes = [
    ("The greatest glory in living lies not in never falling, but in rising every time we fall.", "Nelson Mandela"),
    ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
    ("Life is what happens when you're busy making other plans.", "John Lennon"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("Spread love everywhere you go. Let no one ever come to you without leaving happier.", "Mother Teresa")
]

def greet():
    # Clear screen and set window title
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033]0;Astra - Personal Assistant\007", end='')  # Set window title
    print(color.BOLD + color.GREEN + "          ___           ")
    print("        //   \\\\         ")
    print("       ||" + color.BLUE + "Astra" + color.GREEN + "||        ")
    print("        \\\\___//         ")
    print("     ___________        ")
    print("    /   Welcome \       ")
    print("   /    to your  \      ")
    print("  /  Personal    /\\     ")
    print(" /   Assistant  /  \\    ")
    print("/______________/____\\   ")
    print(" ")
    print(color.END + "Hello! I am your personal assistant, Astra.")
    print(" ")
    print("I can help you with the following tasks:")
    print(" ")
    print("1. Open applications: Type 'open <application_name>'.")
    print("2. Search the web: Type 'search <query>'.")
    print("3. Get summary from Wikipedia: Type 'summary <topic>'.")
    print("4. Get a joke: Type 'joke'.")
    print("5. Get a quote: Type 'quote'.")
    print("6. Get system information: Type 'sysinfo'.")
    print(" ")
    print("Type 'quit' to exit.")
    print(" ")

def open_application(application_name):
    try:
        os.system(f"start {application_name}")
        print(f"Opening {application_name}...")
    except Exception as e:
        print(f"Error: {e}")

def search_web(query):
    try:
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
        print(f"Searching the web for '{query}'...")
    except Exception as e:
        print(f"Error: {e}")

def get_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        print(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        print("Ambiguous topic. Please provide more specific query.")
    except wikipedia.exceptions.PageError as e:
        print("Page not found. Please provide a valid query.")
    except Exception as e:
        print(f"Error: {e}")

# Function to get a random joke
def get_joke():
    return random.choice(jokes)

# Function to get a random quote
def get_quote():
    return random.choice(quotes)

# Function to get system information
def get_system_info():
    print("System Information:")
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Processor: {platform.processor()}")
    print(f"Total Memory: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB")
    print(f"Available Memory: {psutil.virtual_memory().available / (1024 ** 3):.2f} GB")
    print(f"Total CPU Cores: {psutil.cpu_count(logical=False)}")
    print(f"Total CPU Threads: {psutil.cpu_count(logical=True)}")
    print(f"CPU Usage: {psutil.cpu_percent()}%")
    print()

def main():
    greet()
    while True:
        user_input = input("How can I assist you?\n\n")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif 'open' in user_input:
            app = user_input.split('open ')[1]
            open_application(app)
            print(f"{app} is being opened...")
        elif 'search' in user_input:
            query = user_input.split('search ')[1]
            search_web(query)
            print(f"Searching the web for '{query}'...")
        elif 'summary' in user_input:
            topic = user_input.split('summary ')[1]
            get_wikipedia_summary(topic)
        elif user_input.lower() == 'joke':
            setup, punchline = get_joke()
            print("Here's a joke for you:")
            print(setup)
            print(punchline)
        elif user_input.lower() == 'quote':
            quote, author = get_quote()
            print("Here's a quote for you:")
            print(f'"{quote}" - {author}')
        elif user_input.lower() == 'sysinfo':
            get_system_info()
        else:
            print("I'm sorry, I didn't understand that. Can you please repeat?")

if __name__ == "__main__":
    main()
