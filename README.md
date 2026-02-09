# Poromorph

![Poro Logo](./assets/poro.png)

# League Of Legends Champion Data Index

## What is Poromorph?
---

**Poromorph** is a Django-based application that tracks **League of Legends champion stats** and **changes per patch**. It periodically fetches the latest champion data from Riot's Data Dragon API, stores champion stats and media, and keeps track of **patch history** over time. With automatic patch updates via [Celery](https://docs.celeryq.dev/en/v5.6.0/getting-started/introduction.html), **Poromorph** helps monitor and visualize stat changes across game patches.

#### Running
Infra: `docker compose up -d`

### TODO
- [ ] Cache **per-patch** data in Redis.
- [ ] Ping `https://ddragon.leagueoflegends.com/api/versions.json` for latest version (CRON)
- [ ] Upon patch release (CRON) kick-off data ingestion pipeline via Celery.
