from datetime import datetime
import os
import requests
from dotenv import load_dotenv
import aksjer
import weather

load_dotenv()

nå = datetime.now()
nåtid = nå.strftime("%H:%M:%S")

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url_message = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
url_fil = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
API = f"https://api.telegram.org/bot{TOKEN}"


def hent_melding():
    # Hopp over gamle meldinger som ligger igjen hos Telegram
    gamle = requests.get(f"{API}/getUpdates", params={"offset": -1}, timeout=10).json()
    offset = None
    if gamle["result"]:
        offset = gamle["result"][-1]["update_id"] + 1

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
tekst = hent_melding() #Melding sendt fra telefon


#Aksjer
def stockrapport():
    pdf = aksjer.kjor_aksjerscan()
    if pdf is None:
        requests.post(url_message, data={"chat_id": CHAT_ID, "text": "Fikk ingen kurser fra Yahoo Finance."})
    else:
        with open(pdf, "rb") as fil:
            requests.post(
                url_fil,
                data={"chat_id": CHAT_ID, "caption": f"📈 Aksjerapport {nåtid}"},
                files={"document": fil},
            )

# Vær for imorgen
def weatherrapport():
    data = {
        "chat_id": CHAT_ID,
        "text": weather.main()
    }
    requests.post(url_message, data=data)

tekst = tekst.lower()

if tekst == "/aksjer" or tekst == "/stocks":
    stockrapport()
elif tekst == "/vaer":
    weatherrapport()
else:
    requests.post(url_message, data={"chat_id": CHAT_ID, "text": "Ukjent kommando"})