from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine


PLAYER_FEATURES_SQL = Path("database/player_features.sql")


def load_player_match_features(engine: Engine) -> pd.DataFrame:
    query = PLAYER_FEATURES_SQL.read_text()

    return pd.read_sql(query, engine)

def merge_player_minutes(player_match_df: pd.DataFrame, player_minutes_df: pd.DataFrame) -> pd.DataFrame:
    return player_match_df.merge(player_minutes_df, on=["player_id", "team_id", "match_id"], how="inner")
