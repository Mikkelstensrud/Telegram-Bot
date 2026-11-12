import json
from datetime import datetime
from pathlib import Path

import yfinance as yf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

FIL = Path("aksjerFil.json")

aksjerselskaper = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Google": "GOOGL",
}


def hent_kurser():
    kurser = {}
    for navn, ticker in aksjerselskaper.items():
        try:
            historikk = yf.Ticker(ticker).history(period="1d")
            if not historikk.empty:
                kurser[navn] = round(float(historikk["Close"].iloc[-1]), 2)
        except Exception as feil:
            print(f"Kunne ikke hente {navn}: {feil}")
    return kurser


def les_forrige():
    if FIL.exists():
        try:
            with open(FIL, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def lagre(data):
    with open(FIL, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def norsk_tall(tall):
    return f"{tall:,.2f}".replace(",", " ").replace(".", ",")


def lag_pdf(nye, gamle, filnavn="aksjerapport.pdf"):
    tid = datetime.now().strftime("%d.%m.%Y kl. %H:%M")

    moerk = colors.HexColor("#0f172a")
    lys = colors.HexColor("#f1f5f9")
    gronn = colors.HexColor("#16a34a")
    rod = colors.HexColor("#dc2626")
    graa = colors.HexColor("#64748b")

    doc = SimpleDocTemplate(
        filnavn, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="Aksjerapport",
    )
    
    tittel = ParagraphStyle("tittel", fontName="Helvetica-Bold",
                            fontSize=24, leading=30, textColor=moerk, spaceAfter=6)
    under = ParagraphStyle("under", fontName="Helvetica",
                           fontSize=11, leading=15, textColor=graa, spaceAfter=20)
    bunn = ParagraphStyle("bunn", fontName="Helvetica",
                          fontSize=9, leading=12, textColor=graa)

    data = [["Selskap", "Ticker", "Kurs (USD)", "Endring"]]
    farger = []

    rader = sorted(nye.items(), key=lambda x: x[1], reverse=True)
    for i, (navn, kurs) in enumerate(rader, start=1):
        if gamle.get(navn):
            endring = (kurs - gamle[navn]) / gamle[navn] * 100
            tekst = f"{endring:+.1f} %".replace(".", ",")
            farger.append(("TEXTCOLOR", (3, i), (3, i), gronn if endring >= 0 else rod))
        else:
            tekst = "–"
            farger.append(("TEXTCOLOR", (3, i), (3, i), graa))
        data.append([navn, aksjerselskaper[navn], f"${norsk_tall(kurs)}", tekst])

    tabell = Table(data, colWidths=[6 * cm, 3 * cm, 4 * cm, 4 * cm])
    tabell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), moerk),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTNAME", (2, 1), (3, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, lys]),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("LINEBELOW", (0, -1), (-1, -1), 1, moerk),
        *farger,
    ]))

    doc.build([
        Paragraph("Aksjerapport", tittel),
        Paragraph(f"Sluttkurser · {tid}", under),
        tabell,
        Spacer(1, 16),
        Paragraph("Endring er mot forrige kjøring. Data fra Yahoo Finance.", bunn),
    ])
    return filnavn


def kjor_aksjerscan():
    """Henter kurser, lager PDF og returnerer filnavnet (eller None ved feil)."""
    gamle = les_forrige()
    nye = hent_kurser()

    if not nye:
        return None

    pdf = lag_pdf(nye, gamle)
    gamle.update(nye)
    lagre(gamle)
    return pdf