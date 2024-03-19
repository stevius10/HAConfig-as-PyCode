import logging
import inspect
import os
import datetime

class Logger:
    def __init__(self):
        pass
    
    def __call__(self, message):
        try:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame)[1]
            function_name = caller_frame.function
            filename = os.path.basename(caller_frame.filename)
            current_time = datetime.datetime.now().strftime("%H:%M")

            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

            # Logge die Nachricht in die Konsole
            log.info(f"{current_time} - {function_name} in {filename}: {message}")

            print(f"{current_time} - {function_name} in {filename}: {message}")
        except Exception as e:
            print(f"Fehler beim Loggen: {e}")

# Direkter Aufruf des Loggers ohne Methodennamen
Logger()("Testnachricht")