import requests

LAT, LON = 59.91, 10.75  # Oslo
FRA_TIME, TIL_TIME = 8, 20

KODER = {
    0: "☀️ Klarvær",
    1: "🌤️ Stort sett klart",
    2: "⛅ Delvis skyet",
    3: "☁️ Overskyet",
    45: "🌫️ Tåke",
    48: "🌫️ Rimtåke",
    51: "🌦️ Lett yr",
    53: "🌦️ Yr",
    55: "🌧️ Kraftig yr",
    56: "🌧️ Lett underkjølt yr",
    57: "🌧️ Underkjølt yr",
    61: "🌧️ Lett regn",
    63: "🌧️ Regn",
    65: "🌧️ Kraftig regn",
    66: "🌧️ Lett underkjølt regn",
    67: "🌧️ Underkjølt regn",
    71: "🌨️ Lett snø",
    73: "🌨️ Snø",
    75: "❄️ Kraftig snø",
    77: "❄️ Snøkorn",
    80: "🌦️ Lette regnbyger",
    81: "🌧️ Regnbyger",
    82: "⛈️ Kraftige regnbyger",
    85: "🌨️ Lette snøbyger",
    86: "❄️ Kraftige snøbyger",
    95: "⛈️ Tordenvær",
    96: "⛈️ Tordenvær med lett hagl",
    99: "⛈️ Tordenvær med kraftig hagl",
}


def hent_vaer_i_morgen():
    svar = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": LAT,
            "longitude": LON,
            "hourly": "weather_code",
            "forecast_days": 2,
            "timezone": "auto",
        },
        timeout=10,
    )
    svar.raise_for_status()
    data = svar.json()["hourly"]

    # Datoen i morgen = den andre datoen i svaret (i norsk tid)
    datoer = sorted({tid[:10] for tid in data["time"]})
    i_morgen = datoer[1]

    timer = []
    for tid, kode in zip(data["time"], data["weather_code"]):
        dato, klokke = tid[:10], int(tid[11:13])
        if dato == i_morgen and FRA_TIME <= klokke <= TIL_TIME:
            timer.append((tid, kode))
    return i_morgen, timer


def main():
    try:
        dato, timer = hent_vaer_i_morgen()
    except requests.RequestException as feil:
        print("Kunne ikke hente værdata:", feil)
        return

    melding = f"Værmelding for Oslo, {dato}, kl. {FRA_TIME:02d}-{TIL_TIME:02d}"
    for tid, kode in timer:
        melding += f"\n{tid[11:16]}  {kode:>2}  {KODER.get(kode, 'Ukjent')}"
    return melding
