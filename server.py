# -*- coding: utf-8 -*-
"""
================================================================================
 CT Guardian AI — tarpinis (proxy) serveris savarankiškam veikimui
================================================================================

Kam to reikia?
---------------
Web aplikacijoje esantis AI asistentas ir „Naujo aparato analizė" skirtukas
kviečia Anthropic Claude API. Naršyklė NEGALI saugiai laikyti ir tiesiogiai
naudoti API rakto (tai būtų nesaugu ir Anthropic to neleidžia dėl CORS
apsaugos). Todėl reikalingas nedidelis serveris „tarpe" — jis:

  1. saugo tavo Anthropic API raktą TIK serverio pusėje (aplinkos kintamajame),
  2. priima užklausas iš naršyklės (frontend'o),
  3. persiunčia jas į tikrąjį Anthropic API su raktu,
  4. grąžina atsakymą atgal į naršyklę.

Paleidimas
----------
1. Įdiek priklausomybes:
     pip install -r requirements.txt

2. Nustatyk savo Anthropic API raktą kaip aplinkos kintamąjį:

   Linux / macOS (terminale):
     export ANTHROPIC_API_KEY="sk-ant-...tavo-raktas..."

   Windows (PowerShell):
     $env:ANTHROPIC_API_KEY="sk-ant-...tavo-raktas..."

   (Raktą gauni https://console.anthropic.com/ → Settings → API Keys)

3. Paleisk serverį:
     python server.py

4. Atidaryk naršyklėje:
     http://localhost:5000

   Serveris pats atiduoda CT_Guardian_AI_app.html failą, o AI kvietimai
   automatiškai eina per šį serverį — CORS problemų nebus.

Pastaba dėl saugumo
--------------------
Vietiniam naudojimui šis serveris veikia be papildomos autentifikacijos. Jei
jį patalpinsi viešame internete (žr. README_serveriui.md skyrių apie diegimą
į Render.com), API raktą visada saugok debesijos platformos "Environment
Variables" / "Secrets" skiltyje — NIEKADA neįrašyk jo tiesiai į kodą ar į
GitHub repozitoriją.
================================================================================
"""

import os
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = "CT_Guardian_AI_app.html"

app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")
CORS(app)  # leidžia frontend'ui (jei paleistas iš kito adreso) kreiptis į šį serverį

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"


@app.route("/")
def index():
    """Atiduoda pagrindinį web aplikacijos HTML failą."""
    return send_from_directory(BASE_DIR, HTML_FILE)


@app.route("/api/messages", methods=["POST"])
def proxy_messages():
    """
    Priima frontend'o užklausą (tą patį JSON, kurį siųstų tiesiai į Anthropic API),
    prideda API raktą serverio pusėje ir persiunčia į Anthropic API.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({
            "error": "Serveryje nenustatytas ANTHROPIC_API_KEY aplinkos kintamasis. "
                     "Žr. instrukcijas server.py faile arba README_serveriui.md."
        }), 500

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Trūksta arba blogas JSON turinys užklausoje."}), 400

    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }

    try:
        upstream = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=60)
    except requests.RequestException as e:
        return jsonify({"error": f"Nepavyko pasiekti Anthropic API: {e}"}), 502

    # Persiunčiame Anthropic atsakymą (JSON turinį ir HTTP statusą) atgal frontend'ui.
    return Response(upstream.content, status=upstream.status_code, mimetype="application/json")


@app.route("/health")
def health():
    """Paprastas patikros maršrutas — patogu pasitikrinti, ar serveris veikia."""
    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    return jsonify({"status": "ok", "anthropic_api_key_nustatytas": has_key})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    is_local = os.environ.get("PORT") is None
    print("=" * 70)
    print(" CT Guardian AI — tarpinis serveris")
    if is_local:
        print(f" Atidaryk naršyklėje: http://localhost:{port}")
    else:
        print(f" Serveris paleistas debesijos aplinkoje ant prievado {port}")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(" ĮSPĖJIMAS: ANTHROPIC_API_KEY aplinkos kintamasis NENUSTATYTAS.")
        print(" AI funkcijos (chat, naujo aparato analizė) neveiks, kol jo nenustatysi.")
    print("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=is_local)

