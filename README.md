# Football/Soccer Match Intelligence System

## Project Overview

This project is an end-to-end machine learning and MLOps system for analyzing football/soccer match event data. The goal is to build a system that can ingest open-source football/soccer event data, store it in a MySQL database, engineer useful match and possession-level features, train machine learning models, track experiments, and eventually serve predictions through an API.

The first modeling task is:

> Predict whether a possession sequence is likely to become dangerous.
A dangerous possession may be defined as a possession that directly leads to a meaningful goal-scoring opportunity. In the first version, this may be labeled using outcomes such as a shot, a touch or pass into the penalty box, or another attacking event close to goal.
_is_dangerous_possession = 1 if possession contains a shot, 0 otherwise
This project uses StatsBomb Open Data, an open-source soccer event dataset. The dataset contains match-level event data, including passes, carries, shots, fouls, pressures, and other in-game actions.
## Planned System Design

```text
Raw soccer event data
        ↓
Data cleaning and preprocessing
        ↓
MySQL database
        ↓
SQL queries and feature engineering
        ↓
Machine learning model training
        ↓
Experiment tracking with MLflow
        ↓
Model evaluation and error analysis
        ↓
FastAPI prediction service
        ↓
Dockerized application
