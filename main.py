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

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
url_fil = f"https://api.telegram.org/bot{TOKEN}/sendDocument"


#Aksjer
aksjer.kjor_aksjerscan()
valgfri_tekst = f"Live Stock Prices - Close Values\nTime: {nåtid}"
data = {
    "chat_id": CHAT_ID,
    "text": valgfri_tekst
}
requests.post(url, data=data)
with open("aksjerFil.json", "rb") as fil:
    requests.post(url_fil, data={"chat_id": CHAT_ID}, files={"document": fil})

# Vær for imorgen
data = {
    "chat_id": CHAT_ID,
    "text": weather.main()
}
requests.post(url, data=data)