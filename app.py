import streamlit as st
import pandas as pd
import random

# --- Spelersdata met echte afbeeldingen ---
spelers_data = [
    {"naam": "Lionel Messi", "club": "Inter Miami", "rating": 93, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Leo_Messi_WC2022.jpg"},
    {"naam": "Cristiano Ronaldo", "club": "Al Nassr", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"},
    {"naam": "Kylian Mbappé", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Kylian_Mbapp%C3%A9_2019.jpg"},
    {"naam": "Erling Haaland", "club": "Manchester City", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Erling_Haaland_2023.jpg"},
    {"naam": "Kevin De Bruyne", "club": "Manchester City", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Kevin_De_Bruyne_201807091.jpg"},
    {"naam": "Luka Modrić", "club": "Real Madrid", "rating": 87, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/5/58/Luka_Modri%C4%87_2018.jpg"},
    {"naam": "Sergio Ramos", "club": "Sevilla", "rating": 86, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/3/37/Sergio_Ramos_2017.jpg"},
    {"naam": "Mohamed Salah", "club": "Liverpool", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/4/40/Mohamed_Salah_2018.jpg"},
    {"naam": "Neymar Jr", "club": "Al Hilal", "rating": 89, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Neymar_2018.jpg"},
    {"naam": "Robert Lewandowski", "club": "Barcelona", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/5/57/Robert_Lewandowski_2019.jpg"},
    # Voeg hier extra spelers toe...
]

spelers_df = pd.DataFrame(spelers_data)

# --- Init session state ---
if "coins" not in st.session_state:
    st.session_state.coins = 1000
if "gepackte_spelers" not in st.session_state:
    st.session_state.gepackte_spelers = {}
if "team" not in st.session_state:
    st.session_state.team = []
if "message" not in st.session_state:
    st.session_state.message = ""

st.title("🎮 EAFC Pack Opening Game")
st.sidebar.title("🛒 Shop")
st.sidebar.write(f"💰 Coins: {st.session_state.coins}")

# --- Minigame: Kop of Munt ---
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

# --- Packs ---
pack_types = {
    "Gold Pack (500)": {"prijs": 500, "aantal": 3, "types": ["Gold", "Gold Rare"]},
    "Rare Pack (1000)": {"prijs": 1000, "aantal": 5, "types": ["Gold Rare"]},
}
TOTS_KANS = 0.05

st.sidebar.markdown("---")
st.sidebar.subheader("🎁 Packs")
pack_naam = st.sidebar.selectbox("Kies een pack", list(pack_types.keys()))

if st.sidebar.button("Koop & Open Pack"):
    prijs = pack_types[pack_naam]["prijs"]
    if st.session_state.coins >= prijs:
        st.session_state.coins -= prijs
        opties = spelers_df[spelers_df["type"].isin(pack_types[pack_naam]["types"])].copy()
        max_rating = opties["rating"].max()
        opties["gewicht"] = max_rating - opties["rating"] + 1
        gekozen = opties.sample(
            n=pack_types[pack_naam]["aantal"],
            weights=opties["gewicht"],
            replace=False
        )

        st.subheader("📦 Je pack bevat:")
        for _, speler in gekozen.iterrows():
            is_tots = random.random() < TOTS_KANS
            unieke_id = f"{speler['naam']}_TOTS" if is_tots else speler['naam']

            if unieke_id not in st.session_state.gepackte_spelers:
                st.session_state.gepackte_spelers[unieke_id] = {
                    "naam": speler["naam"],
                    "club": speler["club"],
                    "rating": speler["rating"] + 3 if is_tots else speler["rating"],
                    "type": speler["type"] + (" TOTS" if is_tots else ""),
                    "afbeelding": speler["afbeelding"]
                }

            kaart = st.session_state.gepackte_spelers[unieke_id]
            kleur = "blue" if "TOTS" in kaart["type"] else "black"
            st.markdown(f"<span style='color:{kleur}; font-size:18px;'>⭐ {kaart['rating']} - {kaart['naam']} ({kaart['club']}) - {kaart['type']}</span>", unsafe_allow_html=True)
            st.image(kaart["afbeelding"], width=150)
            if "TOTS" in kaart["type"]:
                st.markdown("<h3 style='color:blue;'>✨ TOTS ANIMATIE ✨</h3>", unsafe_allow_html=True)
    else:
        st.error("Niet genoeg coins!")

# --- Verzameling ---
st.markdown("---")
if st.button("📂 Toon verzameling"):
    st.subheader("📦 Gepackte spelers")
    for kaart in st.session_state.gepackte_spelers.values():
        kleur = "blue" if "TOTS" in kaart["type"] else "black"
        st.markdown(f"<span style='color:{kleur}; font-size:16px;'>⭐ {kaart['rating']} - {kaart['naam']} ({kaart['club']}) - {kaart['type']}</span>", unsafe_allow_html=True)
        st.image(kaart["afbeelding"], width=100)

# --- Resetknop ---
if st.button("🔄 Reset verzameling"):
    st.session_state.gepackte_spelers = {}
    st.session_state.team = []
    st.success("Verzameling is gereset!")

# --- Ontbrekende kaarten ---
st.markdown("---")
if st.button("🔍 Toon ontbrekende kaarten"):
    gepackt = {sp["naam"] for sp in st.session_state.gepackte_spelers.values()}
    ontbrekend = [sp for sp in spelers_data if sp["naam"] not in gepackt]
    st.subheader(f"📋 Nog te verzamelen kaarten ({len(ontbrekend)})")
    for speler in ontbrekend:
        st.write(f"🔸 {speler['naam']} ({speler['club']})")

# --- Team builder ---
st.markdown("---")
st.subheader("⚽ Bouw je team")
team = st.session_state.team
keuze_spelers = [sp["naam"] for sp in st.session_state.gepackte_spelers.values() if sp["naam"] not in team]
gekozen = st.selectbox("Kies een speler om toe te voegen aan je team", ["-"] + keuze_spelers)

if gekozen != "-" and len(team) < 11:
    team.append(gekozen)
    st.success(f"✅ {gekozen} toegevoegd aan je team!")

if team:
    st.write(f"👥 Je team ({len(team)}/11):")
    for naam in team:
        st.write(f"- {naam}")

if len(team) >= 11:
    st.success("🎉 Je team is compleet!")
