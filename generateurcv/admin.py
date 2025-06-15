from django.contrib import admin
from .models import (
    Choisircv, HeroImage, HeroSection, Sitelogo, TeamMember, Temoignage, UtilisateurSite, CV,
    Experience, Education, Skill, Language, 
    Interest, AproposHeader, Mission, Histoire,
    Valeur, SectionTitre
)
from django.utils.html import format_html


admin.site.register(Sitelogo)


@admin.register(UtilisateurSite)
class UtilisateurSiteAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'date_inscription', 'photo_preview')
    search_fields = ('nom_complet', 'email')
    list_filter = ('date_inscription',)
    readonly_fields = ('date_inscription', 'photo_preview')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 60px; height:auto; border-radius: 3px;" />',
                obj.photo.url
            )
        return "-"
    photo_preview.short_description = 'Photo'


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1


class InterestInline(admin.TabularInline):
    model = Interest
    extra = 1


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = (
        'titre', 'full_name', 'utilisateur', 'version',
        'created_at', 'preview_thumbnail', 'address', 'website', 'nationality'  # ✅ Ajouts
    )
    search_fields = (
        'titre', 'full_name', 'utilisateur__email', 'address', 'website', 'nationality'  # ✅ Ajouts
    )
    list_filter = ('created_at', 'version')
    readonly_fields = ('preview_thumbnail',)
    inlines = [ExperienceInline, EducationInline, SkillInline, LanguageInline, InterestInline]

    def preview_thumbnail(self, obj):
        if obj.preview_image:
            return format_html('<img src="{}" style="max-height:120px; border:1px solid #ccc;" />', obj.preview_image)
        return "Pas d'image"
    preview_thumbnail.short_description = "Aperçu"


@admin.register(SectionTitre)
class SectionTitreAdmin(admin.ModelAdmin):
    list_display = ('titre_header', 'titre_mission', 'titre_histoire', 'titre_equipe', 'titre_valeurs')
    search_fields = ('titre_header', 'titre_mission', 'titre_histoire', 'titre_equipe', 'titre_valeurs')


@admin.register(AproposHeader)
class AproposHeaderAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('texte_1', 'texte_2')
    search_fields = ('texte_1', 'texte_2')


@admin.register(Histoire)
class HistoireAdmin(admin.ModelAdmin):
    list_display = ('texte_1', 'texte_2')
    search_fields = ('texte_1', 'texte_2')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'photo_preview')
    search_fields = ('name', 'title')
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 60px; height:auto; border-radius: 3px;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = 'Photo'


@admin.register(Valeur)
class ValeurAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description')
    search_fields = ('titre', 'description')


class HeroImageInline(admin.TabularInline):
    model = HeroImage
    extra = 1


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['titre']
    inlines = [HeroImageInline]


admin.site.register(HeroImage)


@admin.register(Choisircv)
class ChoisircvAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'date_post', 'contenu_tronque')
    list_filter = ('date_post',)
    search_fields = ('utilisateur__nom_complet', 'contenu')
    ordering = ('-date_post',)

    def contenu_tronque(self, obj):
        return (obj.contenu[:75] + '...') if len(obj.contenu) > 75 else obj.contenu
    contenu_tronque.short_description = 'Contenu'
