from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Query

from src.scouting.engine import ScoutingEngine


PROFILE_PATH = Path("data/artifacts/scouting_profiles.parquet")

app = FastAPI(title="Football Scouting Intelligence API", version="1.0.0", description="Player replacement recommendations based on statistical playing profiles.")

player_profiles = pd.read_parquet(PROFILE_PATH)
scouting_engine = ScoutingEngine(player_profiles)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "players_loaded": len(player_profiles),
    }

@app.get("/players/{player_id}/replacements")
def find_replacements(player_id: int, top_n: int = Query(default=10, ge=1, le=50), position_filter: str | None = Query(default="role")):
    try:
        return {
            "player_id": player_id,
            "position_filter": position_filter,
            "recommendations": scouting_engine.find_replacements(player_id=player_id, top_n=top_n, position_filter=position_filter)}

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@app.get("/players")
def list_players():
    players = (player_profiles[["player_id", "player_name", "role_group"]].drop_duplicates().sort_values("player_name"))
    return players.to_dict(orient="records")

@app.get("/players/{player_id}/profile")
def get_player_profile(player_id: int):
    player = player_profiles[player_profiles["player_id"] == player_id]

    if player.empty:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")
    return player.iloc[0].to_dict()

@app.get("/players/{player_id}/percentiles")
def get_player_percentiles(player_id: int):
    player = player_profiles[player_profiles["player_id"] == player_id]

    if player.empty:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    features = ["passes_per_90", "pass_completion_rate", "progressive_passes_per_90", "progressive_pass_rate", "carries_per_90", "progressive_carries_per_90", "dribbles_per_90", "dribble_success_rate", "shots_per_90", "goals_per_90", "xg_per_90", "average_xg_per_shot", "duels_per_90", "successful_duels_per_90", "duel_success_rate"]
    role_group = player.iloc[0]["role_group"]
    role_players = player_profiles[player_profiles["role_group"] == role_group]
    percentiles = (role_players[features].rank(pct=True).mul(100))

    player_index = player.index[0]

    return {
        "player_id": player_id,
        "player_name": player.iloc[0]["player_name"],
        "percentiles": percentiles.loc[player_index].round(1).to_dict(),
    }
