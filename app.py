import streamlit as st
import pandas as pd
import random

# DATA INLADEN
@st.cache_data
def load_spelers():
    return pd.read_csv("spelers.csv", encoding="utf-8-sig")


spelers_df = load_spelers()

# MUNTEN
if "coins" not in st.session_state:
    st.session_state.coins = 1000  # Begin met 1000 coins

# TITEL
st.title("🎮 EAFC Pack Opening Game")

# SHOP
st.sidebar.title("🛒 Shop")
st.sidebar.write(f"💰 Coins: {st.session_state.coins}")

# PACK TYPE
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
