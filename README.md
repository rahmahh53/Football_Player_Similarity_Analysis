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

The first planned machine learning component is a **role-aware player similarity system**.

Given a selected player, the system will rank other players with similar statistical and event-based profiles.

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
- Downloaded and explored StatsBomb Open Data
- Examined competition, match, lineup, and event JSON structures
- Designed the initial normalized relational database schema
- Connected Jupyter Notebook to MySQL using SQLAlchemy
- Created core MySQL tables
- Parsed competition, match, team, player, and event data
- Built event-specific DataFrames
- Implemented Parquet-based event batch generation
- Loaded selected datasets into MySQL
- Wrote foundational SQL analytics queries
- Created initial passing and attacking-action analyses

### In Progress

- Finalizing the reusable database-loading pipeline
- Validating primary-key and foreign-key relationships
- Consolidating the database schema into reusable SQL files
- Creating data-quality and validation queries
- Developing player scouting metrics
- Engineering role-specific player features
- Creating player and team summary tables
- Improving the reproducibility of the ingestion pipeline

### Planned

- Player-level feature matrix
- Per-90 metrics
- Possession-adjusted metrics
- Position and role filtering
- Player similarity modeling
- Player archetype clustering
- Transfer-target ranking
- MLflow experiment tracking
- FastAPI inference service
- Docker deployment
- Automated tests
- CI/CD pipeline

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


## Repository Structure

```text
Football_Project/
│
├── football/
│   ├── data/
│   │   ├── raw_data/
│   │   └── processed/
│   │
│   ├── database/
│   │   ├── schema.sql
│   │   ├── analysis_queries.sql
│   │   └── validation_queries.sql
│   │
│   ├── notebooks/
│   │   ├── 01_explore_events.ipynb
│   │   ├── 02_explore_data.ipynb
│   │   └── 03_parse_data.ipynb
│   │
│   ├── src/
│   │   ├── load_config.py
│   │   ├── load_data.py
│   │   ├── parse_data.py
│   │   └── parse_events.py
│   │
│   ├── models/
│   ├── reports/
│   ├── docker/
│   ├── tests/
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

Some files shown above represent the intended final repository structure and will be added as the project develops.

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

The current focus is building a reliable data foundation for the scouting system.

This includes:

1. Completing the normalized MySQL database
2. Validating table relationships and data completeness
3. Moving exploratory parsing logic into reusable Python modules
4. Consolidating polished SQL queries
5. Defining meaningful role-specific scouting features
6. Building the player-level feature dataset required for modeling

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
