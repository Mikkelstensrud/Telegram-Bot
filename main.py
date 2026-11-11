import requests
import aksjer
from datetime import datetime
import os

import requests
from dotenv import load_dotenv

import aksjer

load_dotenv()

nå = datetime.now()
nåtid = nå.strftime("%H:%M:%S")

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
url_fil = f"https://api.telegram.org/bot{TOKEN}/sendDocument"


def aksjeRapport():

    aksjer.kjor_aksjerscan()
    valgfri_tekst = f"Live Stock Prices - Close Values\nTime: {nåtid}"

    data = {
        "chat_id": CHAT_ID,
        "text": valgfri_tekst
    }
    requests.post(url, data=data)

    with open("aksjerFil.json", "rb") as fil:
        requests.post(url_fil, data={"chat_id": CHAT_ID}, files={"document": fil})

def niceCom():
    data = {
        "chat_id": CHAT_ID,
        "text": "Fyfaen du var kjekk i dag ass"
    }
    requests.post(url, data=data)



print("1 --> Live stock rapport")
print("2 --> Nice comment")
inp = int(input("Skriv inn tall: "))

if inp == 1:
    aksjeRapport()
elif inp == 2:
    niceCom()