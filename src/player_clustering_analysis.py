from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy import URL, create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAYER_FEATURE_QUERY_PATH = PROJECT_ROOT / "database" / "player_features.sql"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
OUTPUTS_DIR = PROJECT_ROOT / "data" / "processed"
ELBOW_PLOT_PATH = FIGURES_DIR / "elbow_curve.png"
CLUSTERED_PLAYERS_PATH = OUTPUTS_DIR / "clustered_players.parquet"
CLUSTER_PROFILES_PATH = REPORTS_DIR / "cluster_profiles.csv"

FEATURE_COLUMNS = ["pass_completion_rate", "passes_per_match", "progressive_passes_per_match", "progressive_pass_rate", "shots_per_match", "goals_per_match", "xg_per_match", "average_xg_per_shot", "dribbles_per_match", "dribble_success_rate", "carries_per_match", "progressive_carries_per_match"]

IDENTIFIER_COLUMNS = ["player_id", "player_name"]
FINAL_K = 6
RANDOM_STATE = 42
N_INIT = 10


def load_player_features() -> pd.DataFrame:
    """Load the player feature dataset from MySQL using the SQL file."""
    database_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "football_db"),
    )

    engine = create_engine(database_url)
    query = PLAYER_FEATURE_QUERY_PATH.read_text(encoding="utf-8")
    try:
        return pd.read_sql(query, con=engine)
    finally:
        engine.dispose()


def validate_player_features(player_features_df: pd.DataFrame) -> None:
    required_columns = set(IDENTIFIER_COLUMNS + FEATURE_COLUMNS)

    print("\nDataset shape:")
    print(player_features_df.shape)
    print("\nColumn data types:")
    print(player_features_df.dtypes)
    print("\nMissing values:")
    print(player_features_df.isna().sum())
    print("\nAre player IDs unique?")
    print(player_features_df["player_id"].is_unique)

    percentage_columns = ["pass_completion_rate", "progressive_pass_rate", "dribble_success_rate"]
    print("\nPercentage ranges:")
    for column in percentage_columns:
        minimum = player_features_df[column].min()
        maximum = player_features_df[column].max()
        print(f"{column}: min={minimum:.2f}, max={maximum:.2f}")

def prepare_model_features(player_features_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, StandardScaler]:
    """Separate IDs, select model features, fill missing values, and scale."""
    identifiers_df = player_features_df[IDENTIFIER_COLUMNS].copy()
    model_features_df = player_features_df[FEATURE_COLUMNS].copy()

    model_features_df["average_xg_per_shot"] = (model_features_df["average_xg_per_shot"].fillna(0))

    if model_features_df.isna().sum().sum() != 0:
        raise ValueError("Model features still contain missing values.")

    non_numeric_columns = (model_features_df.select_dtypes(exclude="number").columns.tolist())
    if non_numeric_columns:
        raise TypeError("Non-numeric model columns found: " + ", ".join(non_numeric_columns))

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(model_features_df)
    scaled_features_df = pd.DataFrame(scaled_features, columns=FEATURE_COLUMNS, index=player_features_df.index)

    print("\nScaled feature means and standard deviations:")
    print(scaled_features_df.describe().T[["mean", "std"]])

    return identifiers_df, model_features_df, scaled_features_df, scaler


def find_similar_players(player_name: str, identifiers_df: pd.DataFrame, scaled_features_df: pd.DataFrame, player_id: int | None = None, n: int = 10) -> pd.DataFrame | None:
    """Return nearest players using Euclidean distance."""
    matching_rows = identifiers_df[identifiers_df["player_name"].str.contains(player_name, case=False, na=False)]

    if player_id is not None:
        matching_rows = matching_rows[matching_rows["player_id"] == player_id]

    if matching_rows.empty:
        print("No matching rows found.")
        return None

    if len(matching_rows) > 1:
        print("Multiple players matched. Provide player_id to choose one.")
        return matching_rows

    player_index = matching_rows.index[0]
    player_vector = scaled_features_df.loc[player_index]
    differences = scaled_features_df - player_vector
    distances = np.linalg.norm(differences.to_numpy(), axis=1)

    similarity_results = identifiers_df.copy()
    similarity_results["distance"] = distances
    similarity_results = similarity_results.sort_values(by="distance", ascending=True)

    return similarity_results.iloc[1 : n + 1]


def calculate_inertias(scaled_features_df: pd.DataFrame, minimum_k: int = 2, maximum_k: int = 12) -> tuple[list[int], list[float]]:
    """Fit K-Means across candidate K values and collect inertia."""
    k_values = list(range(minimum_k, maximum_k + 1))
    inertias: list[float] = []

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=N_INIT)
        kmeans.fit(scaled_features_df)
        inertias.append(float(kmeans.inertia_))

    return k_values, inertias


def save_elbow_plot(k_values: list[int], inertias: list[float]) -> None:
    """Save the elbow curve used to support the choice of k=6."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.plot(k_values, inertias, marker="o")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Inertia")
    plt.title("Elbow Method for Player Clustering")
    plt.xticks(k_values)
    plt.tight_layout()
    plt.savefig(ELBOW_PLOT_PATH, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nSaved elbow plot to: {ELBOW_PLOT_PATH}")


def fit_final_kmeans(scaled_features_df: pd.DataFrame, n_clusters: int = FINAL_K) -> tuple[KMeans, np.ndarray]:
    """Fit the final K-Means model and return cluster labels."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=N_INIT)
    cluster_labels = kmeans.fit_predict(scaled_features_df)

    if len(cluster_labels) != len(scaled_features_df):
        raise ValueError("Cluster label count does not match player count.")

    return kmeans, cluster_labels


def build_cluster_outputs(player_features_df: pd.DataFrame, cluster_labels: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Attach labels to players and calculate average cluster profiles."""
    clustered_players_df = player_features_df.copy()
    clustered_players_df["cluster"] = cluster_labels

    cluster_profiles = (clustered_players_df[FEATURE_COLUMNS + ["cluster"]].groupby("cluster").mean())

    print("\nCluster sizes:")
    print(clustered_players_df["cluster"].value_counts().sort_index())
    print("\nAverage cluster profiles:")
    print(cluster_profiles)

    return clustered_players_df, cluster_profiles


def save_outputs(clustered_players_df: pd.DataFrame, cluster_profiles: pd.DataFrame) -> None:
    """Save player assignments and cluster summaries."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    clustered_players_df.to_parquet(CLUSTERED_PLAYERS_PATH, index=False)
    cluster_profiles.to_csv(CLUSTER_PROFILES_PATH, index=True)

    print(f"\nSaved clustered players to: {CLUSTERED_PLAYERS_PATH}")
    print(f"Saved cluster profiles to: {CLUSTER_PROFILES_PATH}")


def main() -> None:
    player_features_df = load_player_features()
    validate_player_features(player_features_df)

    identifiers_df, _, scaled_features_df, _ = prepare_model_features(player_features_df)

    print("\nPlayers most similar to Messi:")
    print(find_similar_players(player_name="Messi", identifiers_df=identifiers_df, scaled_features_df=scaled_features_df, n=10))

    k_values, inertias = calculate_inertias(scaled_features_df, minimum_k=2, maximum_k=12)

    print("\nCandidate K values and inertias:")
    for k, inertia in zip(k_values, inertias):
        print(f"k={k}: inertia={inertia:.2f}")

    save_elbow_plot(k_values, inertias)

    _, cluster_labels = fit_final_kmeans(scaled_features_df, n_clusters=FINAL_K)

    clustered_players_df, cluster_profiles = build_cluster_outputs(player_features_df, cluster_labels)

    save_outputs(clustered_players_df, cluster_profiles)


if __name__ == "__main__":
    main()
