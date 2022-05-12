from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile
from .models import Song
from .models import Album
from .models import Author
from .models import Fav


# Permet d'accéder à toutes tes tables de la db dans le panneau de controle admin inclus sur le site
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Author)
admin.site.register(Fav)
