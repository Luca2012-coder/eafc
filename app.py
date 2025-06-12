import streamlit as st
import pandas as pd
import random
import time

# --- SPELERSDATA (voorbeeld: eerste 10, jij kan uitbreiden tot 100) ---
spelers_data = [
    {"naam": "Lionel Messi", "club": "Inter Miami", "rating": 93, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/89/Lionel_Messi_20180626.jpg"},
    {"naam": "Cristiano Ronaldo", "club": "Al-Nassr", "rating": 92, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"},
    {"naam": "Kylian Mbappé", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Kylian_Mbapp%C3%A9_2019.jpg"},
    {"naam": "Kevin De Bruyne", "club": "Manchester City", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Kevin_De_Bruyne_2021.jpg"},
    {"naam": "Erling Haaland", "club": "Manchester City", "rating": 90, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Erling_Haaland_2022.jpg"},
    {"naam": "Luka Modrić", "club": "Real Madrid", "rating": 88, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/6/63/Luka_Modri%C4%87_2018.jpg"},
    {"naam": "Sergio Ramos", "club": "Sevilla", "rating": 86, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Sergio_Ramos_2017.jpg"},
    {"naam": "Neymar Jr", "club": "Al-Hilal", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Neymar_WC2018.jpg"},
    {"naam": "Mohamed Salah", "club": "Liverpool", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Mohamed_Salah_2018.jpg"},
    {"naam": "Robert Lewandowski", "club": "Barcelona", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/5/59/Lewandowski-Bayern-2020.jpg"},
    # Voeg hier nog 90 spelers toe in hetzelfde formaat
]

spelers_df = pd.DataFrame(spelers_data)

# --- INITIËLE STATUS ---
if "coins" not in st.session_state:
    st.session_state.coins = 1000
if "gepackte_spelers" not in st.session_state:
    st.session_state.gepackte_spelers = {}
if "message" not in st.session_state:
    st.session_state.message = ""

# --- TITEL ---
st.title("🎮 EAFC Pack Opening Game")

# --- SIDEBAR ---
st.sidebar.title("🛒 Shop")
st.sidebar.write(f"💰 Coins: {st.session_state.coins}")

# Minigame
st.sidebar.markdown("---")
st.sidebar.subheader("🎲 Minigame: Kop of Munt")
keuze = st.sidebar.radio("Kies:", ["Kop", "Munt"])
if st.sidebar.button("Speel"):
    uitkomst = random.choice(["Kop", "Munt"])
    if keuze == uitkomst:
        st.session_state.coins += 200
        st.session_state.message = f"🎉 Het was {uitkomst}! Je wint 200 coins."
    else:
        st.session_state.message = f"😢 Het was {uitkomst}. Geen winst."
st.sidebar.write(st.session_state.message)

# Packs
pack_types = {
    "Gold Pack (500)": {"prijs": 500, "aantal": 3, "types": ["Gold", "Gold Rare"]},
    "Rare Pack (1000)": {"prijs": 1000, "aantal": 5, "types": ["Gold Rare"]},
}

pack_naam = st.sidebar.selectbox("Kies een pack", list(pack_types.keys()))
TOTS_KANS = 0.05

# --- PACK OPENEN ---
if st.sidebar.button("Koop & Open Pack"):
    prijs = pack_types[pack_naam]["prijs"]
    if st.session_state.coins >= prijs:
        st.session_state.coins -= prijs
        opties = spelers_df[spelers_df["type"].isin(pack_types[pack_naam]["types"])].copy()
        opties["gewicht"] = opties["rating"].apply(lambda r: max(1, 100 - r))  # hoe hoger, hoe zeldzamer
        gekozen = opties.sample(n=pack_types[pack_naam]["aantal"], weights=opties["gewicht"])

        st.subheader("🎁 Je pack bevat:")
        for _, speler in gekozen.iterrows():
            unieke_id = speler['naam']
            is_tots = random.random() < TOTS_KANS
            rating = speler['rating'] + 3 if is_tots else speler['rating']
            naam = f"{speler['naam']} (TOTS)" if is_tots else speler['naam']
            kleur = "blue" if is_tots else "black"

            # TOTS animatie
            if is_tots:
                with st.spinner("✨ Je hebt een TOTS..."):
                    time.sleep(1)

            st.markdown(f"<span style='color:{kleur};'>⭐ {rating} - {naam} ({speler['club']})</span>", unsafe_allow_html=True)
            if pd.notna(speler["afbeelding"]):
                st.image(speler["afbeelding"], width=150)

            # Toevoegen aan collectie
            if unieke_id not in st.session_state.gepackte_spelers:
                st.session_state.gepackte_spelers[unieke_id] = {
                    "naam": naam,
                    "club": speler["club"],
                    "rating": rating,
                    "afbeelding": speler["afbeelding"],
                    "is_tots": is_tots
                }
    else:
        st.error("Niet genoeg coins!")

# --- GEPAACKTE SPELERS TONEN ---
if st.button("📦 Toon Mijn Verzameling"):
    verzameling = st.session_state.gepackte_spelers
    st.subheader(f"📋 Verzameling ({len(verzameling)} / {len(spelers_df)})")
    for speler in verzameling.values():
        kleur = "blue" if speler["is_tots"] else "black"
        st.markdown(f"<span style='color:{kleur};'>⭐ {speler['rating']} - {speler['naam']} ({speler['club']})</span>", unsafe_allow_html=True)
        if speler["afbeelding"]:
            st.image(speler["afbeelding"], width=150)

# --- RESETKNOP ---
if st.button("❌ Reset mijn verzameling"):
    st.session_state.gepackte_spelers = {}
    st.success("Je verzameling is gereset!")

# --- NOG TE VERZAMELEN ---
if st.button("🔍 Wat mis ik nog?"):
    gepackte_namen = set(st.session_state.gepackte_spelers.keys())
    ontbrekend = spelers_df[~spelers_df["naam"].isin(gepackte_namen)]
    st.subheader(f"📉 Nog te verzamelen: {len(ontbrekend)} kaarten")
    for _, speler in ontbrekend.iterrows():
        st.write(f"🔲 {speler['naam']} ({speler['club']})")
