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
pdf = aksjer.kjor_aksjerscan()
if pdf is None:
    requests.post(url, data={"chat_id": CHAT_ID, "text": "Fikk ingen kurser fra Yahoo Finance."})
else:
    with open(pdf, "rb") as fil:
        requests.post(
            url_fil,
            data={"chat_id": CHAT_ID, "caption": f"📈 Aksjerapport {nåtid}"},
            files={"document": fil},
        )

# Vær for imorgen
data = {
    "chat_id": CHAT_ID,
    "text": weather.main()
}
requests.post(url, data=data)