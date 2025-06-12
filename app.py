import streamlit as st
import pandas as pd
import random

# --- Spelerslijst (voorbeeld 10, breid uit tot 100+) ---
spelers_data = [
    {"naam": "Lionel Messi", "club": "PSG", "rating": 93, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/89/Lionel_Messi_20180626.jpg"},
    {"naam": "Cristiano Ronaldo", "club": "Manchester United", "rating": 92, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"},
    {"naam": "Erling Haaland", "club": "Manchester City", "rating": 88, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Erling_Haaland_2019.jpg"},
    {"naam": "Kylian Mbappé", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Kylian_Mbappe_2021.jpg"},
    {"naam": "Kevin De Bruyne", "club": "Manchester City", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/5/53/Kevin_De_Bruyne_201807091.jpg"},
    {"naam": "Neymar Jr", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/9/99/Neymar_2018.jpg"},
    {"naam": "Robert Lewandowski", "club": "Barcelona", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/3/36/Robert_Lewandowski_2019.jpg"},
    {"naam": "Mohamed Salah", "club": "Liverpool", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/0/03/Mohamed_Salah_2018.jpg"},
    {"naam": "Luka Modrić", "club": "Real Madrid", "rating": 87, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Luka_Modric_2018.jpg"},
    {"naam": "Sergio Ramos", "club": "PSG", "rating": 86, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/c/c5/Sergio_Ramos_2018.jpg"},
    # ... hier kan je aanvullen tot 100+
]

# Maak uitgebreide lijst inclusief TOTS-versies
spelers_data_ext = []
for speler in spelers_data:
    spelers_data_ext.append({**speler, "is_tots": False})
    spelers_data_ext.append({
        **speler,
        "rating": speler["rating"] + 3,
        "type": "TOTS",
        "naam": speler["naam"] + " (TOTS)",
        "is_tots": True
    })

# --- Helper functie voor unieke id ---
def maak_unieke_id(speler):
    return f"{speler['naam']}_{speler['club']}"

# --- Init sessie variabelen ---
if "coins" not in st.session_state:
    st.session_state.coins = 1000
if "message" not in st.session_state:
    st.session_state.message = ""
if "gepackte_spelers" not in st.session_state:
    st.session_state.gepackte_spelers = {}
if "team" not in st.session_state:
    st.session_state.team = []

# --- Titel ---
st.title("🎮 EAFC Pack Opening Game")

# --- Sidebar: Coins en minigames ---
st.sidebar.title("🛒 Shop")
st.sidebar.write(f"💰 Coins: {st.session_state.coins}")

st.sidebar.markdown("---")
st.sidebar.subheader("🎲 Minigames om coins te verdienen")

# Minigame 1: Kop of Munt
st.sidebar.write("1️⃣ Kop of Munt (win 200 coins)")
keuze = st.sidebar.radio("Kies Kop of Munt:", ["Kop", "Munt"])
if st.sidebar.button("Speel Kop of Munt"):
    uitkomst = random.choice(["Kop", "Munt"])
    if keuze == uitkomst:
        st.session_state.coins += 200
        st.sidebar.success(f"🎉 Je had {uitkomst}! Je wint 200 coins!")
    else:
        st.sidebar.error(f"😢 Het was {uitkomst}. Probeer het nog eens!")

# Minigame 2: Raad het getal (1-5), win 100 coins
st.sidebar.write("2️⃣ Raad het getal 1-5 (win 100 coins)")
getal = st.sidebar.number_input("Raad het getal:", min_value=1, max_value=5, step=1, key="raad_getal")
if st.sidebar.button("Speel Raad het Getal"):
    random_getal = random.randint(1,5)
    if getal == random_getal:
        st.session_state.coins += 100
        st.sidebar.success(f"🎉 Goed geraden! Het was {random_getal}. Je wint 100 coins!")
    else:
        st.sidebar.error(f"Fout! Het was {random_getal}. Probeer opnieuw!")

# Minigame 3: Dobbelsteen (win 50 coins bij 6)
st.sidebar.write("3️⃣ Dobbelsteen (win 50 coins bij 6)")
if st.sidebar.button("Gooi Dobbelsteen"):
    worp = random.randint(1,6)
    if worp == 6:
        st.session_state.coins += 50
        st.sidebar.success("🎉 Je gooide een 6! Je wint 50 coins!")
    else:
        st.sidebar.info(f"Je gooide een {worp}. Probeer het nog eens!")

st.sidebar.markdown("---")

# --- Packs ---
pack_types = {
    "Bronze Pack (300) - min rating 80": {"prijs": 300, "aantal": 3, "min_rating": 80},
    "Silver Pack (600) - min rating 85": {"prijs": 600, "aantal": 4, "min_rating": 85},
    "Gold Pack (1000) - min rating 88": {"prijs": 1000, "aantal": 5, "min_rating": 88},
    "Rare Pack (1500) - min rating 90": {"prijs": 1500, "aantal": 6, "min_rating": 90},
    "Ultimate Pack (3000) - min rating 93": {"prijs": 3000, "aantal": 7, "min_rating": 93},
}

pack_naam = st.selectbox("Kies een pack", list(pack_types.keys()))

TOTS_KANS = 0.05  # 5% kans op TOTS

if st.button("Koop & Open Pack"):
    prijs = pack_types[pack_naam]["prijs"]
    if st.session_state.coins < prijs:
        st.error("Niet genoeg coins!")
    else:
        st.session_state.coins -= prijs
        # Filter spelers op min rating, geen TOTS pakken hier (komt via kans)
        opties = [p for p in spelers_data if p["rating"] >= pack_types[pack_naam]["min_rating"]]

        gekozen_spelers = []
        max_rating = max(p["rating"] for p in opties) if opties else 100

        while len(gekozen_spelers) < pack_types[pack_naam]["aantal"]:
            # Gewicht: hoe hoger rating, hoe kleiner kans
            kandidaten = []
            gewichten = []
            for p in opties:
                gewicht = max_rating - p["rating"] + 1
                kandidaten.append(p)
                gewichten.append(gewicht)
            gekozen = random.choices(kandidaten, weights=gewichten, k=1)[0]

            # Check TOTS kans
            is_tots = random.random() < TOTS_KANS
            if is_tots:
                speler = {
                    **gekozen,
                    "rating": min(100, gekozen["rating"] + 3),
                    "naam": gekozen["naam"] + " (TOTS)",
                    "type": "TOTS",
                    "is_tots": True,
                    "afbeelding": gekozen["afbeelding"]
                }
            else:
                speler = {**gekozen, "is_tots": False}

            # Check dubbele
            unique_id = maak_unieke_id(speler)
            if unique_id not in st.session_state.gepackte_spelers:
                st.session_state.gepackte_spelers[unique_id] = speler
                gekozen_spelers.append(speler)

        st.subheader("🎁 Je pack bevat:")
        for s in gekozen_spelers:
            kleur = "blue" if s.get("is_tots") else "black"
            st.markdown(f"<span style='color:{kleur}; font-weight:bold'>{s['naam']} ({s['rating']}) - {s['club']}</span>", unsafe_allow_html=True)
            st.image(s["afbeelding"], width=100)

        # TOTS animatie bij minstens 1 TOTS
        if any(s.get("is_tots") for s in gekozen_spelers):
            st.balloons()
            st.success("✨ Je hebt een TOTS speler gepackt! ✨")

# --- Bekijk collectie en reset ---
if st.button("Bekijk mijn collectie"):
    st.subheader("📦 Mijn collectie:")
    if not st.session_state.gepackte_spelers:
        st.write("Je hebt nog geen spelers gepackt.")
    else:
        for uid, speler in st.session_state.gepackte_spelers.items():
            kleur = "blue" if speler.get("is_tots") else "black"
            st.markdown(f"<span style='color:{kleur}; font-weight:bold'>{speler['naam']} ({speler['rating']}) - {speler['club']}</span>", unsafe_allow_html=True)
            st.image(speler["afbeelding"], width=80)
if st.button("Reset mijn collectie"):
    st.session_state.gepackte_spelers = {}
    st.success("Collectie is gereset.")

# --- Welke spelers mis je nog? ---
def maak_unieke_id_ext(speler):
    return f"{speler['naam']}_{speler['club']}"

alle_ids = set(maak_unieke_id_ext(s) for s in spelers_data_ext)
gep_ids = set(st.session_state.gepackte_spelers.keys())
ontbrekend = alle_ids - gep_ids
ontbrekende_spelers = [s for s in spelers_data_ext if maak_unieke_id_ext(s) in ontbrekend]

st.subheader(f"🔍 Ontbrekende spelers: {len(ontbrekende_spelers)}")
for s in ontbrekende_spelers:
    kleur = "blue" if s.get("is_tots") else "black"
    st.markdown(f"<span style='color:{kleur};'>🔒 {s['naam']} ({s['rating']}) - {s['club']}</span>", unsafe_allow_html=True)

# --- Team bouwen ---
st.subheader("⚽ Bouw je team (max 11 spelers)")

beschikbare_spelers = list(st.session_state.gepackte_spelers.values())

if not beschikbare_spelers:
    st.write("Je hebt nog geen spelers om een team te maken.")
else:
    namen = [f"{s['naam']} ({s['rating']})" for s in beschikbare_spelers]
    selectie = st.multiselect("Selecteer spelers voor je team", namen, default=[s['naam']+" ("+str(s['rating'])+")" for s in st.session_state.team])

    # Opslaan geselecteerd team
    if st.button("Sla team op"):
        nieuw_team = []
        naam_rating_map = {f"{s['naam']} ({s['rating']})": s for s in beschikbare_spelers}
        for naam in selectie:
            if naam in naam_rating_map:
                nieuw_team.append(naam_rating_map[naam])
        if len(nieuw_team) > 11:
            st.error("Maximaal 11 spelers in je team!")
        else:
            st.session_state.team = nieuw_team
            st.success("Team opgeslagen!")

    if st.session_state.team:
        st.write("### Jouw team:")
        cols = st.columns(4)
        for i, speler in enumerate(st.session_state.team):
            with cols[i % 4]:
                kleur = "blue" if speler.get("is_tots") else "black"
                st.markdown(f"<span style='color:{kleur}; font-weight:bold'>{speler['naam']} ({speler['rating']})</span>", unsafe_allow_html=True)
                st.image(speler["afbeelding"], width=90)
