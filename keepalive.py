import threading
import requests
import time

def keep_alive():
    def run():
        while True:
            try:
                requests.get("https://scornful-andreana-moxi35-c66f799a.koyeb.app/")
            except:
                pass
            time.sleep(90)
    threading.Thread(target=run, daemon=True).start()
