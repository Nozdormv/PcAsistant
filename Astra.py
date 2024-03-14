import os
import webbrowser
import wikipedia

# ANSI color codes for text styling
class color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'

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
    print("4. Run start: Opens Discord and Chrome with Twitch URL.")
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

def run_start():
    open_application("Discord")
    webbrowser.get("chrome").open("https://www.twitch.tv/")

def main():
    greet()
    while True:
        user_input = input("How can I assist you?\n")
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
        elif user_input.lower() == 'run start':
            run_start()
            print("Discord and Chrome with Twitch URL are being opened...")
        else:
            print("I'm sorry, I didn't understand that. Can you please repeat?")

if __name__ == "__main__":
    main()
