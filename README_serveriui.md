# CT Guardian AI — savarankiškas veikimas (be Claude.ai)

Šis aplankas leidžia paleisti CT Guardian AI web aplikaciją **savo kompiuteryje**,
su veikiančiu AI asistentu ir „Naujo aparato analizė" skirtuku — nepriklausomai
nuo Claude.ai lango.

## Kodėl reikia serverio, o ne tik HTML failo?

AI funkcijos kviečia Anthropic Claude API. Šis API reikalauja slapto rakto
(API key), kurio **niekada negalima įrašyti į naršyklės pusės kodą** (HTML/JS) —
kiekvienas, atidaręs failą ir peržiūrėjęs kodą, jį pamatytų ir galėtų
pasinaudoti tavo sąskaita. Todėl raktas laikomas serveryje, o naršyklė
kreipiasi į TAVO serverį, kuris jau saugiai persiunčia užklausą į Anthropic.

```
Naršyklė (HTML)  ──▶  Tavo serveris (server.py)  ──▶  Anthropic API
                       (čia laikomas API raktas)
```

## Failai šiame aplanke

| Failas | Paskirtis |
|---|---|
| `CT_Guardian_AI_app.html` | Pati web aplikacija (skydelis, taisyklės, AI asistentas, naujo aparato analizė) |
| `server.py` | Python/Flask tarpinis serveris |
| `requirements.txt` | Python bibliotekų sąrašas |
| `README_serveriui.md` | Šis failas |

## Žingsnis po žingsnio

### 1. Įsitikink, kad turi Python 3.9+

```bash
python3 --version
```

### 2. Įdiek reikalingas bibliotekas

Geriausia — atskiroje virtualioje aplinkoje:

```bash
cd šis-aplankas
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Gauk Anthropic API raktą

1. Eik į https://console.anthropic.com/
2. Prisijunk / užsiregistruok
3. Settings → API Keys → Create Key
4. Nusikopijuok raktą (jis prasideda `sk-ant-...`)

> ⚠️ API naudojimas yra mokamas pagal sunaudotus tokenus (paprastai centai už
> užklausą su šiuo modeliu). Nustatyk išlaidų limitą (Billing) savo Anthropic
> paskyroje, jei nori apsisaugoti nuo netikėtų sąskaitų.

### 4. Nustatyk API raktą kaip aplinkos kintamąjį

**macOS / Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-tavo-tikras-raktas"
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-tavo-tikras-raktas"
```

> Šį kintamąjį reikės nustatyti kiekvieną kartą, kai atidarai naują
> terminalo langą — arba įrašyk jį į `.bashrc` / `.zshrc` / sistemos
> aplinkos kintamuosius, jei nori, kad išliktų nuolat.

### 5. Paleisk serverį

```bash
python server.py
```

Turėtum matyti:
```
======================================================================
 CT Guardian AI — tarpinis serveris
 Atidaryk naršyklėje: http://localhost:5000
======================================================================
```

### 6. Atidaryk naršyklėje

```
http://localhost:5000
```

Viskas turėtų veikti: skydelis, taisyklės, AI asistentas ir naujo aparato
AI analizė.

## Kaip patikrinti, ar raktas tikrai nustatytas

Atidaryk naršyklėje: `http://localhost:5000/health`

Turėtum matyti:
```json
{"status": "ok", "anthropic_api_key_nustatytas": true}
```

Jei `false` — reiškia, kad terminale, kuriame paleidai `python server.py`,
`ANTHROPIC_API_KEY` nebuvo nustatytas prieš tai.

## Dažniausios problemos

| Problema | Sprendimas |
|---|---|
| „Nepavyko gauti arba apdoroti AI atsakymo" | Patikrink `/health` maršrutą — ar raktas nustatytas. Patikrink terminalo langą, kuriame veikia `server.py` — ten matysis tikroji klaida. |
| `ModuleNotFoundError: No module named 'flask'` | Nepaleista `pip install -r requirements.txt`, arba pamiršai aktyvuoti virtualią aplinką. |
| `401 Unauthorized` iš Anthropic | API raktas neteisingas arba nebegaliojantis — pasitikrink console.anthropic.com. |
| Puslapis neatsidaro `localhost:5000` | Ar terminale, kuriame paleidai `server.py`, nėra klaidos pranešimo? Ar joks kitas procesas neužima 5000 prievado? |

## Pastaba dėl modelio

`CT_Guardian_AI_app.html` faile AI kvietimai naudoja modelį `"claude-sonnet-5"`.
Jei tavo Anthropic paskyroje šis modelis nepasiekiamas arba nori naudoti kitą
(pvz. pigesnį/greitesnį), pakeisk eilutę `model: "claude-sonnet-5"` faile
`CT_Guardian_AI_app.html` (yra 2 vietos — pokalbio funkcija ir naujo aparato
analizės funkcija) į norimą modelio pavadinimą. Galimus modelius rasi
https://docs.claude.com dokumentacijoje.

## Priežiūros KPI rodikliai ir gedimų žurnalas

Naujas skirtukas **„🛠️ Gedimų žurnalas"** (inžinieriaus vaizde) leidžia:

1. **Registruoti gedimo pradžią** — nurodai aparatą, datą/laiką ir trumpą aprašymą, kai gedimas atsiranda.
2. **Uždaryti gedimą** — kai inžinierius baigia remontą, paspaudi „✓ Uždaryti gedimą" prie atviro įrašo ir nurodai pabaigos laiką, faktinį komponentą, remonto kainą bei tipą (reaktyvus/planinis). Sistema pati apskaičiuoja prastovos trukmę ir įtraukia įrašą į bendrą gedimų istoriją.
3. **Įvesti aparatų instaliavimo datas** — reikalingos MTBF skaičiavimui.

Pagal šiuos duomenis (bei importuotus/dirbtinius) automatiškai skaičiuojami trys standartiniai priežiūros rodikliai (rodomi „Gedimų istorija", „Vadovo apžvalga" ir „Gedimų žurnalas" skirtukuose):

- **MTTR** (Mean Time To Repair) — vidutinis remonto laikas = bendra prastova / gedimų skaičius.
- **MTBF** (Mean Time Between Failures) — vidutinis laikas tarp gedimų = bendras veikimo laikas (nuo instaliavimo datos) / gedimų skaičius. Reikalauja bent vieno aparato instaliavimo datos — jei jos nenurodytos, rodoma „—".
- **Bendra prastova** — visų gedimų (tiek reaktyvių, tiek planinių priežiūrų) prastovos valandų suma.

> ⚠️ Kaip ir importuoti duomenys, žurnale registruoti gedimai bei instaliavimo datos išlieka tik šios naršyklės sesijos atmintyje (dingsta atnaujinus puslapį). Nuolatiniam saugojimui reikėtų duomenų bazės — žr. „Ką daryti toliau" skyrių.

## Kaip prijungti REALIUS duomenis (ne dirbtinius)

Aplikacijoje (inžinieriaus vaizde) yra skirtukas **„📥 Realių duomenų importas"**.
Tai leidžia pereiti nuo dirbtinai sugeneruotų duomenų prie tavo tikrų duomenų
BE jokio papildomo programavimo:

1. **Dabartinė parko būklė.** Paruošk CSV failą su stulpeliais:
   ```
   aparatas,gamintojas,vamzdzio_temp_C,ausinimo_temp_C,gantry_vibracija_mm_s,
   generatoriaus_pulsacija_pct,detektoriaus_dreifas_pct,ventiliatoriaus_rpm,
   klaidu_kodu_sk,skenavimai_per_diena,tendencija,pastabos
   ```
   Šiuos rodmenis gausi iš aparato serviso meniu, gamintojo log failų, DICOM
   antraščių ar CMMS/Maximo eksporto. Skirtuke paspaudus „⬇️ Atsisiųsti CSV
   šabloną" gausi tuščią failą su teisingais stulpelių pavadinimais ir
   pavyzdine eilute. Įkėlus failą ir paspaudus „🤖 Importuoti ir analizuoti
   su AI", kiekvienai eilutei bus sugeneruota AI analizė (rizikos lygis,
   tikėtinas mazgas, prognozė) — lygiai taip pat, kaip „Naujo aparato
   analizė" skirtuke, tik automatizuotai visam parkui iš karto. Rezultatai
   atsiranda Skydelyje.

2. **Istoriniai gedimų įrašai.** Paruošk CSV su stulpeliais:
   ```
   data,aparatas,gamintojas,komponentas,tiekejas,remonto_kaina_eur,
   prastova_val,tipas,atsaukti_tyrimai
   ```
   (`data` formatu YYYY-MM-DD, `tipas` — „reaktyvus" arba „planinis"). Šie
   duomenys paprastai jau yra jūsų CMMS/Maximo sistemoje arba serviso
   žurnaluose. Importavus šis rinkinys IŠKART pakeičia dirbtinai sugeneruotus
   10 metų duomenis „Gedimų istorija", „Vadovo apžvalga" ir „Tendencijos ir
   sąnaudos" skirtukuose — visos suvestinės (metinės išlaidos, dažniausiai
   gendantys mazgai ir pan.) perskaičiuojamos automatiškai naršyklėje.

3. **AI asistentas** automatiškai „mato" naujausius (importuotus) duomenis
   pokalbyje — jam nieko papildomai konfigūruoti nereikia.

> ⚠️ Importuoti duomenys išlieka tik atmintyje šios naršyklės sesijos metu
> (kol neuždarai lango arba neatnaujini puslapio). Jei nori, kad duomenys
> išliktų nuolat tarp sesijų, reikėtų papildomai pridėti duomenų bazę
> (žr. „Tolesni žingsniai" skyrių taisyklėse) — tai jau nebe vieno
> failo, o pilnos sistemos plėtra.

## Kaip patalpinti šią programą viešame internete (kad ją rastų per Google)

Iki šiol programa veikė tik tavo kompiuteryje (`localhost`). Kad ją pasiektų
bet kas internete pagal nuorodą (ir kad ji galiausiai atsirastų Google
paieškoje), reikia ją patalpinti į **debesijos serverį**. Žemiau — nemokamas
būdas per **Render.com**, be jokios komandinės eilutės (viskas naršyklėje).

### 1 žingsnis — įkelk projektą į GitHub

GitHub — tai vieta, kur laikomas tavo kodas, iš kurios Render vėliau jį pasiims.

1. Eik į https://github.com ir susikurk nemokamą paskyrą (jei dar neturi).
2. Paspausk **„+"** viršuje dešinėje → **„New repository"**.
3. Duok pavadinimą, pvz. `ct-guardian-ai` → pasirink **„Public"** → paspausk **„Create repository"**.
4. Naujame (tuščiame) repozitorijos puslapyje paspausk nuorodą **„uploading an existing file"**.
5. Nutempk (drag & drop) VISUS failus iš `ct_guardian_serveris` aplanko:
   `server.py`, `requirements.txt`, `Procfile`, `CT_Guardian_AI_app.html`, `README_serveriui.md`.
6. Apačioje paspausk **„Commit changes"**.

> ⚠️ **NIEKADA neįkelk savo API rakto į GitHub** — jo šiuose failuose ir nėra (jis įrašomas tik Render nustatymuose, žr. žemiau).

### 2 žingsnis — susikurk Render.com paskyrą ir prijunk projektą

1. Eik į https://render.com → **„Get Started"** → registruokis (patogiausia — per GitHub paskyrą, vienu mygtuku).
2. Paspausk **„New +"** → **„Web Service"**.
3. Pasirink savo ką tik sukurtą repozitoriją `ct-guardian-ai` (gali reikėti paspausti „Connect account" ir leisti Render matyti tavo GitHub repozitorijas).
4. Užpildyk nustatymus:
   - **Name**: `ct-guardian-ai` (arba kitas norimas — tai bus dalis nuorodos)
   - **Region**: pasirink artimiausią (pvz. Frankfurt)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app`
   - **Instance Type**: `Free`

### 3 žingsnis — įrašyk API raktą SAUGIAI (Render nustatymuose, ne kode)

Toliau tame pačiame nustatymų puslapyje surask skiltį **„Environment Variables"** →
paspausk **„Add Environment Variable"**:
   - **Key**: `ANTHROPIC_API_KEY`
   - **Value**: tavo tikras raktas (prasideda `sk-ant-...`)

Tai vienintelė vieta, kur reikia įvesti raktą — jis bus saugomas užšifruotas Render serveryje, niekas kitas jo nematys.

### 4 žingsnis — paleisk diegimą

Paspausk **„Create Web Service"** (arba „Deploy") apačioje. Render pradės diegti —
tai užtruks 1–3 minutes. Kai baigsis, viršuje pamatysi žalią **„Live"** statusą
ir nuorodą, panašią į:
```
https://ct-guardian-ai.onrender.com
```

Atidaryk tą nuorodą naršyklėje — programa jau veiks bet kur internete, ne tik tavo kompiuteryje!

### 5 žingsnis — pasitikrink

Atidaryk `https://tavo-nuoroda.onrender.com/health` — turėtum matyti
`"anthropic_api_key_nustatytas": true`. Jei taip — viskas veikia, gali dalintis
pagrindine nuoroda su bet kuo.

### Svarbu žinoti apie nemokamą Render planą

- **„Užmiega" po 15 min. neveiklumo.** Jei niekas neaplanko puslapio 15 minučių, serveris „užmiega", o pirmas kito žmogaus apsilankymas gali užtrukti ~30-60 sek., kol serveris „pabunda". Tai normalu nemokamam planui.
- Jei norėsi, kad visada veiktų greitai — reikėtų mokamo plano (nuo ~7 USD/mėn.).

### Kad puslapį rastų per Google

- Google savaime suranda viešus puslapius per kelias dienas–savaites, bet gali paspartinti:
  1. Eik į https://search.google.com/search-console
  2. Pridėk savo Render nuorodą kaip "Property".
  3. Paspausk „Request Indexing".
- Puslapio pavadinimas (title) jau nustatytas kaip **„CT Guardian AI"**, tad būtent to ieškant, jis turėtų būti lengviau atrandamas laikui bėgant.
- Jei nori "gražesnio" adreso (pvz. `ctguardianai.lt` vietoj `.onrender.com`), reikėtų nusipirkti domeną (pvz. per Namecheap ar panašiai, ~10 €/metus) ir jį susieti Render nustatymuose (**Settings → Custom Domain**).

## Papildomos apsaugos priemonės, jei programa naudosis daugiau žmonių

Aukščiau aprašytas Render.com diegimas jau suteikia HTTPS ir saugiai laikomą
API raktą. Jei programa taps viešai naudojama daugelio žmonių (ne tik
demonstracijai), verta papildomai apsvarstyti:
- naudotojų autentifikaciją (kad bet kas internete negalėtų neribotai naudoti tavo API rakto ir kelti sąskaitos),
- užklausų skaičiaus ribojimą (rate limiting) — pvz. per Flask-Limiter biblioteką,
- Render "Environment Variables" reguliarų peržiūrėjimą ir rakto atnaujinimą, jei įtarsi, kad jis kur nors netyčia paviešintas.
