import streamlit as st
import pandas as pd
import random

# --- Spelersdata met openbare, betrouwbare afbeelding URL's ---
spelers_data = [
    {"naam": "Lionel Messi", "club": "PSG", "rating": 93, "type": "Gold Rare",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/89/Lionel_Messi_20180626.jpg"},
    {"naam": "Cristiano Ronaldo", "club": "Manchester United", "rating": 92, "type": "Gold Rare",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"},
    {"naam": "Erling Haaland", "club": "Manchester City", "rating": 88, "type": "Gold",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Erling_Haaland_2022.jpg"},
    {"naam": "Kylian Mbappé", "club": "PSG", "rating": 91, "type": "Gold Rare",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/a/ae/Kylian_Mbapp%C3%A9_2021.jpg"},
    {"naam": "Kevin De Bruyne", "club": "Manchester City", "rating": 91, "type": "Gold Rare",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Kevin_De_Bruyne_201807091.jpg"},
    {"naam": "Neymar Jr", "club": "PSG", "rating": 91, "type": "Gold Rare",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Neymar_2018.jpg"},
    {"naam": "Robert Lewandowski", "club": "Barcelona", "rating": 91, "type": "Gold Rare",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/d/dd/Robert_Lewandowski_2020.jpg"},
    {"naam": "Mohamed Salah", "club": "Liverpool", "rating": 90, "type": "Gold Rare",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Mohamed_Salah_2020.jpg"},
    {"naam": "Luka Modrić", "club": "Real Madrid", "rating": 87, "type": "Gold",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Luka_Modrić_2018.jpg"},
    {"naam": "Sergio Ramos", "club": "PSG", "rating": 86, "type": "Gold",
     "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Sergio_Ramos_2019.jpg"},
    # Voeg gerust meer spelers toe in dit formaat
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
