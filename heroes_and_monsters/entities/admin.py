from django.contrib import admin
from .models import Hero, Villain, Category, Origin, HeroProxy, AllEntity, HeroAcquaintance

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    # form = HeroForm

    list_display = ("name", "is_immortal", "category", "origin")
    list_filter = ("is_immortal", "category", "origin")

@admin.register(HeroProxy)
class HeroProxyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_immortal", "category", "origin",)
    readonly_fields = ("name", "is_immortal", "category", "origin",)

@admin.register(Villain)
class VillainAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "origin")

class VillainInline(admin.StackedInline):
    model = Villain

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

    inlines = [VillainInline]

@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("name",)
