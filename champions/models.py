from django.db import models

class Champion(models.Model):
    class Partype(models.TextChoices):
        MANA = "Mana", "Mana"
        ENERGY = "Energy", "Energy"
        NONE = "None", "None"
        RAGE = "Rage", "Rage"
        SHIELD = "Shield", "Shield"
        BLOOD_WELL = "BloodWell", "Blood Well"
        FURY = "Fury", "Fury"
        MANA_SHIELD = "ManaShield", "Mana Shield"

    champion_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    blurb = models.CharField(max_length=1000, blank=True)
    title = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    partype = models.CharField(
        max_length=20,
        choices=Partype.choices,
        default=Partype.MANA
    )

    def __str__(self):
        return self.name

class ChampionMedia(models.Model):
    champion = models.ForeignKey(
        "Champion",
        on_delete=models.CASCADE,
        related_name="media"
    )
    full = models.CharField(max_length=50, blank=True)
    sprite = models.CharField(max_length=50, blank=True)
    group = models.CharField(max_length=50, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full

class ChampionInfo(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE, related_name="info")
    attack = models.IntegerField()
    patch = models.CharField(max_length=10, blank=True)
    defense = models.IntegerField()
    magic = models.IntegerField()
    difficulty = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("champion", "patch")

class ChampionStats(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE, related_name="stats")
    patch = models.CharField(max_length=10, blank=True)
    hp = models.FloatField(null=True, blank=True)
    hpperlevel = models.FloatField(null=True, blank=True)
    mp = models.FloatField(null=True, blank=True)
    mpperlevel = models.FloatField(null=True, blank=True)
    movespeed = models.FloatField(null=True, blank=True)
    armor = models.FloatField(null=True, blank=True)
    armorperlevel = models.FloatField(null=True, blank=True)
    spellblock = models.FloatField(null=True, blank=True)
    spellblockperlevel = models.FloatField(null=True, blank=True)
    attackrange = models.FloatField(null=True, blank=True)
    hpregen = models.FloatField(null=True, blank=True)
    hpregenperlevel = models.FloatField(null=True, blank=True)
    mpregen = models.FloatField(null=True, blank=True)
    mpregenperlevel = models.FloatField(null=True, blank=True)
    crit = models.FloatField(null=True, blank=True)
    critperlevel = models.FloatField(null=True, blank=True)
    attackdamage = models.FloatField(null=True, blank=True)
    attackdamageperlevel = models.FloatField(null=True, blank=True)
    attackspeedperlevel = models.FloatField(null=True, blank=True)
    attackspeed = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("champion", "patch")
    
    def __str__(self):
        return f"{self.champion.name} ({self.patch})"