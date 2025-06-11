import streamlit as st
import pandas as pd
import random

# --- Spelersdata direct in de app.py (voorbeeld met meer spelers) ---
spelers_data = [
    {"naam": "Lionel Messi", "club": "PSG", "rating": 93, "type": "Gold Rare", "afbeelding": "https://cdn.sofifa.org/players/158/023/22_60.png"},
    {"naam": "Cristiano Ronaldo", "club": "Manchester United", "rating": 92, "type": "Gold Rare", "afbeelding": "https://cdn.sofifa.org/players/208/01/22_60.png"},
    {"naam": "Erling Haaland", "club": "Manchester City", "rating": 88, "type": "Gold", "afbeelding": "https://cdn.sofifa.org/players/246/741/22_60.png"},
    {"naam": "Kylian Mbappé", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://cdn.sofifa.org/players/231/747/22_60.png"},
    {"naam": "Kevin De Bruyne", "club": "Manchester City", "rating": 91, "type": "Gold Rare", "afbeelding": "https://cdn.sofifa.org/players/192/985/22_60.png"},
    {"naam": "Neymar Jr", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://cdn.sofifa.org/players/190/871/22_60.png"},
    {"naam": "Robert Lewandowski", "club": "Barcelona", "rating": 91, "type": "Gold Rare", "afbeelding": "https://cdn.sofifa.org/players/188/545/22_60.png"},
    {"naam": "Mohamed Salah", "club": "Liverpool", "rating": 90, "type": "Gold Rare", "afbeelding": "https://cdn.sofifa.org/players/203/376/22_60.png"},
    {"naam": "Luka Modrić", "club": "Real Madrid", "rating": 87, "type": "Gold", "afbeelding": "https://cdn.sofifa.org/players/189/657/22_60.png"},
    {"naam": "Sergio Ramos", "club": "PSG", "rating": 86, "type": "Gold", "afbeelding": "https://cdn.sofifa.org/players/189/561/22_60.png"},
    # Meer spelers toevoegen is hetzelfde patroon
]

spelers_df = pd.DataFrame(spelers_data)

# --- Coins in sessie ---
if "coins" not in st.session_state:
    st.session_state.coins = 1000

# --- Titel ---
st.title("🎮 EAFC Pack Opening Game")

# --- Sidebar: Coins & Minigame ---
st.sidebar.title("🛒 Shop")
st.sidebar.write(f"💰 Coins: {st.session_state.coins}")

st.sidebar.markdown("---")
st.sidebar.subheader("🎲 Minigame: Kop of Munt")

if "message" not in st.session_state:
    st.session_state.message = ""

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

# --- Packs ---
pack_types = {
    "Gold Pack (500)": {"prijs": 500, "aantal": 3, "types": ["Gold", "Gold Rare"]},
    "Rare Pack (1000)": {"prijs": 1000, "aantal": 5, "types": ["Gold Rare", "Inform", "Icon"]},
}

pack_naam = st.sidebar.selectbox("Kies een pack", list(pack_types.keys()))

if st.sidebar.button("Koop & Open Pack"):
    prijs = pack_types[pack_naam]["prijs"]
    if st.session_state.coins >= prijs:
        st.session_state.coins -= prijs
        opties = spelers_df[spelers_df["type"].isin(pack_types[pack_naam]["types"])]
        gekozen = opties.sample(pack_types[pack_naam]["aantal"])
        st.subheader("🎁 Je pack bevat:")
        for _, speler in gekozen.iterrows():
            st.write(f"⭐ {speler['rating']} - {speler['naam']} ({speler['club']}) - {speler['type']}")
            if pd.notna(speler['afbeelding']):
                st.image(speler['afbeelding'], width=150)
    else:
        st.error("Niet genoeg coins!")
