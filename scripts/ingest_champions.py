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

from champions.models import Champion, ChampionStats, ChampionInfo, ChampionMedia

load_dotenv()

DATA_DRAGON_VERSION = os.getenv("DATA_DRAGON_VERSION")

CHAMPION_URL = f"https://ddragon.leagueoflegends.com/cdn/{DATA_DRAGON_VERSION}/data/en_US/champion.json"

def fetch_champions():
    response = requests.get(CHAMPION_URL)
    response.raise_for_status()

    data = response.json()
    champions = []

    for key, champ_info in data['data'].items():
        champions.append({
            "champion_id": int(champ_info['key']),
            "name": champ_info['name'],
            "blurb": champ_info["blurb"],
            "title": champ_info["title"],
            "partype": champ_info["partype"],
            "role": champ_info.get('tags')[0] if champ_info.get('tags') else None,
            "info": champ_info['info'],
            "media": champ_info['image'],
            "stats": champ_info['stats']
        })

    return champions

def ingest_champions():
    champions = fetch_champions()

    for champ in champions:
        champion_obj, _ = Champion.objects.update_or_create(
            champion_id=champ["champion_id"],
            defaults={
                "name": champ["name"],
                "role": champ["role"],
                "blurb": champ["blurb"],
                "title": champ["title"],
                "partype": champ["partype"]
            }
        )

        ChampionMedia.objects.update_or_create(
            champion=champion_obj,
            defaults={
            "full": champ["media"]["full"],
            "sprite": champ["media"]["sprite"],
            "group": champ["media"]["group"]
             }
        )

        ChampionInfo.objects.update_or_create(
            champion=champion_obj,
            patch=DATA_DRAGON_VERSION,
            defaults={
                "attack": champ["info"]["attack"],
                "defense": champ["info"]["defense"],
                "magic": champ["info"]["magic"],
                "difficulty": champ["info"]["difficulty"],
            }
        )

        ChampionStats.objects.update_or_create(
            champion=champion_obj,
            patch=DATA_DRAGON_VERSION,
            defaults={
                "hp": champ["stats"]["hp"],
                "hpperlevel": champ["stats"]["hpperlevel"],
                "mp": champ["stats"]["mp"],
                "mpperlevel": champ["stats"]["mpperlevel"],
                "movespeed": champ["stats"]["movespeed"],
                "armor": champ["stats"]["armor"],
                "armorperlevel": champ["stats"]["armorperlevel"],
                "spellblock": champ["stats"]["spellblock"],
                "spellblockperlevel": champ["stats"]["spellblockperlevel"],
                "attackrange": champ["stats"]["attackrange"],
                "hpregen": champ["stats"]["hpregen"],
                "hpregenperlevel": champ["stats"]["hpregenperlevel"],
                "mpregen": champ["stats"]["mpregen"],
                "mpregenperlevel": champ["stats"]["mpregenperlevel"],
                "crit": champ["stats"]["crit"],
                "critperlevel": champ["stats"]["critperlevel"],
                "attackdamage": champ["stats"]["attackdamage"],
                "attackdamageperlevel": champ["stats"]["attackdamageperlevel"],
                "attackspeedperlevel": champ["stats"]["attackspeedperlevel"],
                "attackspeed": champ["stats"]["attackspeed"]
            }
        )
        print(f"Ingested: {champ["name"]}")

if __name__ == "__main__":
    ingest_champions()
