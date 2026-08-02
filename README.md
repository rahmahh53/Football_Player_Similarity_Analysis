# Football Scouting Intelligence System

An end-to-end football analytics and machine learning project built using StatsBomb Open Data.

This project combines data engineering, relational database design, SQL analytics, feature engineering, machine learning, and MLOps to build a data-driven football scouting system.

## Project Goal

The goal of this project is to develop a football scouting platform that can:

- Evaluate player performance using event-level match data
- Build role-specific player profiles
- Compare players across teams, competitions, and seasons
- Identify players with similar playing styles
- Recommend potential transfer targets or replacement players
- Present scouting insights through a deployable application

Rather than evaluating players using only goals and assists, the system will use actions such as passes, carries, shots, dribbles, duels, pressures, and defensive contributions to build more complete player profiles.

## Machine Learning Goal

The primary machine learning goal is to build a role-aware system for recommending potential transfer targets and replacement players.

The current baseline uses standardized player features, Euclidean similarity, and K-Means clustering to explore player profiles and identify broad playing archetypes. These baseline models are used to validate the feature space and establish reference results before developing more advanced similarity and recommendation approaches.

For example:

> Find midfielders whose passing, ball progression, chance creation, carrying, and defensive profiles are similar to a selected player.

Future versions may include:

- Player archetype clustering
- Transfer-target recommendation
- Player performance prediction
- Role suitability analysis
- Team-style and player-fit analysis

## Dataset

This project uses the [StatsBomb Open Data](https://github.com/statsbomb/open-data) dataset.

The dataset contains detailed match-level and event-level information, including:

- Competitions
- Seasons
- Matches
- Teams
- Managers
- Players
- Lineups
- Player positions
- Passes
- Carries
- Shots
- Dribbles
- Duels
- Pressures
- Ball recoveries
- Fouls
- Cards
- Possession information

The complete raw dataset is excluded from version control because of its size and because it can be downloaded again from the original source.

## Technology Stack

- Python
- Pandas
- MySQL
- SQL
- SQLAlchemy
- Jupyter Notebook
- Parquet
- Scikit-learn — planned
- MLflow — planned
- FastAPI — planned
- Docker — planned
- GitHub Actions — planned

## Project Architecture

```text
StatsBomb Open Data
        │
        ▼
Raw JSON Files
        │
        ▼
Data Exploration and Validation
        │
        ▼
Reusable Parsing Pipeline
(parse_data.py / parse_events.py)
        │
        ├────────────────────┐
        ▼                    ▼
Normalized DataFrames   Parquet Event Batches
        │                    │
        └──────────┬─────────┘
                   ▼
             MySQL Database
                   │
                   ▼
        SQL Analysis and Validation
                   │
                   ▼
       Player-Level Feature Engineering
                   │
                   ▼
        Role-Specific Scouting Profiles
                   │
                   ▼
     Player Similarity and Ranking Models
                   │
                   ▼
          MLflow Experiment Tracking
                   │
                   ▼
          FastAPI Scouting Service
                   │
                   ▼
             Docker Deployment
```

## Database Design

The relational database separates match metadata, player information, and event-specific information into normalized tables.

### Core Tables

- `competitions`
- `seasons`
- `countries`
- `teams`
- `managers`
- `matches`
- `players`
- `lineups`
- `player_positions`
- `team_managers`
- `cards`

### Event Tables

- `events`
- `passes`
- `shots`
- `carries`
- `dribbles`
- `duels`

General event information is stored in the `events` table, while event-specific attributes are stored in the corresponding subtype tables.

```text
events.event_id
        │
        ├── passes.event_id
        ├── shots.event_id
        ├── carries.event_id
        ├── dribbles.event_id
        └── duels.event_id
```

This structure reduces duplication and allows event-specific tables to reference the general event record through `event_id`.

## Current Progress

### Completed

- Set up the project repository and development environment
- Designed and created the normalized MySQL database schema
- Built reusable parsing pipelines for core and event data
- Implemented batch-based Parquet generation for large event datasets
- Loaded core and event-specific tables into MySQL
- Created reusable SQL analysis queries
- Engineered player-level passing, shooting, dribbling, carrying, and duel metrics
- Built the initial player-level feature dataset
- Standardized player features for machine learning
- Implemented a baseline Euclidean player-similarity analysis
- Implemented a baseline K-Means clustering model
- Interpreted six data-driven player archetypes
- Documented the clustering analysis and model limitations

### In Progress

- Built the initial player-level feature dataset
- Standardized player features for machine learning
- Implemented a baseline Euclidean player-similarity analysis
- Implemented a baseline K-Means clustering model
- Interpreted six data-driven player archetypes
- Documented the clustering analysis and model limitations

### Planned

#### Feature Engineering

- Engineer advanced role-specific scouting metrics
- Incorporate defensive event statistics (tackles, interceptions, recoveries, pressures)
- Add possession-adjusted and percentile-based metrics
- Expand feature normalization using minutes played and per-90 statistics

#### Machine Learning

- Evaluate the baseline K-Means clustering model using silhouette scores and other clustering metrics
- Explore dimensionality reduction techniques (PCA and UMAP) for player visualization
- Compare alternative clustering algorithms (Hierarchical Clustering, Gaussian Mixture Models, DBSCAN)
- Develop a role-aware player recommendation engine
- Build a transfer-target and replacement-player ranking model
- Experiment with learned player embeddings for improved similarity search

#### Deployment & MLOps

- Track experiments using MLflow
- Build a FastAPI inference service
- Containerize the application with Docker
- Automate testing and deployment using GitHub Actions

#### Application

- Develop an interactive football scouting dashboard
- Build player search and comparison interfaces
- Visualize player archetypes and similarity networks
- Generate automated scouting reports

## Planned Scouting Metrics

### Passing

- Pass attempts
- Completed passes
- Pass-completion percentage
- Progressive passes
- Average pass length
- Final-third passes
- Passes into the penalty area
- Key passes
- Crosses
- Switches of play

### Ball Progression

- Progressive carries
- Carry distance
- Carries into the final third
- Carries into the penalty area
- Successful dribbles
- Dribble success percentage

### Attacking Contribution

- Shots
- Shots on target
- Goals
- Expected goals, where available
- Shot-creating actions
- Completed attacking actions
- Penalty-area involvement

### Defensive Contribution

- Duels
- Duel success percentage
- Pressures
- Ball recoveries
- Interceptions
- Tackles
- Counterpressing actions

Where appropriate, metrics will be normalized using:

- Per-90-minute rates
- Per-possession rates
- Team-possession adjustments
- Success percentages
- Position-group percentile rankings

## Example SQL Analyses

Current and planned SQL analyses include:

- Passing leaders
- Pass-completion leaders
- Progressive-passing leaders
- Average pass length
- Successful dribblers
- Player attacking actions
- Home and away performance
- Competition summaries
- Event-type distributions
- Position-specific player rankings


```

## Data Storage Strategy

The project uses different storage formats for different purposes:

- **JSON** for the original StatsBomb source data
- **Pandas DataFrames** during exploration and transformation
- **Parquet** for efficient intermediate event storage
- **MySQL** for relational analysis and reusable SQL queries
- **Serialized model artifacts** for machine learning inference

Raw and complete processed datasets are excluded from Git because of their size.

Small sample datasets may be added later to demonstrate the pipeline.

## Reproducibility

The project separates exploratory work from reusable production code:

- Exploratory analysis remains in `notebooks/`
- Reusable parsing and loading logic belongs in `src/`
- Finalized schema definitions belong in `database/schema.sql`
- Polished analytical queries belong in `database/analysis_queries.sql`
- Data-integrity checks belong in `database/validation_queries.sql`
- The reusable player-level modeling dataset is defined in `database/player_features.sql`

This structure will allow the database and feature pipeline to be rebuilt from the original StatsBomb data.

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/rahmahh53/Football_Project.git
cd Football_Project/football
```

### 2. Create and activate a Python environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create a MySQL database:

```sql
CREATE DATABASE football_db;
```

Create a dedicated database user and grant access:

```sql
CREATE USER 'notebook_user'@'localhost'
IDENTIFIED BY 'your_password';

GRANT ALL PRIVILEGES
ON football_db.*
TO 'notebook_user'@'localhost';
```

### 5. Run the notebooks

Start Jupyter Notebook:

```bash
jupyter notebook
```

Use the notebooks for data exploration, parsing validation, and SQL analysis.

### 6. Generate event Parquet files

```bash
python src/parse_events.py
```

The exact command-line configuration may change as the reusable pipeline is finalized.

## Current Focus

The current focus is preparing the engineered player feature dataset for exploratory analysis and machine learning.

This includes:

1. Validating the final player-level feature table
2. Expanding role-specific scouting metrics
3. Exporting SQL features into pandas
4. Analyzing distributions, correlations, and outliers
5. Preparing features for player similarity and clustering models

## Long-Term Outcome

The completed system will allow a user to select a player, position, or desired playing profile and receive:

- A statistical scouting report
- Role-specific strengths and weaknesses
- Percentile comparisons
- Similar-player rankings
- Potential replacement candidates
- Supporting event-level evidence

## Project Status

This project is under active development.
