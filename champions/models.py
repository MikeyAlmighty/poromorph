from django.db import models

class Champion(models.Model):
    champion_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class ChampionStats(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE, related_name="stats")
    patch = models.CharField(max_length=20)
    pick_rate = models.FloatField()
    win_rate = models.FloatField()
    ban_rate = models.FloatField()
    games_played = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("champion", "patch")
    
    def __str__(self):
        return f"{self.champion.name} ({self.patch})"