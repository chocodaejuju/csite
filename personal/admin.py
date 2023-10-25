from django.contrib import admin
from .models import note, NoteImage, Material, MatImage
# Register your models here.


# Photo 클래스를 inline으로 나타낸다.
class PhotoInline(admin.TabularInline):
    model = NoteImage

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다.
class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

# Register your models here.
admin.site.register(note,PostAdmin)

class PhotoInline(admin.TabularInline):
    model = MatImage

class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]
admin.site.register(Material,PostAdmin)