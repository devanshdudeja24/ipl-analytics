from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="IPL Analytics", layout="wide")

ROOT = Path(__file__).resolve().parent


@st.cache_data
def load_data():
    matches = pd.read_csv(ROOT / "data" / "processed" / "matches_clean.csv")
    deliveries = pd.read_csv(ROOT / "data" / "processed" / "deliveries_clean.csv")
    return matches, deliveries


@st.cache_resource
def load_model():
    return joblib.load(ROOT / "models" / "win_predictor.pkl")


matches, deliveries = load_data()
teams = sorted(matches["team1"].unique())
cities = sorted(matches["city"].dropna().unique())

st.title("🏏 IPL Analytics and Win Predictor")
st.caption("Built on simulated practice data, not real IPL records.")

tab1, tab2, tab3 = st.tabs(["Team Stats", "Player Stats", "Win Predictor"])

# ---------- Tab 1: Team stats ----------
with tab1:
    team = st.selectbox("Select team", teams)
    played = matches[(matches["team1"] == team) | (matches["team2"] == team)]
    wins = int((played["winner"] == team).sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Matches", len(played))
    c2.metric("Wins", wins)
    c3.metric("Win %", f"{wins / len(played) * 100:.1f}%")

    by_season = (
        played[played["winner"] == team]
        .groupby("season")
        .size()
        .reset_index(name="wins")
    )
    st.plotly_chart(px.bar(by_season, x="season", y="wins", title="Wins per season"))

# ---------- Tab 2: Player stats ----------
with tab2:
    top = deliveries.groupby("batter")["batsman_runs"].sum().nlargest(15).reset_index()
    st.plotly_chart(px.bar(top, x="batter", y="batsman_runs", title="Top 15 run scorers"))

# ---------- Tab 3: Win predictor ----------
with tab3:
    model = load_model()

    c1, c2, c3 = st.columns(3)
    bat = c1.selectbox("Batting team", teams, key="bat")
    bowl = c2.selectbox("Bowling team", [t for t in teams if t != bat], key="bowl")
    city = c3.selectbox("City", cities)

    target = st.number_input("Target", 1, 300, 180)
    score = st.number_input("Current score", 0, 299, 100)

    c4, c5 = st.columns(2)
    overs_done = c4.number_input("Overs completed", 0, 19, 10)
    balls_done = c5.number_input("Balls in current over", 0, 5, 0)

    wickets = st.slider("Wickets fallen", 0, 9, 3)

    if st.button("Predict"):
        balls_bowled = int(overs_done) * 6 + int(balls_done)
        balls_left = 120 - balls_bowled
        runs_left = target - score

        if balls_bowled < 1:
            st.warning("Enter at least one ball bowled.")
        elif runs_left <= 0:
            st.success(f"{bat} has already reached the target.")
        else:
            row = pd.DataFrame([{
                "batting_team": bat,
                "bowling_team": bowl,
                "city": city,
                "runs_left": runs_left,
                "balls_left": balls_left,
                "wickets_left": 10 - wickets,
                "target": target,
                "crr": score * 6 / balls_bowled,
                "rrr": runs_left * 6 / balls_left,
            }])
            p = model.predict_proba(row)[0]
            st.success(f"{bat}: {p[1] * 100:.1f}%   |   {bowl}: {p[0] * 100:.1f}%")
