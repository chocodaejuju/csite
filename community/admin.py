from django.contrib import admin
from .models import Question, Shopping,SaveQ,Free,Shopping, Tip,TipImage,ShopImage,FreeImage,QImage
#from .models import Category, SaveQ

admin.site.register(SaveQ)


# Photo 클래스를 inline으로 나타낸다.
class PhotoInline(admin.TabularInline):
    model = TipImage

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다.
class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

# Register your models here.
admin.site.register(Tip,PostAdmin)

# Photo 클래스를 inline으로 나타낸다.
class PhotoInline2(admin.TabularInline):
    model = ShopImage

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다.
class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline2, ]

# Register your models here.
admin.site.register(Shopping,PostAdmin)

# Photo 클래스를 inline으로 나타낸다.
class PhotoInline3(admin.TabularInline):
    model = QImage

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다.
class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline3, ]

# Register your models here.
admin.site.register(Question,PostAdmin)


# Photo 클래스를 inline으로 나타낸다.
class PhotoInline4(admin.TabularInline):
    model = FreeImage

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다.
class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline4, ]

# Register your models here.
admin.site.register(Free,PostAdmin)