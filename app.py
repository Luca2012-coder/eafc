import streamlit as st
import pandas as pd
import random

# SPELERSDATA direct in de code (geen extern CSV nodig)
@st.cache_data
def load_spelers():
    data = {
        "naam": ["Mbappe", "Messi", "Ronaldo", "Bellingham", "Haaland", "De Bruyne"],
        "rating": [91, 90, 88, 86, 91, 91],
        "club": ["PSG", "Inter Miami", "Al Nassr", "Real Madrid", "Manchester City", "Manchester City"],
        "positie": ["ST", "RW", "ST", "CM", "ST", "CM"],
        "type": ["Gold Rare", "Gold Rare", "Gold Rare", "Gold", "Gold Rare", "Gold Rare"],
        "afbeelding": [
            "https://cdn.sofifa.net/players/231/747/24_120.png",
            "https://cdn.sofifa.net/players/158/023/24_120.png",
            "https://cdn.sofifa.net/players/020/801/24_120.png",
            "https://cdn.sofifa.net/players/243/812/24_120.png",
            "https://cdn.sofifa.net/players/239/085/24_120.png",
            "https://cdn.sofifa.net/players/192/985/24_120.png"
        ]
    }
    return pd.DataFrame(data)

# Laden van spelersdata
spelers_df = load_spelers()

# MUNTEN bijhouden in sessiestate
if "coins" not in st.session_state:
    st.session_state.coins = 1000  # Start met 1000 coins

# TITEL
st.title("🎮 EAFC Pack Opening Game")

# SHOP (sidebar)
st.sidebar.title("🛒 Shop")
st.sidebar.write(f"💰 Coins: {st.session_state.coins}")

# PACK TYPES met prijzen, aantal kaarten en toegestane types
pack_types = {
    "Gold Pack (500)": {"prijs": 500, "aantal": 3, "types": ["Gold", "Gold Rare"]},
    "Rare Pack (1000)": {"prijs": 1000, "aantal": 5, "types": ["Gold Rare", "Inform", "Icon"]},
}

pack_naam = st.sidebar.selectbox("Kies een pack", list(pack_types.keys()))

# Pack openen
if st.sidebar.button("Koop & Open Pack"):
    prijs = pack_types[pack_naam]["prijs"]
    if st.session_state.coins >= prijs:
        st.session_state.coins -= prijs
        opties = spelers_df[spelers_df["type"].isin(pack_types[pack_naam]["types"])]

        # Pak willekeurig aantal spelers
        gekozen = opties.sample(pack_types[pack_naam]["aantal"])

        st.subheader("🎁 Je pack bevat:")
        for _, speler in gekozen.iterrows():
            st.write(f"⭐ {speler['rating']} - {speler['naam']} ({speler['club']}) - {speler['type']}")
            if pd.notna(speler['afbeelding']):
                st.image(speler['afbeelding'], width=150)
    else:
        st.error("Niet genoeg coins!")

