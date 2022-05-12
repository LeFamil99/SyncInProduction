from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math


class Author(models.Model):
    """La classe définit le modèle pour la table qui inclut tous les auteurs de chansons connus
    """
    id = models.AutoField(primary_key=True) # Identifiant unique généré par django
    spotId = models.CharField(max_length=200) # Identifiant unique de Spotify
    name = models.CharField(max_length=100) # Nom de l'auteur
    desc = models.TextField(max_length=3000) # Description sommaire de l'auteur
    found = models.BooleanField(default=False) # Vrai si la description de l'auteur est trouvée
    image = models.CharField(max_length=300) # URL de l'image de l'auteur
    link = models.CharField(max_length=200, null=True, blank=True) # Lien de la page Wikipedia de l'auteur

    def __str__(self):
        """Valeur de retour du modèle

        Returns:
            String: Nom_ID
        """
        return str(self.name) + "_" + str(self.id)

class Album(models.Model):
    """La classe définit le modèle pour la table qui inclut tous les albums connus
    """
    id = models.AutoField(primary_key=True) # Identifiant unique généré par django
    spotId = models.CharField(max_length=200) # Identifiant unique de Spotify
    name = models.CharField(max_length=100) # Nom de l'album
    dat = models.IntegerField(default=2022, null=True) # Date de création de l'album
    link = models.CharField(max_length=200) # Lien de la page Spotify de l'album
    image = models.CharField(max_length=300) # URL de l'image de l'album

    def __str__(self):
        """Valeur de retour du modèle

        Returns:
            String: Nom_ID
        """
        return str(self.name) + "_" + str(self.id)


class Song(models.Model):
    """La classe définit le modèle pour la table qui inclut toutes les chansons connus
    """
    id = models.AutoField(primary_key=True) # Identifiant unique généré par django
    spotId = models.CharField(max_length=200) # Identifiant unique de Spotify
    title = models.CharField(max_length=200) # Titre de la chanson
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.CASCADE, related_name="written_by") # Auteur de la chanson 
    feats = models.ManyToManyField(Author, symmetrical=False, blank=True, related_name="feat_by") # Auteurs "featured" dans la chanson
    durationS = models.IntegerField(null=True) # Durée en secondes de la chanson
    durationM = models.IntegerField(null=True) # Durée en minutes de la chanson
    lyrics = models.TextField(max_length=10000) # Paroles de la chanson
    spotLink = models.CharField(max_length=200) # Lien de la page Spotify de la chanson
    ytLink = models.CharField(max_length=200) # Lien de la page Youtube de la chanson
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE, related_name="includes") # Album de la chanson

    def __str__(self):
        """Valeur de retour du modèle

        Returns:
            String: Titre_ID
        """
        return str(self.title) + "_" + str(self.id)

class Profile(models.Model):
    """La classe définit le modèle pour la table qui inclut tous les utilisateurs du site
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Modèle user de l'utilisateur

    def __str__(self):
        """Valeur de retour du modèle

        Returns:
            String: Username
        """
        return self.user.username

class Fav(models.Model):
    """La classe définit le modèle pour la table qui inclut tous les favoris de chaque utilisateur du site
    """
    id = models.AutoField(primary_key=True) # Identifiant unique généré par django
    date = models.DateTimeField(auto_now_add=True) # Date de création
    song = models.ForeignKey(Song, blank=True, null=True, on_delete=models.CASCADE, related_name="liked") # Chanson mise en favori
    user = models.ForeignKey(
        Profile, 
        related_name = "likes",
        blank = True,
        null=True,
        on_delete=models.CASCADE
        ) # Utilisateur mettan la chanson en favori

    def __str__(self):
        """Valeur de retour du modèle

        Returns:
            String: Username, si le favori existe, sinon "Empty"
        """
        try:
            return str(self.song) + "__" + str(self.user)
        except:
            return "Empty"

    def diff(self):
        """Calcule le temps écoulé depuis la création du favori, 
        avec l'unité de mesure la plus grande possible

        Returns:
            Object: o.value = valeur, o.tag = unité de mesure
        """
        seconds = (timezone.now() - self.date).total_seconds()
        minutes = seconds / 60
        if minutes < 1: return {"value": math.floor(seconds), "tag": "secondes"}
        hours = minutes / 60
        if hours < 1: return {"value": math.floor(minutes), "tag": "minutes"}
        days = hours / 24
        if days < 1: return {"value": math.floor(hours), "tag": "heures"}
        years = days / 365.25
        if years < 1: return {"value": math.floor(days), "tag": "jours"} 
        return {
            "value": math.floor(years), "tag": "années"
        }

    timeSince = property(diff)

    class Meta:
        """Trie les favoris en ordre chronologique de date de création
        """
        ordering = ["-date"]


from django.db.models.signals import post_save

# Permet d'automatiquement créer un modèle Profile lorsqu'un nouvel utilisateur crée un compte sur le site
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)




# Djalilou, ça c'est mon disstrack sur toi mon frère ... eh, mon pitre

# Djalilou
# Djalilou
# Es-tu prêt à subir la colère de Djalilou

# Tu parles comme un kangourou, Djalilou, Djalilou
# Cet été, t'étais où, Djalilou, Djalilou
# Aussi mytho que manitou, c'est relou, c'est relou
# Moins poli, qu'un bijou, j'te f'rais pas des bisous
# De subir la bite de Kirikou
# Aussi mature qu'un bout d'chou, t'es chelou, t'es chelou

# Djalilou
# Djalilou
