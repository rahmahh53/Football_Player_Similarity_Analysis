import os
import requests
import streamlit as st
import plotly.graph_objects as go

API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://127.0.0.1:8000"))

st.set_page_config(page_title="Football Scouting Intelligence", page_icon="⚽", layout="wide")
st.title("Football Scouting Intelligence")
st.write("Find statistically similar players using event-level football performance profiles.")
st.caption("Select a player to find statistically similar alternatives based on 15 passing, progression, carrying, dribbling, shooting, and duel metrics.")

players = []
feature_labels = {
    "passes_per_90": "Passes / 90",
    "pass_completion_rate": "Pass Completion",
    "progressive_passes_per_90": "Progressive Passes / 90",
    "progressive_pass_rate": "Progressive Pass Rate",
    "carries_per_90": "Carries / 90",
    "progressive_carries_per_90": "Progressive Carries / 90",
    "dribbles_per_90": "Dribbles / 90",
    "dribble_success_rate": "Dribble Success",
    "shots_per_90": "Shots / 90",
    "goals_per_90": "Goals / 90",
    "xg_per_90": "xG / 90",
    "average_xg_per_shot": "Average xG / Shot",
    "duels_per_90": "Duels / 90",
    "successful_duels_per_90": "Successful Duels / 90",
    "duel_success_rate": "Duel Success",
    }

try:
    response = requests.get(f"{API_URL}/players")
    response.raise_for_status()
    players = response.json()

except requests.RequestException:
    st.error("Unable to connect to the scouting API. Please try again later.")
    st.stop()


selected_player = st.selectbox("Target player", players, format_func=lambda player: (f"{player['player_name']} - {player['role_group']}"))
selected_player_id = selected_player["player_id"]

scope_options = {"Same role": "role", "Exact position": "position", "All players": None}
selected_scope = st.selectbox("Compare within", options=list(scope_options.keys()))
position_filter = scope_options[selected_scope]

top_n = st.slider("Number of recommendations", min_value=1, max_value=10, value=5)
search_button = st.button("Find replacements", type="primary")

if search_button:
    params = {"top_n": top_n}
    if position_filter is not None:
        params["position_filter"] = position_filter
    response = requests.get(f"{API_URL}/players/{selected_player_id}/replacements", params=params)
    response.raise_for_status()
    result = response.json()

    st.session_state["recommendations"] = result["recommendations"]
    st.session_state["target_player"] = selected_player


if "recommendations" in st.session_state:
    recommendations = st.session_state["recommendations"]
    target_player = st.session_state["target_player"]

    st.subheader(f"Recommended replacements for {target_player['player_name']}")
    st.caption("Players are ranked by standardized Euclidean distance. Lower distance indicates a more similar statistical playing profile")

    for rank, player in enumerate(recommendations, start=1):
        with st.container(border=True):
            st.subheader(f"{rank}. {player['player_name']}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Role", player["role_group"])
            with col2:
                st.metric("Qualifying matches", player["qualifying_matches"])
            with col3:
                st.metric(f"Similarity distance ↓", f"{player['distance']: .3f}")

            st.write("**Most similar attributes**")
            st.write(", ". join(feature_labels.get(feature, feature) for feature in player["most_similar_features"]))
            st.write("**Largest differences**")
            st.write(", ".join(feature_labels.get(feature, feature) for feature in player["largest_differences"]))

    st.divider()

    comparison_player = st.selectbox("Compare target with", recommendations, format_func=lambda player: player["player_name"])

    target_response = requests.get(f"{API_URL}/players/{target_player['player_id']}/profile")
    target_response.raise_for_status()
    target_profile = target_response.json()

    comparison_response = requests.get(f"{API_URL}/players/{comparison_player['player_id']}/profile")
    comparison_response.raise_for_status()
    comparison_profile = comparison_response.json()

    target_percentile_response = requests.get(f"{API_URL}/players/{target_player['player_id']}/percentiles")
    target_percentile_response.raise_for_status()
    target_percentiles = target_percentile_response.json()["percentiles"]

    comparison_percentile_response = requests.get(f"{API_URL}/players/{comparison_player['player_id']}/percentiles")
    comparison_percentile_response.raise_for_status()
    comparison_percentiles = comparison_percentile_response.json()["percentiles"]

    st.write(f"Percentile comparison relative to other {target_player['role_group'].lower()}s")

    features = list(feature_labels.keys())
    labels = [feature_labels[feature] for feature in features]

    fig = go.Figure()
    fig.add_trace(go.Bar(name=target_player["player_name"], y=labels, x=[target_percentiles[feature] for feature in features], orientation="h"))
    fig.add_trace(go.Bar(name=comparison_player["player_name"], y=labels, x=[comparison_percentiles[feature] for feature in features], orientation='h'))
    fig.update_layout(barmode="group", xaxis=dict(title="Role-relative percentile", range=[0, 100]), yaxis=dict(title=None, autorange="reversed"), legend_title_text="Player", height=700)

    st.caption(
    "Percentiles are calculated relative to players in the same role. "
    "A 90th percentile score means the player ranks above approximately "
    "90% of players in that role for that attribute.")
    st.plotly_chart(fig, use_container_width=True)
