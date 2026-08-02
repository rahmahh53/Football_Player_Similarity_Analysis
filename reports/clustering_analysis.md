# Player Clustering Analysis

## Objective

The objective of this analysis was to determine whether football players naturally group into distinct playing styles based on their on-ball performance metrics rather than predefined positions. Instead of using labels such as defender, midfielder, or forward, K-Means clustering was applied to engineered player features to identify statistically similar groups of players.

---

## Dataset

The analysis was performed on **4,160 players** extracted from the StatsBomb open-data event dataset.

Each player's statistics were aggregated across all matches in which they appeared. To reduce the effect of different sample sizes, most counting statistics were converted into **per-match metrics**.

Before clustering, all numerical features were standardized using **StandardScaler** to ensure that variables measured on larger scales did not dominate the clustering process.

---

## Features Used

The clustering model used the following engineered features:

- pass_completion_rate
- passes_per_match
- progressive_passes_per_match
- progressive_pass_rate
- shots_per_match
- goals_per_match
- xg_per_match
- average_xg_per_shot
- goals_minus_xg
- dribbles_per_match
- dribble_success_rate
- carries_per_match
- progressive_carries_per_match

These features capture multiple aspects of a player's style, including:

- Passing ability
- Ball progression
- Shooting volume
- Finishing quality
- Dribbling
- Ball carrying

---

## Data Preprocessing

Several preprocessing steps were performed before clustering:

- Missing values were checked and handled during feature engineering.
- Only numerical features were retained for clustering.
- Player identifiers and names were excluded from the clustering model.
- Features were standardized using StandardScaler.

Feature scaling was particularly important because statistics such as pass completion rate and goals per match exist on very different numerical scales. Standardization ensures that each feature contributes equally when computing distances between players.

---

## Selecting the Number of Clusters

To determine an appropriate number of clusters, the **Elbow Method** was used.

K-Means models were trained for values of **K ranging from 2 to 12**, and the inertia (within-cluster sum of squares) was recorded for each model.

The resulting elbow curve showed that the reduction in inertia began to slow after approximately **six clusters**. Based on this observation, **K = 6** was selected for the final model.

> *(Insert elbow plot here.)*

---

# Cluster Interpretation

## Cluster 0 – Advanced Attackers / Creative Forwards

This cluster contains highly involved attacking players who contribute through shooting, dribbling, and chance creation while still participating in build-up play.

### Characteristics

- Moderate passing volume
- High shots per match
- High expected goals (xG)
- Highest dribbles per match
- High carries

### Representative Players

- Lionel Messi
- Neymar Jr.
- Kylian Mbappé
- Johan Cruyff

These players combine goalscoring with creativity and progression.

---

## Cluster 1 – Defensive Stoppers (Centre Backs)

This cluster is dominated by central defenders whose primary responsibility is defending rather than progressing the ball.

### Characteristics

- High progressive passing
- Very low shooting
- Very low goals
- Very low dribbling
- Low carries

### Representative Players

- Presnel Kimpembe
- Jan Vertonghen
- Vincent Kompany
- Antonio Rüdiger

These players contribute mainly through defensive stability and ball distribution.

---

## Cluster 2 – Secondary Attackers / Supporting Players

This cluster contains a mixture of supporting attackers, wide forwards, and some attacking midfielders.

### Characteristics

- Low passing volume
- Low progressive passing
- Moderate shooting
- Moderate goals
- Moderate dribbling

Although predominantly attacking players, this cluster also contains a small number of midfielders and attacking full-backs.

---

## Cluster 3 – Ball-Playing Defenders and Possession Builders

Players in this cluster are heavily involved in possession and ball progression.

### Characteristics

- Highest passes per match
- Highest progressive passes
- Highest carries
- High pass completion
- Low shooting output

### Representative Players

- Marco Verratti
- Kyle Walker
- John Stones
- Aaron Cresswell

This cluster represents players responsible for progressing possession from deeper areas of the pitch.

---

## Cluster 4 – Defensive Ball Retainers

This cluster is primarily composed of defenders and defensive midfielders who recycle possession rather than aggressively progressing play.

### Characteristics

- Second-highest passing volume
- Moderate progressive passing
- Very low shooting
- Very low goals
- Low dribbling
- Moderate carries

### Representative Players

- Jamaal Lascelles
- Ben Davies
- Pablo Zabaleta
- Oriol Romeu

These players provide safe possession retention and defensive balance.

---

## Cluster 5 – Primary Attackers / Finishers

This cluster contains players whose primary responsibility is scoring goals.

### Characteristics

- Lowest passing involvement
- Low progressive passing
- Highest goals per match
- Highest xG per match
- High shooting volume
- High dribbling

### Representative Players

- Sergio Agüero
- Romelu Lukaku
- Edinson Cavani
- Pierre-Emerick Aubameyang
- Mohamed Salah
- Kylian Mbappé

Although this cluster includes both centre-forwards and wide forwards, the common characteristic is their high goal-scoring output rather than their listed playing position.

---

# Key Findings

Several interesting patterns emerged from the clustering analysis.

- K-Means successfully grouped players according to statistical playing style without using positional labels.
- Defensive players naturally separated into two distinct groups:
  - Ball-playing defenders
  - Defensive ball retainers
- Attacking players were also divided into two major profiles:
  - Creative attackers
  - Primary finishers
- The discovered clusters reflected player roles rather than official positions, demonstrating that statistical performance can reveal underlying playing styles.

---

# Limitations

This analysis has several limitations.

- Only on-ball event data was considered.
- Defensive actions such as interceptions, tackles, and pressures were not included.
- Playing time was approximated using matches played rather than total minutes.
- Players from multiple competitions, leagues, and seasons were analyzed together.
- Cluster labels were assigned through manual interpretation rather than supervised learning.

---

# Future Work

Several improvements could enhance this analysis.

- Incorporate defensive event metrics.
- Include minutes played to normalize player statistics more accurately.
- Apply dimensionality reduction techniques such as PCA or UMAP for visualization.
- Compare K-Means with alternative clustering algorithms such as Hierarchical Clustering or DBSCAN.
- Develop a player recommendation system using cluster membership and similarity search.
- Evaluate cluster quality using silhouette scores and additional clustering metrics.

---

# Conclusion

This project demonstrates that meaningful football playing styles can be identified directly from event data using unsupervised machine learning. By engineering player performance features, standardizing the data, and applying K-Means clustering, players naturally grouped into interpretable stylistic profiles such as creative attackers, primary finishers, ball-playing defenders, and defensive ball retainers.

These findings provide a foundation for more advanced football analytics applications, including player scouting, recruitment, similarity search, and tactical profiling.
