from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = "gizli55"

def get_has_fiyati():
    return 2430.0

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == "kocero55":
            session["logged_in"] = True
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    has_f = get_has_fiyati()
    result, saved = {}, False
    if request.method == "POST":
        g = float(request.form["gram"])
        m = int(request.form["milyem"])
        s = float(request.form["satis"])
        maliyet = round(g * m / 1000 * has_f, 2)
        kar = round(s - maliyet, 2)
        result = {"maliyet": maliyet, "kar": kar}
        df = pd.DataFrame([{
            "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Gram": g, "Milyem": m, "Has": has_f, "Satış": s,
            "Maliyet": maliyet, "Kâr": kar
        }])
        df.to_excel("rapor.xlsx", index=False)
        saved = True
    return render_template("index.html", has_f=has_f, result=result, saved=saved)

if __name__ == "__main__":
    app.run(debug=True)
