import streamlit as st
import random

# --- Spelerslijst (voorbeeld met 15 spelers, jij voegt er 100+ aan toe) ---
spelers_data = [
    {"naam": "Lionel Messi", "club": "PSG", "rating": 93, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Lionel_Messi_20180626.jpg/120px-Lionel_Messi_20180626.jpg"},
    {"naam": "Cristiano Ronaldo", "club": "Manchester United", "rating": 92, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cristiano_Ronaldo_2018.jpg/120px-Cristiano_Ronaldo_2018.jpg"},
    {"naam": "Erling Haaland", "club": "Manchester City", "rating": 88, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Erling_Haaland_2020.jpg/120px-Erling_Haaland_2020.jpg"},
    {"naam": "Kylian Mbappé", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Kylian_Mbapp%C3%A9_2020.jpg/120px-Kylian_Mbapp%C3%A9_2020.jpg"},
    {"naam": "Kevin De Bruyne", "club": "Manchester City", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Kevin_De_Bruyne_201807091.jpg/120px-Kevin_De_Bruyne_201807091.jpg"},
    {"naam": "Neymar Jr", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Neymar_2018.jpg/120px-Neymar_2018.jpg"},
    {"naam": "Robert Lewandowski", "club": "Barcelona", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Robert_Lewandowski_2020.jpg/120px-Robert_Lewandowski_2020.jpg"},
    {"naam": "Mohamed Salah", "club": "Liverpool", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Mohamed_Salah_2018.jpg/120px-Mohamed_Salah_2018.jpg"},
    {"naam": "Luka Modrić", "club": "Real Madrid", "rating": 87, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Luka_Modric_2018.jpg/120px-Luka_Modric_2018.jpg"},
    {"naam": "Sergio Ramos", "club": "PSG", "rating": 86, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Sergio_Ramos_2017.jpg/120px-Sergio_Ramos_2017.jpg"},
    {"naam": "Icon Pele", "club": "Retired", "rating": 98, "type": "Icon", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Pele_in_1960.jpg/120px-Pele_in_1960.jpg"},
    {"naam": "Icon Maradona", "club": "Retired", "rating": 97, "type": "Icon", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Diego_Maradona_1990.jpg/120px-Diego_Maradona_1990.jpg"},
    {"naam": "Inform De Bruyne", "club": "Manchester City", "rating": 92, "type": "Inform", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Kevin_De_Bruyne_2019.jpg/120px-Kevin_De_Bruyne_2019.jpg"},
    {"naam": "Inform Haaland", "club": "Manchester City", "rating": 89, "type": "Inform", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Erling_Haaland_2021.jpg/120px-Erling_Haaland_2021.jpg"},
    {"naam": "TOTS Messi", "club": "PSG", "rating": 96, "type": "TOTS", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Lionel_Messi_2019.jpg/120px-Lionel_Messi_2019.jpg"},
    # Voeg hier je 100+ spelers toe met echte Wikipedia-afbeeldingen
]

# --- Initialiseer sessie variabelen ---
if "coins" not in st.session_state:
    st.session_state.coins = 1000
if "message" not in st.session_state:
    st.session_state.message = ""
if "gepackte_spelers" not in st.session_state:
    st.session_state.gepackte_spelers = {}
if "team" not in st.session_state:
    st.session_state.team = []

# --- Packs definities ---
pack_types = {
    "Bronze Pack": {"prijs": 200, "aantal": 3, "min_rating": 70, "types": ["Gold", "Gold Rare", "Inform", "Icon", "TOTS"]},
    "Silver Pack": {"prijs": 500, "aantal": 5, "min_rating": 80, "types": ["Gold", "Gold Rare", "Inform", "Icon", "TOTS"]},
    "Gold Pack": {"prijs": 1000, "aantal": 7, "min_rating": 85, "types": ["Gold", "Gold Rare", "Inform", "Icon", "TOTS"]},
    "Rare Pack": {"prijs": 1500, "aantal": 10, "min_rating": 88, "types": ["Gold Rare", "Inform", "Icon", "TOTS"]},
    "Ultimate Pack": {"prijs": 3000, "aantal": 12, "min_rating": 90, "types": ["Gold Rare", "Inform", "Icon", "TOTS"]},
}

TOTS_KANS = 0.05

# --- Functie voor pack openen, snel en netjes ---
def open_pack(pack_info):
    opties = [p.copy() for p in spelers_data if p['rating'] >= pack_info['min_rating'] and p['type'] in pack_info['types']]

    aantal = min(pack_info['aantal'], len(opties))
    gekozen = random.sample(opties, aantal)

    for speler in gekozen:
        # TOTS kans check
        if random.random() < TOTS_KANS and speler['type'] != "TOTS":
            speler['rating'] = min(100, speler['rating'] + 3)
            speler['naam'] += " (TOTS)"
            speler['type'] = "TOTS"
            speler['is_tots'] = True
        else:
            speler['is_tots'] = (speler['type'] == "TOTS")
    return gekozen

# --- Streamlit UI ---

st.title("🎮 EAFC Pack Opening Game")

# Coins en shop
st.sidebar.title("🛒 Shop")
st.sidebar.write(f"💰 Coins: {st.session_state.coins}")

# Minigame: Kop of Munt
st.sidebar.markdown("---")
st.sidebar.subheader("🎲 Minigame: Kop of Munt")

keuze = st.sidebar.radio("Kies Kop of Munt:", ["Kop", "Munt"])
if st.sidebar.button("Speel"):
    uitkomst = random.choice(["Kop", "Munt"])
    if keuze == uitkomst:
        winst = 200
        st.session_state.coins += winst
        st.session_state.message = f"🎉 Je had {uitkomst}! Je wint {winst} coins!"
    else:
        st.session_state.message = f"😢 Het was {uitkomst}. Probeer het nog eens!"

st.sidebar.write(st.session_state.message)

# Coins verdienen extra manier
st.sidebar.markdown("---")
st.sidebar.subheader("💰 Coins verdienen")
if st.sidebar.button("Dagelijkse bonus +500 coins"):
    st.session_state.coins += 500
    st.sidebar.success("Bonus coins toegevoegd!")

# Kies pack
st.sidebar.markdown("---")
st.sidebar.subheader("📦 Kies een pack")
pack_naam = st.sidebar.selectbox("Kies een pack", list(pack_types.keys()))

if st.sidebar.button("Koop & Open Pack"):
    prijs = pack_types[pack_naam]["prijs"]
    if st.session_state.coins >= prijs:
        st.session_state.coins -= prijs
        nieuw_gepakt = open_pack(pack_types[pack_naam])

        st.subheader("🎁 Je pack bevat:")
        for speler in nieuw_gepakt:
            unieke_id = speler['naam'] + "_" + speler['club']
            if unieke_id not in st.session_state.gepackte_spelers:
                st.session_state.gepackte_spelers[unieke_id] = speler

            kleur_naam = "blue" if speler.get('is_tots') else "black"
            st.markdown(f"<span style='color:{kleur_naam};'>⭐ {speler['rating']} - {speler['naam']} ({speler['club']}) - {speler['type']}</span>", unsafe_allow_html=True)
            st.image(speler['afbeelding'], width=120)
    else:
        st.error("Niet genoeg coins!")

# Toon gepackte spelers knop
if st.button("Toon mijn verzameling"):
    st.subheader("📚 Mijn verzamelde spelers (dubbele tellen niet mee):")
    if st.session_state.gepackte_spelers:
        for speler in st.session_state.gepackte_spelers.values():
            kleur_naam = "blue" if speler.get('is_tots') else "black"
            st.markdown(f"<span style='color:{kleur_naam};'>⭐ {speler['rating']} - {speler['naam']} ({speler['club']}) - {speler['type']}</span>", unsafe_allow_html=True)
            st.image(speler['afbeelding'], width=100)
    else:
        st.info("Je hebt nog geen spelers gepackt.")

# Reset verzameling knop
if st.button("Reset verzameling"):
    st.session_state.gepackte_spelers = {}
    st.success("Je verzameling is gereset!")

# Toon missen (alle spelers die je nog niet hebt, incl. TOTS versies)
if st.button("Toon welke spelers je mist"):
    st.subheader("❌ Spelers die je nog moet verzamelen:")
    gemist = []
    # Vergelijk op naam en type (bijv. ook TOTS variant apart)
    alle_ids = {sp['naam'] + "_" + sp['club'] for sp in spelers_data}
    verzameld_ids = set(st.session_state.gepackte_spelers.keys())
    for speler in spelers_data:
        unieke_id = speler['naam'] + "_" + speler['club']
        if unieke_id not in verzameld_ids:
            gemist.append(speler)
    if gemist:
        for sp in gemist:
            kleur_naam = "blue" if sp.get('type') == "TOTS" else "black"
            st.markdown(f"<span style='color:{kleur_naam};'>⭐ {sp['rating']} - {sp['naam']} ({sp['club']}) - {sp['type']}</span>", unsafe_allow_html=True)
            st.image(sp['afbeelding'], width=100)
    else:
        st.success("Gefeliciteerd, je hebt alle spelers!")

# Team bouwen
st.markdown("---")
st.subheader("🏆 Bouw je eigen team (max 11 spelers)")
beschikbare_spelers = list(st.session_state.gepackte_spelers.values())

team_keuze = st.multiselect("Selecteer spelers voor je team:", options=[f"{p['naam']} ({p['club']})" for p in beschikbare_spelers])

# Update team in session_state
nieuw_team = []
for sel in team_keuze:
    naam = sel.split(" (")[0]
    for p in beschikbare_spelers:
        if p['naam'] == naam and p not in nieuw_team:
            nieuw_team.append(p)

st.session_state.team = nieuw_team

if st.session_state.team:
    st.write(f"Je team ({len(st.session_state.team)}/11):")
    for speler in st.session_state.team:
        kleur_naam = "blue" if speler.get('is_tots') else "black"
        st.markdown(f"<span style='color:{kleur_naam};'>⭐ {speler['rating']} - {speler['naam']} ({speler['club']})</span>", unsafe_allow_html=True)
        st.image(speler['afbeelding'], width=100)
else:
    st.info("Selecteer spelers om je team te bouwen.")

# Animatie bij TOTS krijgen (eenvoudige streamlit animatie met ballen)
if st.session_state.message and "TOTS" in st.session_state.message:
    st.balloons()

