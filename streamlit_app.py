import streamlit as st
import pandas as pd
import random
import json
import os

st.set_page_config(page_title="Copa do Mundo FIFA 2026", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0a0a0a; }
    h1, h2, h3 { color: #f0f0f0 !important; }
    .grupo-card {
        background: #1a1a2e;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .standings-table {
        font-size: 14px;
        width: 100%;
        border-collapse: collapse;
    }
    .standings-table th { background: #16213e; color: #aaa; padding: 6px 8px; text-align: center; font-weight: 500; }
    .standings-table td { padding: 6px 8px; text-align: center; border-bottom: 1px solid #2a2a3e; }
    .standings-table tr:nth-child(1) td { background: #0a3d2e; }
    .standings-table tr:nth-child(2) td { background: #0a3d2e; }
    .standings-table td:first-child { text-align: left; font-weight: 600; }
    .match-row {
        display: flex; align-items: center; gap: 8px;
        padding: 6px 0; border-bottom: 1px solid #2a2a3e;
    }
    .match-row .team { min-width: 120px; font-size: 14px; color: #ddd; }
    .match-row .vs { color: #666; font-size: 12px; }
    .match-row input { width: 40px; text-align: center; }
    .qualified { color: #4ade80; font-weight: 700; }
    .eliminated { color: #f87171; font-weight: 600; }
    .third-contention { color: #fbbf24; font-weight: 600; }
    .badge-green { background: #166534; color: #bbf7d0; padding: 2px 10px; border-radius: 20px; font-size: 12px; }
    .badge-yellow { background: #854d0e; color: #fef08a; padding: 2px 10px; border-radius: 20px; font-size: 12px; }
    .badge-red { background: #991b1b; color: #fecaca; padding: 2px 10px; border-radius: 20px; font-size: 12px; }
    .bracket { font-family: monospace; }
    div[data-testid="stNumberInput"] label { display: none; }
    div[data-testid="stNumberInput"] input { font-size: 16px !important; font-weight: 700 !important; }
    .stButton button { background: #1e3a5f; color: white; border: none; }
    .stButton button:hover { background: #2a4a7f; }
    .match-date { color: #888; font-size: 11px; min-width: 38px; }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; }
    .stTabs [data-baseweb="tab"] { background: #1a1a2e; border-radius: 8px 8px 0 0 !important; padding: 8px 16px; color: #aaa; }
    .stTabs [aria-selected="true"] { background: #16213e; color: #fff !important; }
    .knockout-win { color: #4ade80; font-weight: 700; }
    .knockout-loss { color: #f87171; }
</style>
""", unsafe_allow_html=True)

FLAGS = {
    "México": "🇲🇽", "África do Sul": "🇿🇦", "Coreia do Sul": "🇰🇷", "República Tcheca": "🇨🇿",
    "Canadá": "🇨🇦", "Bósnia e Herzegovina": "🇧🇦", "Catar": "🇶🇦", "Suíça": "🇨🇭",
    "Brasil": "🇧🇷", "Marrocos": "🇲🇦", "Haiti": "🇭🇹", "Escócia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Estados Unidos": "🇺🇸", "Paraguai": "🇵🇾", "Austrália": "🇦🇺", "Turquia": "🇹🇷",
    "Alemanha": "🇩🇪", "Curaçao": "🇨🇼", "Costa do Marfim": "🇨🇮", "Equador": "🇪🇨",
    "Holanda": "🇳🇱", "Japão": "🇯🇵", "Suécia": "🇸🇪", "Tunísia": "🇹🇳",
    "Bélgica": "🇧🇪", "Egito": "🇪🇬", "Irã": "🇮🇷", "Nova Zelândia": "🇳🇿",
    "Espanha": "🇪🇸", "Cabo Verde": "🇨🇻", "Arábia Saudita": "🇸🇦", "Uruguai": "🇺🇾",
    "França": "🇫🇷", "Senegal": "🇸🇳", "Iraque": "🇮🇶", "Noruega": "🇳🇴",
    "Argentina": "🇦🇷", "Argélia": "🇩🇿", "Áustria": "🇦🇹", "Jordânia": "🇯🇴",
    "Portugal": "🇵🇹", "RD Congo": "🇨🇩", "Uzbequistão": "🇺🇿", "Colômbia": "🇨🇴",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croácia": "🇭🇷", "Gana": "🇬🇭", "Panamá": "🇵🇦",
}

GROUPS = {
    "A": { "teams": ["México", "África do Sul", "Coreia do Sul", "República Tcheca"] },
    "B": { "teams": ["Canadá", "Bósnia e Herzegovina", "Catar", "Suíça"] },
    "C": { "teams": ["Brasil", "Marrocos", "Haiti", "Escócia"] },
    "D": { "teams": ["Estados Unidos", "Paraguai", "Austrália", "Turquia"] },
    "E": { "teams": ["Alemanha", "Curaçao", "Costa do Marfim", "Equador"] },
    "F": { "teams": ["Holanda", "Japão", "Suécia", "Tunísia"] },
    "G": { "teams": ["Bélgica", "Egito", "Irã", "Nova Zelândia"] },
    "H": { "teams": ["Espanha", "Cabo Verde", "Arábia Saudita", "Uruguai"] },
    "I": { "teams": ["França", "Senegal", "Iraque", "Noruega"] },
    "J": { "teams": ["Argentina", "Argélia", "Áustria", "Jordânia"] },
    "K": { "teams": ["Portugal", "RD Congo", "Uzbequistão", "Colômbia"] },
    "L": { "teams": ["Inglaterra", "Croácia", "Gana", "Panamá"] },
}

MATCH_ROUNDS = {
    "A": ["11/06", "11/06", "18/06", "18/06", "24/06", "24/06"],
    "B": ["12/06", "13/06", "18/06", "18/06", "24/06", "24/06"],
    "C": ["13/06", "13/06", "19/06", "19/06", "24/06", "24/06"],
    "D": ["12/06", "13/06", "19/06", "19/06", "25/06", "25/06"],
    "E": ["14/06", "14/06", "20/06", "20/06", "25/06", "25/06"],
    "F": ["14/06", "14/06", "20/06", "21/06", "25/06", "25/06"],
    "G": ["15/06", "15/06", "21/06", "21/06", "26/06", "26/06"],
    "H": ["15/06", "15/06", "21/06", "21/06", "26/06", "26/06"],
    "I": ["16/06", "16/06", "22/06", "22/06", "26/06", "26/06"],
    "J": ["16/06", "17/06", "22/06", "23/06", "27/06", "27/06"],
    "K": ["17/06", "17/06", "23/06", "23/06", "27/06", "27/06"],
    "L": ["17/06", "17/06", "23/06", "23/06", "27/06", "27/06"],
}

for grp in GROUPS:
    t = GROUPS[grp]["teams"]
    GROUPS[grp]["matches"] = [
        (t[0], t[1]), (t[2], t[3]),
        (t[0], t[2]), (t[1], t[3]),
        (t[0], t[3]), (t[1], t[2]),
    ]

SALVAR_PATH = os.path.join(os.path.dirname(__file__), "resultados_copa2026.json")

if "results" not in st.session_state:
    st.session_state.results = {}
    for grp in GROUPS:
        for i in range(6):
            st.session_state.results[f"{grp}_{i}"] = None
    if os.path.exists(SALVAR_PATH):
        try:
            with open(SALVAR_PATH) as f:
                carregar_resultados(f.read())
        except Exception:
            pass

if "knockout" not in st.session_state:
    st.session_state.knockout = {}

def flag(t):
    return f"{FLAGS.get(t, '')} {t}"

def get_standings(grp):
    teams = GROUPS[grp]["teams"]
    s = {t: {"P": 0, "J": 0, "V": 0, "E": 0, "D": 0, "GP": 0, "GC": 0, "SG": 0} for t in teams}
    for i, (h, a) in enumerate(GROUPS[grp]["matches"]):
        r = st.session_state.results.get(f"{grp}_{i}")
        if r is not None:
            gh, ga = r
            s[h]["J"] += 1; s[a]["J"] += 1
            s[h]["GP"] += gh; s[h]["GC"] += ga
            s[a]["GP"] += ga; s[a]["GC"] += gh
            if gh > ga:
                s[h]["V"] += 1; s[a]["D"] += 1; s[h]["P"] += 3
            elif ga > gh:
                s[a]["V"] += 1; s[h]["D"] += 1; s[a]["P"] += 3
            else:
                s[h]["E"] += 1; s[a]["E"] += 1; s[h]["P"] += 1; s[a]["P"] += 1
    for t in s:
        s[t]["SG"] = s[t]["GP"] - s[t]["GC"]
    def sort_key(t):
        return (s[t]["P"], s[t]["SG"], s[t]["GP"])
    sorted_teams = sorted(teams, key=sort_key, reverse=True)
    return s, sorted_teams

def get_group_table(grp):
    stats, ordered = get_standings(grp)
    rows = []
    for i, t in enumerate(ordered, 1):
        rows.append({
            "POS": i, "TIME": flag(t),
            "P": stats[t]["P"], "J": stats[t]["J"],
            "V": stats[t]["V"], "E": stats[t]["E"], "D": stats[t]["D"],
            "GP": stats[t]["GP"], "GC": stats[t]["GC"], "SG": stats[t]["SG"]
        })
    return pd.DataFrame(rows)

def get_third_placed_ranking():
    entries = []
    for grp in sorted(GROUPS.keys()):
        stats, ordered = get_standings(grp)
        t3 = ordered[2]
        entries.append((grp, t3, stats[t3]["P"], stats[t3]["SG"], stats[t3]["GP"], stats[t3]["J"]))
    entries.sort(key=lambda x: (x[2], x[3], x[4]), reverse=True)
    return entries

def random_score():
    w = [0.25, 0.35, 0.22, 0.12, 0.06]
    return random.choices(range(5), weights=w)[0]

def simulate_all():
    for grp in GROUPS:
        for i in range(6):
            gh, ga = random_score(), random_score()
            if gh == ga == 0 and random.random() < 0.3:
                gh, ga = 1, 0
            st.session_state.results[f"{grp}_{i}"] = (gh, ga)
    st.session_state.knockout = {}

def reset_all():
    for grp in GROUPS:
        for i in range(6):
            st.session_state.results[f"{grp}_{i}"] = None
    st.session_state.knockout = {}

def serializar_resultados():
    data = {}
    data["results"] = {k: list(v) for k, v in st.session_state.results.items() if v is not None}
    data["knockout"] = {k: list(v) for k, v in st.session_state.knockout.items() if v is not None}
    return json.dumps(data, ensure_ascii=False, indent=2)

def carregar_resultados(conteudo):
    data = json.loads(conteudo)
    for grp in GROUPS:
        for i in range(6):
            key = f"{grp}_{i}"
            if key in data.get("results", {}):
                st.session_state.results[key] = tuple(data["results"][key])
            else:
                st.session_state.results[key] = None
    st.session_state.knockout = {}
    for key, val in data.get("knockout", {}).items():
        st.session_state.knockout[key] = tuple(val)

# ========================= UI =========================

st.title("🏆 Copa do Mundo FIFA 2026 — Simulador")
st.markdown('<p style="color:#888; margin-top:-12px;">Canadá · México · Estados Unidos · 11 jun – 19 jul 2026 · 48 seleções · 12 grupos</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🎲 Simular Todos os Jogos", use_container_width=True):
        simulate_all()
with col2:
    if st.button("🔄 Resetar Tudo", use_container_width=True):
        reset_all()
with col3:
    uploaded = st.file_uploader("📂 Carregar", type="json", label_visibility="collapsed")
    if uploaded is not None:
        carregar_resultados(uploaded.read().decode("utf-8"))
        st.rerun()
with col4:
    resultados_json = serializar_resultados()
    st.download_button("💾 Salvar", data=resultados_json, file_name="resultados_copa2026.json",
                       mime="application/json", use_container_width=True)

st.divider()

total_played = sum(1 for v in st.session_state.results.values() if v is not None)
total_matches = 72

if total_played > 0:
    st.markdown(f"**Jogos disputados:** {total_played}/{total_matches} — {total_played/total_matches*100:.0f}% completo")
    st.progress(total_played / total_matches)
    st.divider()

tabs = st.tabs(["Grupos A–D", "Grupos E–H", "Grupos I–L", "📊 Classificação Geral", "🏆 Mata-mata"])

all_groups = list(GROUPS.keys())

with tabs[0]:
    for grp in all_groups[0:4]:
        st.markdown(f"### Grupo {grp}")
        df = get_group_table(grp)
        st.dataframe(df, hide_index=True, width="stretch", height=190,
                     column_config={c: st.column_config.Column(c, width=None if c != "TIME" else 200) for c in df.columns})
        for i, (h, a) in enumerate(GROUPS[grp]["matches"]):
            key = f"{grp}_{i}"
            r = st.session_state.results.get(key)
            date_label = MATCH_ROUNDS[grp][i]
            cols = st.columns([3, 1, 1, 1, 3])
            with cols[0]:
                st.markdown(f"<div style='text-align:right; font-size:14px;'>{flag(h)}</div>", unsafe_allow_html=True)
            with cols[1]:
                gh = st.number_input("C", key=f"gh_{key}", value=r[0] if r else 0, min_value=0, max_value=20, label_visibility="collapsed")
            with cols[2]:
                st.markdown("<div style='text-align:center; color:#666; padding-top:6px;'>×</div>", unsafe_allow_html=True)
            with cols[3]:
                ga = st.number_input("F", key=f"ga_{key}", value=r[1] if r else 0, min_value=0, max_value=20, label_visibility="collapsed")
            with cols[4]:
                st.markdown(f"<div style='text-align:left; font-size:14px;'>{flag(a)} <span style='color:#666; font-size:11px;'>{date_label}</span></div>", unsafe_allow_html=True)
            if r is None and (gh > 0 or ga > 0):
                st.session_state.results[key] = (gh, ga)
            elif r is not None:
                st.session_state.results[key] = (gh, ga)
        st.divider()

with tabs[1]:
    for grp in all_groups[4:8]:
        st.markdown(f"### Grupo {grp}")
        df = get_group_table(grp)
        st.dataframe(df, hide_index=True, width="stretch", height=190,
                     column_config={c: st.column_config.Column(c, width=None if c != "TIME" else 200) for c in df.columns})
        for i, (h, a) in enumerate(GROUPS[grp]["matches"]):
            key = f"{grp}_{i}"
            r = st.session_state.results.get(key)
            date_label = MATCH_ROUNDS[grp][i]
            cols = st.columns([3, 1, 1, 1, 3])
            with cols[0]:
                st.markdown(f"<div style='text-align:right; font-size:14px;'>{flag(h)}</div>", unsafe_allow_html=True)
            with cols[1]:
                gh = st.number_input("C", key=f"gh_{key}", value=r[0] if r else 0, min_value=0, max_value=20, label_visibility="collapsed")
            with cols[2]:
                st.markdown("<div style='text-align:center; color:#666; padding-top:6px;'>×</div>", unsafe_allow_html=True)
            with cols[3]:
                ga = st.number_input("F", key=f"ga_{key}", value=r[1] if r else 0, min_value=0, max_value=20, label_visibility="collapsed")
            with cols[4]:
                st.markdown(f"<div style='text-align:left; font-size:14px;'>{flag(a)} <span style='color:#666; font-size:11px;'>{date_label}</span></div>", unsafe_allow_html=True)
            if r is None and (gh > 0 or ga > 0):
                st.session_state.results[key] = (gh, ga)
            elif r is not None:
                st.session_state.results[key] = (gh, ga)
        st.divider()

with tabs[2]:
    for grp in all_groups[8:12]:
        st.markdown(f"### Grupo {grp}")
        df = get_group_table(grp)
        st.dataframe(df, hide_index=True, width="stretch", height=190,
                     column_config={c: st.column_config.Column(c, width=None if c != "TIME" else 200) for c in df.columns})
        for i, (h, a) in enumerate(GROUPS[grp]["matches"]):
            key = f"{grp}_{i}"
            r = st.session_state.results.get(key)
            date_label = MATCH_ROUNDS[grp][i]
            cols = st.columns([3, 1, 1, 1, 3])
            with cols[0]:
                st.markdown(f"<div style='text-align:right; font-size:14px;'>{flag(h)}</div>", unsafe_allow_html=True)
            with cols[1]:
                gh = st.number_input("C", key=f"gh_{key}", value=r[0] if r else 0, min_value=0, max_value=20, label_visibility="collapsed")
            with cols[2]:
                st.markdown("<div style='text-align:center; color:#666; padding-top:6px;'>×</div>", unsafe_allow_html=True)
            with cols[3]:
                ga = st.number_input("F", key=f"ga_{key}", value=r[1] if r else 0, min_value=0, max_value=20, label_visibility="collapsed")
            with cols[4]:
                st.markdown(f"<div style='text-align:left; font-size:14px;'>{flag(a)} <span style='color:#666; font-size:11px;'>{date_label}</span></div>", unsafe_allow_html=True)
            if r is None and (gh > 0 or ga > 0):
                st.session_state.results[key] = (gh, ga)
            elif r is not None:
                st.session_state.results[key] = (gh, ga)
        st.divider()

with tabs[3]:
    st.subheader("📋 Classificação Geral")
    if total_played < 72:
        st.info(f"Preencha todos os {total_matches} jogos da fase de grupos para ver a classificação geral e os classificados.")
    else:
        leaders = []
        for grp in sorted(GROUPS.keys()):
            stats, ordered = get_standings(grp)
            leaders.append({"Grupo": grp, "1°": flag(ordered[0]), "Pts": stats[ordered[0]]["P"],
                           "2°": flag(ordered[1]), "Pts2": stats[ordered[1]]["P"],
                           "3°": flag(ordered[2]), "Pts3": stats[ordered[2]]["P"],
                           "4°": flag(ordered[3]), "Pts4": stats[ordered[3]]["P"]})
        df_leaders = pd.DataFrame(leaders)
        st.dataframe(df_leaders, hide_index=True, width="stretch",
                     column_config={c: st.column_config.Column(c) for c in df_leaders.columns})

        st.divider()
        st.subheader("🏅 Classificados para o Mata-mata")

        third_ranked = get_third_placed_ranking()

        qualified = []
        for grp in sorted(GROUPS.keys()):
            stats, ordered = get_standings(grp)
            qualified.append((grp, ordered[0], stats[ordered[0]]["P"], "1°", True))
            qualified.append((grp, ordered[1], stats[ordered[1]]["P"], "2°", True))

        best_third = third_ranked[:8]
        for grp, t, pts, sg, gf, _ in best_third:
            qualified.append((grp, t, pts, "3°", True))

        remaining_third = third_ranked[8:]
        for grp, t, pts, sg, gf, _ in remaining_third:
            qualified.append((grp, t, pts, "3°", False))

        qualified.sort(key=lambda x: (0 if x[4] else 1, x[0]))

        st.markdown("**Critério:** 2 primeiros de cada grupo (24) + 8 melhores terceiros = **32 seleções**")

        cls1, cls2, cls3 = st.columns(3)
        for idx, (grp, t, pts, pos, q) in enumerate(qualified):
            col = cls1 if idx % 3 == 0 else cls2 if idx % 3 == 1 else cls3
            badge = "🟢" if q else "🔴"
            status = "Classificado" if q else "Eliminado"
            with col:
                st.markdown(f"{badge} **{flag(t)}** — Grupo {grp} ({pos}) — {pts} pts — <span style='color:{"#4ade80" if q else "#f87171"}; font-size:13px;'>{status}</span>", unsafe_allow_html=True)

with tabs[4]:
    st.subheader("🏆 Mata-mata")
    if total_played < 72:
        st.info("Complete todos os jogos da fase de grupos para simular o mata-mata.")
    else:
        third_ranked = get_third_placed_ranking()
        qualified_third = {g: t for g, t, _, _, _, _ in third_ranked[:8]}

        group_winners = {}
        group_runners = {}
        for grp in sorted(GROUPS.keys()):
            stats, ordered = get_standings(grp)
            group_winners[grp] = ordered[0]
            group_runners[grp] = ordered[1]

        def best_third_from(groups):
            for g, t, _, _, _, _ in third_ranked:
                if g in groups and g in qualified_third:
                    return t
            return None

        KO_MATCHES = [
            ("73", group_runners["A"], group_runners["B"]),
            ("74", group_winners["E"], best_third_from({"A","B","C","D","F"})),
            ("75", group_winners["F"], group_runners["C"]),
            ("76", group_winners["C"], group_runners["F"]),
            ("77", group_winners["I"], best_third_from({"C","D","F","G","H"})),
            ("78", group_runners["E"], group_runners["I"]),
            ("79", group_winners["A"], best_third_from({"C","E","F","H","I"})),
            ("80", group_winners["L"], best_third_from({"E","H","I","J","K"})),
            ("81", group_winners["D"], best_third_from({"B","E","F","I","J"})),
            ("82", group_winners["G"], best_third_from({"A","E","H","I","J"})),
            ("83", group_runners["K"], group_runners["L"]),
            ("84", group_winners["H"], group_runners["J"]),
            ("85", group_winners["B"], best_third_from({"E","F","G","I","J"})),
            ("86", group_winners["J"], group_runners["H"]),
            ("87", group_winners["K"], best_third_from({"D","E","I","J","L"})),
            ("88", group_runners["D"], group_runners["G"]),
        ]

        st.markdown("### ⚽ Oitavas de Final (16 avos)")
        for i in range(0, 16, 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j >= len(KO_MATCHES):
                    continue
                num, t1, t2 = KO_MATCHES[i + j]
                key = f"R32_{num}"
                r = st.session_state.knockout.get(key)
                with cols[j]:
                    st.markdown(f"**Jogo {num}**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        gh = st.number_input("C", key=f"gh_{key}", value=r[0] if r else 0, min_value=0, max_value=20, label_visibility="collapsed")
                    with col_b:
                        ga = st.number_input("F", key=f"ga_{key}", value=r[1] if r else 0, min_value=0, max_value=20, label_visibility="collapsed")
                    t1_name = t1 if t1 else "?"
                    t2_name = t2 if t2 else "?"
                    st.markdown(f"<div style='font-size:12px; line-height:1.8;'>{flag(t1_name)}<br>{flag(t2_name)}</div>", unsafe_allow_html=True)
                    if r is None and (gh > 0 or ga > 0):
                        st.session_state.knockout[key] = (gh, ga)
                    elif r is not None:
                        st.session_state.knockout[key] = (gh, ga)

        if st.button("🎲 Simular Mata-mata", use_container_width=True):
            for num, _, _ in KO_MATCHES:
                key = f"R32_{num}"
                g1, g2 = random_score(), random_score()
                if g1 == g2:
                    g1 += 1
                st.session_state.knockout[key] = (g1, g2)
            st.rerun()

# Auto-salvar sempre que houver mudancas
novo_snapshot = serializar_resultados()
if "snapshot" not in st.session_state or st.session_state.snapshot != novo_snapshot:
    st.session_state.snapshot = novo_snapshot
    try:
        with open(SALVAR_PATH, "w") as f:
            f.write(novo_snapshot)
    except Exception:
        pass
