import streamlit as st
import pandas as pd
import random

# --- Spelersdata met echte afbeeldingen ---
spelers_data = [
    {"naam": "Lionel Messi", "club": "Inter Miami", "rating": 93, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/89/Lionel_Messi_20180626.jpg"},
    {"naam": "Cristiano Ronaldo", "club": "Al-Nassr", "rating": 92, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"},
    {"naam": "Kylian Mbappé", "club": "PSG", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Kylian_Mbapp%C3%A9_2019.jpg"},
    {"naam": "Erling Haaland", "club": "Manchester City", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/5/55/Erling_Haaland_2021.jpg"},
    {"naam": "Kevin De Bruyne", "club": "Manchester City", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Kevin_De_Bruyne_201807091.jpg"},
    {"naam": "Robert Lewandowski", "club": "Barcelona", "rating": 91, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Robert_Lewandowski_2020.jpg"},
    {"naam": "Mohamed Salah", "club": "Liverpool", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/f/fd/Mohamed_Salah_2018.jpg"},
    {"naam": "Neymar Jr", "club": "Al Hilal", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Neymar_in_2018.jpg"},
    {"naam": "Karim Benzema", "club": "Al-Ittihad", "rating": 89, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Karim_Benzema_2018.jpg"},
    {"naam": "Harry Kane", "club": "Bayern München", "rating": 90, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/89/Harry_Kane_2018.jpg"},
    {"naam": "Luka Modrić", "club": "Real Madrid", "rating": 87, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Luka_Modri%C4%87_2018.jpg"},
    {"naam": "Sergio Ramos", "club": "Sevilla", "rating": 85, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/8f/Sergio_Ramos_2017.jpg"},
    {"naam": "Thibaut Courtois", "club": "Real Madrid", "rating": 89, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Thibaut_Courtois_2018.jpg"},
    {"naam": "Virgil van Dijk", "club": "Liverpool", "rating": 89, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/1/10/Virgil_van_Dijk_2018.jpg"},
    {"naam": "Marc-André ter Stegen", "club": "Barcelona", "rating": 88, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Marc-Andr%C3%A9_ter_Stegen_2018.jpg"},
    {"naam": "Joshua Kimmich", "club": "Bayern München", "rating": 88, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Joshua_Kimmich_2019.jpg"},
    {"naam": "Jude Bellingham", "club": "Real Madrid", "rating": 86, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/c/cd/Jude_Bellingham_2020.jpg"},
    {"naam": "Phil Foden", "club": "Manchester City", "rating": 85, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Phil_Foden_2021.jpg"},
    {"naam": "Vinícius Jr", "club": "Real Madrid", "rating": 86, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/f/fb/Vin%C3%ADcius_J%C3%BAnior_2021.jpg"},
    {"naam": "Pedri", "club": "Barcelona", "rating": 85, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/1/17/Pedri_2021.jpg"},
    {"naam": "João Félix", "club": "Barcelona", "rating": 84, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Jo%C3%A3o_F%C3%A9lix_2019.jpg"},
    {"naam": "Antoine Griezmann", "club": "Atlético Madrid", "rating": 86, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/7/7d/Antoine_Griezmann_2018.jpg"},
    {"naam": "Frenkie de Jong", "club": "Barcelona", "rating": 86, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Frenkie_de_Jong_2019.jpg"},
    {"naam": "Mason Mount", "club": "Manchester United", "rating": 83, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Mason_Mount_2020.jpg"},
    {"naam": "Bruno Fernandes", "club": "Manchester United", "rating": 87, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Bruno_Fernandes_2020.jpg"},
    {"naam": "Jadon Sancho", "club": "Manchester United", "rating": 84, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Jadon_Sancho_2020.jpg"},
    {"naam": "Casemiro", "club": "Manchester United", "rating": 88, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/4/44/Casemiro_2018.jpg"},
    {"naam": "Bernardo Silva", "club": "Manchester City", "rating": 88, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/7/75/Bernardo_Silva_2018.jpg"},
    {"naam": "Kai Havertz", "club": "Arsenal", "rating": 84, "type": "Gold", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Kai_Havertz_2020.jpg"},
    {"naam": "Bukayo Saka", "club": "Arsenal", "rating": 85, "type": "Gold Rare", "afbeelding": "https://upload.wikimedia.org/wikipedia/commons/6/65/Bukayo_Saka_2021.jpg"},
    # Voeg hier gerust nog 70 spelers toe in ditzelfde formaat...
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
