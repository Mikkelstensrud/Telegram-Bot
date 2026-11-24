from datetime import datetime
import os
import time
import requests
from dotenv import load_dotenv
import aksjer
import weather

load_dotenv()

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url_message = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
url_fil = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
API = f"https://api.telegram.org/bot{TOKEN}"

offset = None


def hent_melding():
    global offset

    while True:
        svar = requests.get(
            f"{API}/getUpdates",
            params={"offset": offset, "timeout": 30},
            timeout=40,
        ).json()

        for update in svar["result"]:
            offset = update["update_id"] + 1
            melding = update.get("message")
            if melding and str(melding["chat"]["id"]) == str(CHAT_ID):
                return melding.get("text", "")

#Aksjer
def stockrapport():
    nåtid = datetime.now().strftime("%H:%M:%S")
    pdf = aksjer.kjor_aksjerscan()
    if pdf is None:
        requests.post(url_message, data={"chat_id": CHAT_ID, "text": "Fikk ingen kurser fra Yahoo Finance."})
    else:
        with open(pdf, "rb") as fil:
            requests.post(
                url_fil,
                data={"chat_id": CHAT_ID, "caption": f"📈 Aksjerapport {nåtid}"},
                files={"document": fil},
                timeout=30,
            )

# Vær for imorgen
def weatherrapport():
    data = {
        "chat_id": CHAT_ID,
        "text": weather.main()
    }
    requests.post(url_message, data=data)


# Hopp over gamle meldinger én gang ved oppstart
try:
    gamle = requests.get(f"{API}/getUpdates", params={"offset": -1}, timeout=10).json()
    if gamle["result"]:
        offset = gamle["result"][-1]["update_id"] + 1
except requests.RequestException:
    pass

print("Boten kjører... (Ctrl+C for å avslutte)")

while True:
    try:
        tekst = hent_melding().lower()
        print("Fikk:", tekst)

        if tekst == "/aksjer" or tekst == "/stocks":
            stockrapport()
        elif tekst == "/vaer":
            weatherrapport()
        else:
            requests.post(url_message, data={"chat_id": CHAT_ID, "text": "Ukjent kommando"})

    except KeyboardInterrupt:
        print("Avslutter.")
        break
    except Exception as feil:
        print("Feil:", feil)
        time.sleep(5)