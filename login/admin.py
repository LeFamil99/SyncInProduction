from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile
from .models import Song
from .models import Album
from .models import Author
from .models import Fav
# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)

admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Author)
admin.site.register(Fav)
