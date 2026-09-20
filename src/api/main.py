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
