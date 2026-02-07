import sys
import os
import requests
import random
from datetime import datetime

from dotenv import load_dotenv
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poromorph.settings")
django.setup()

from champions.models import Champion, ChampionStats

load_dotenv()

DATA_DRAGON_VERSION = os.getenv("DATA_DRAGON_VERSION") 

CHAMPION_URL = f"https://ddragon.leagueoflegends.com/cdn/{DATA_DRAGON_VERSION}/data/en_US/champion.json"

def fetch_champions():
    response = requests.get(CHAMPION_URL)
    response.raise_for_status()

    data = response.json()
    champions = []

    for _, champ_info in data['data'].items():
        champions.append({
            "champion_id": int(champ_info['key']),
            "name": champ_info['name'],
            "role": champ_info.get('tags')[0] if champ_info.get('tags') else None
        })

    return champions

def ingest_champions():
    champions = fetch_champions()

    for champ in champions:
        champion_obj, _ = Champion.objects.update_or_create(
            champion_id=champ["champion_id"],
            defaults={"name": champ["name"]}
        )

        # Create mock stats for demo purposes
        pick_rate = round(random.uniform(1, 30), 2)      # percent
        win_rate = round(random.uniform(40, 60), 2)      # percent
        ban_rate = round(random.uniform(0, 10), 2)       # percent
        games_played = random.randint(1000, 50000)

        ChampionStats.objects.update_or_create(
            champion=champion_obj,
            patch=DATA_DRAGON_VERSION,
            defaults={
                "pick_rate": pick_rate,
                "win_rate": win_rate,
                "ban_rate": ban_rate,
                "games_played": games_played,
                "updated_at": datetime.now()
            }
        )

    print(f"Ingested {len(champions)} champions")

if __name__ == "__main__":
    ingest_champions()