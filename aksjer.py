import yfinance as yf
import json


aksjerselskaper = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Google": "GOOGL"
}

def kjor_aksjerscan():
    with open("aksjerFil.json", "r", encoding="utf-8") as fil: #leser JSON-filen.
        data = json.load(fil)
        for stock in aksjerselskaper:

            aksje = yf.Ticker(aksjerselskaper[stock])

            historikk = aksje.history(period="1d")
            if not historikk.empty:
                siste_kurs = historikk["Close"].iloc[-1]

                # Legger til eller oppdaterer informasjon
                data[stock] = round(float(siste_kurs), 2)

    with open("aksjerFil.json", "w", encoding="utf-8") as fil: #lagrer endringene i den eksisterende filen.
            json.dump(data, fil, indent=4)