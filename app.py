import streamlit as st
import pandas as pd
import random
import datetime

# ---------------------- SPELERSDATA ----------------------
spelers_data = [
    {"naam": "Lionel Messi", "club": "Inter Miami", "rating": 93, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Lionel_Messi_20180626.jpg"},
    {"naam": "Cristiano Ronaldo", "club": "Al Nassr", "rating": 92, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"},
    {"naam": "Erling Haaland", "club": "Manchester City", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Erling_Haaland_Dortmund_2021.jpg"},
    {"naam": "Kylian Mbappé", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Kylian_Mbapp%C3%A9_2019.jpg"},
    {"naam": "Kevin De Bruyne", "club": "Manchester City", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/5/58/Kevin_De_Bruyne_2021.jpg"},
    {"naam": "Luka Modrić", "club": "Real Madrid", "rating": 87, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/5/58/Luka_Modri%C4%87_2018.jpg"},
    {"naam": "Sergio Ramos", "club": "Sevilla FC", "rating": 86, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Sergio_Ramos_2018.jpg"},
    {"naam": "Jude Bellingham", "club": "Real Madrid", "rating": 86, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/d/df/Jude_Bellingham_2020.jpg"},
    {"naam": "Robert Lewandowski", "club": "Barcelona", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Robert_Lewandowski_2019.jpg"},
    {"naam": "Mohamed Salah", "club": "Liverpool", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/9/96/Mohamed_Salah_2018.jpg"},
    # Voeg hier 90 extra spelers toe met dezelfde structuur
]

spelers_df = pd.DataFrame(spelers_data)

# ---------------------- INITIALISATIE ----------------------
if "coins" not in st.session_state:
    st.session_state.coins = 1000
if "gepackte_spelers" not in st.session_state:
    st.session_state.gepackte_spelers = {}
if "laatste_bonus" not in st.session_state:
    st.session_state.laatste_bonus = ""

# ---------------------- UI ----------------------
st.title("🎮 EAFC Pack Opening Game")
st.sidebar.title("🛍️ Shop & Coins")
st.sidebar.write(f"💰 Coins: {st.session_state.coins}")

# Dagelijkse bonus
vandaag = datetime.date.today().isoformat()
if st.sidebar.button("🎁 Dagelijkse Bonus"):
    if st.session_state.laatste_bonus != vandaag:
        st.session_state.coins += 300
        st.sidebar.success("Je hebt 300 coins ontvangen!")
        st.session_state.laatste_bonus = vandaag
    else:
        st.sidebar.warning("Je hebt vandaag al een bonus gekregen.")

# Kop of munt
st.sidebar.markdown("---")
st.sidebar.subheader("🎲 Kop of Munt")
keuze = st.sidebar.radio("Kies:", ["Kop", "Munt"])
if st.sidebar.button("Speel!"):
    uitkomst = random.choice(["Kop", "Munt"])
    if keuze == uitkomst:
        st.session_state.coins += 200
        st.sidebar.success(f"🎉 Het was {uitkomst}! Je wint 200 coins!")
    else:
        st.sidebar.error(f"😢 Het was {uitkomst}. Geen winst.")

# Quizvraag
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Voetbalquiz")
vraag, antwoord = "Wie won het WK in 2018?", "Frankrijk"
antwoord_input = st.sidebar.text_input("Vraag: " + vraag)
if st.sidebar.button("Beantwoord"):
    if antwoord_input.strip().lower() == antwoord.lower():
        st.session_state.coins += 150
        st.sidebar.success("Goed! Je wint 150 coins.")
    else:
        st.sidebar.error("Fout antwoord.")

# ---------------------- PACKS ----------------------
pack_types = {
    "Bronze Pack (200)": {"prijs": 200, "aantal": 2, "min_rating": 75, "tots_kans": 0.01},
    "Silver Pack (500)": {"prijs": 500, "aantal": 3, "min_rating": 78, "tots_kans": 0.03},
    "Gold Pack (1000)": {"prijs": 1000, "aantal": 4, "min_rating": 81, "tots_kans": 0.05},
    "Rare Pack (1500)": {"prijs": 1500, "aantal": 5, "min_rating": 84, "tots_kans": 0.07},
    "Ultimate Pack (2500)": {"prijs": 2500, "aantal": 7, "min_rating": 85, "tots_kans": 0.1},
}

pack_naam = st.selectbox("📦 Kies een pack", list(pack_types.keys()))

if st.button("🧨 Koop & Open Pack"):
    pack = pack_types[pack_naam]
    if st.session_state.coins < pack["prijs"]:
        st.error("Niet genoeg coins!")
    else:
        st.session_state.coins -= pack["prijs"]
        opties = spelers_df[spelers_df["rating"] >= pack["min_rating"]].copy()
        opties["gewicht"] = opties["rating"].apply(lambda r: 100 - r)
        gekozen = opties.sample(n=pack["aantal"], weights=opties["gewicht"], replace=False)

        st.subheader("🎁 Je pack bevat:")
        for _, speler in gekozen.iterrows():
            is_tots = random.random() < pack["tots_kans"]
            naam = speler["naam"] + (" (TOTS)" if is_tots else "")
            rating = speler["rating"] + 3 if is_tots else speler["rating"]
            kleur = "blue" if is_tots else "black"
            unieke_id = speler["naam"] + ("_TOTS" if is_tots else "")

            if unieke_id not in st.session_state.gepackte_spelers:
                st.session_state.gepackte_spelers[unieke_id] = {
                    "naam": naam,
                    "club": speler["club"],
                    "rating": rating,
                    "type": speler["type"],
                    "afbeelding": speler["afbeelding"]
                }

            st.markdown(f"<span style='color:{kleur}'>⭐ {rating} - {naam} ({speler['club']})</span>", unsafe_allow_html=True)
            if speler["afbeelding"]:
                st.image(speler["afbeelding"], width=150)

# ---------------------- VERZAMELING ----------------------
if st.button("📚 Toon Mijn Verzameling"):
    st.subheader("📦 Je verzameling")
    for speler in st.session_state.gepackte_spelers.values():
        kleur = "blue" if "TOTS" in speler["naam"] else "black"
        st.markdown(f"<span style='color:{kleur}'>⭐ {speler['rating']} - {speler['naam']} ({speler['club']})</span>", unsafe_allow_html=True)
        if speler["afbeelding"]:
            st.image(speler["afbeelding"], width=150)

# Reset collectie
if st.button("🗑️ Reset Verzameling"):
    st.session_state.gepackte_spelers = {}
    st.success("Verzameling is gereset!")
