from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from core import models


@admin.register(models.Artista)
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "pais", "ano_formacao")
    search_fields = ("nome", "pais", "bio")
    list_filter = ("pais",)


@admin.register(models.Gravadora)
class GravadoraAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "pais", "ano_formacao")
    search_fields = ("nome", "pais")
    list_filter = ("pais",)


@admin.register(models.Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)


class FaixaInline(admin.TabularInline):
    model = models.Faixa
    extra = 0
    fields = ("numero", "titulo", "duracao")
    ordering = ("numero",)


@admin.register(models.Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "titulo",
        "formato",
        "data_lancamento",
        "gravadora",
        "total_faixas",
    )
    search_fields = (
        "titulo",
        "gravadora__nome",
    )
    list_filter = ("formato", "gravadora", "data_lancamento")
    date_hierarchy = "data_lancamento"
    list_select_related = ("gravadora",)  # busca as gravadoras de uma vez só
    autocomplete_fields = ("gravadora",)
    inlines = (FaixaInline,)  # editar as faixas dentro da página de lançamento

    def get_queryset(self, request):  # calcula o número de faixas para cada lançamento
        return super().get_queryset(request).annotate(_total_faixas=Count("faixas"))

    @admin.display(description=_("faixas"), ordering="_total_faixas")
    def total_faixas(self, obj):
        return obj._total_faixas


@admin.register(models.Faixa)
class FaixaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "numero", "lancamento", "duracao_formatada")
    search_fields = ("titulo", "lancamento__titulo")
    list_filter = ("lancamento__formato",)
    list_select_related = ("lancamento",)
    autocomplete_fields = ("lancamento",)

    @admin.display(description=_("duração"), ordering="duracao")
    def duracao_formatada(self, obj):
        if obj.duracao is None:
            return "-"
        minutos, segundos = divmod(int(obj.duracao.total_seconds()), 60)
        return f"{minutos}:{segundos:02d}"


@admin.register(models.PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "pais")
    search_fields = ("usuario__username", "usuario__email", "pais")
    list_filter = ("pais",)
    list_select_related = ("usuario",)
    autocomplete_fields = ("usuario",)
