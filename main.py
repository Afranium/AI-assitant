import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import time # Added for stability
from rich.console import Console
from rich.panel import Panel

console = Console()

class AfraniumAssistant:
    def __init__(self):
        self.listener = sr.Recognizer()
        
        # --- IMPROVED LISTENING SETTINGS ---
        # How long it waits for you to start speaking
        self.listener.pause_threshold = 3.0 
        # Helps ignore background hum
        self.listener.dynamic_energy_threshold = True 
        
        self.engine = pyttsx3.init()
        self.name = "afranium"
        
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id) 
        self.engine.setProperty('rate', 160)

    def display_message(self, text, title="SYSTEM", style="cyan"):
        console.print(Panel(text, title=title, border_style=style, expand=False))

    def talk(self, text):
        self.display_message(text, title="AFRANIUM SAYS", style="bold magenta")
        self.engine.say(text)
        self.engine.runAndWait() # Standard pyttsx3 command

    def take_command(self):
        try:
            with sr.Microphone() as source:
                # 1. Calibrate for the room noise
                self.listener.adjust_for_ambient_noise(source, duration=1)
                console.print("\n[bold green]Listening...[/bold green] (Speak now)")
                
                # 2. phrase_time_limit=15 gives you 15 seconds to finish your sentence
                voice = self.listener.listen(source, timeout=10, phrase_time_limit=15)
                
                console.print("[yellow]Processing voice...[/yellow]")
                command = self.listener.recognize_google(voice)
                command = command.lower()
                
                if self.name in command:
                    command = command.replace(self.name, '').strip()
                
                return command

        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return "none"
        except sr.RequestError:
            self.display_message("Internet connection lost!", "ERROR", "red")
            return "none"
        except Exception as e:
            return "none"

    def run(self):
        self.display_message("AFRANIUM INTELLIGENCE ONLINE", "BOOT SUCCESS", "green")
        
        while True:
            command = self.take_command()

            if command == "none" or len(command) < 2:
                continue

            self.display_message(f"User said: {command}", "INPUT", "blue")

            if 'play' in command:
                song = command.replace('play', '').strip()
                self.talk(f'Playing {song} on YouTube')
                # Tiny pause helps the pyttsx3 engine close properly before the browser opens
                time.sleep(0.5) 
                pywhatkit.playonyt(song)

            elif 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                self.talk(f"The current time is {current_time}")

            elif 'who is' in command or 'what is' in command:
                query = command.replace('who is', '').replace('what is', '')
                try:
                    info = wikipedia.summary(query, sentences=1)
                    self.talk(info)
                except:
                    self.talk("I'm sorry, I couldn't find a specific result for that.")
            
            elif 'terminate' in command or 'stop' in command or 'shutdown' in command:
                self.talk("System shutting down. Goodbye.")
                break

if __name__ == "__main__":
    assistant = AfraniumAssistant()
    assistant.run()