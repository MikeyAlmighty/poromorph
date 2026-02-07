# Poromorph

League Of Legends Index

![Poro Logo](./assets/poro.png)

# ⚔️ LoL Champion API

Welcome to **Poromorph** — The League of Legends Champion Data analytics

---

## What is Poromorph?

Champion, item, and build database -

- ‍**Champion data**
- **Item info**
  — Stats, Passives, Actives, and Upgrade Paths
- **item builds**
  - Actives, Passives

New match ingested
Celery: update player stats
->
Celery: update champion stats
->
Celery: update matchup stats
->
Redis cache invalidated
->
API serves recommendations instantly

GET /lol/match/v5/matches/{matchId} // Fetch Game Data

## Tables (PostgreSQL)

### matches

id
patch
queue
duration

### champion_stats

champion_id
role
patch
games
wins
avg_kda
avg_cs_min
pick_rate

### champion_matchups

champion_id
opponent_champion_id
role
patch
games
winrate

### meta_snapshots

patch
role
champion_id
tier_score
last_updated

## Celery

### 1. Match ingestion worker

- Fetch match JSON
- Normalize → DB
- Enqueue aggregation tasks

### 2. Champion stat aggregator

Update rolling stats per:

- role
- patch
- queue type

### 3. Matchup calculator

For each champ vs champ in role Increment counters

### 4. Meta snapshot job (nightly)

- Rank champs per role
- Compute tier scores
- Cache results

All async. All idempotent.

## Redis (Caching)

- Performance layer
- Safety net

### Cache tier lists:

- meta:{patch}:{role}

### Cache matchup lookups:

- matchup:{patch}:{role}:{champ}:{enemy}

### Deduplicate matches:

- seen_matches:{match_id}

### Scoring

- tier*score = (winrate * 0.55) + (pick*rate * 0.25) + (matchup_strength \* 0.20)

#### Example

```python
{
  "patch": "14.2",
  "role": "JUNGLE",
  "tiers": {
    "S": ["Maokai", "Rell"],
    "A": ["Vi", "Sejuani"],
    "B": ["Lee Sin"]
  }
}
```
