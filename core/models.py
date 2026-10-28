from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO: usar biblioteca de paises nesses modelos (https://github.com/SmileyChris/django-countries)
# TODO: adicionar foto a esse modelo
class Artista(models.Model):
    nome = models.CharField(_("nome"), max_length=255)
    pais = models.CharField(_("país"), max_length=100)
    ano_formacao = models.PositiveSmallIntegerField(
        _("ano de formação"),
        null=True,
        blank=True,
    )
    bio = models.TextField(_("biografia"), null=True, blank=True)

    class Meta:
        verbose_name = _("artista")
        verbose_name_plural = _("artistas")
        db_table = "artistas"
        ordering = ("nome",)

    def __str__(self):
        return self.nome


class Gravadora(models.Model):
    nome = models.CharField(_("nome"), max_length=255)
    pais = models.CharField(_("país"), max_length=100)
    ano_formacao = models.PositiveSmallIntegerField(
        _("ano de formação"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("gravadora")
        verbose_name_plural = _("gravadoras")
        db_table = "gravadoras"
        ordering = ("nome",)

    def __str__(self):
        return self.nome


class Genero(models.Model):
    nome = models.CharField(_("nome"), max_length=255)

    class Meta:
        verbose_name = _("gênero")
        verbose_name_plural = _("gêneros")
        db_table = "generos"
        ordering = ("nome",)

    def __str__(self):
        return self.nome


# TODO: adicionar imagem de capa
class Lancamento(models.Model):
    class Formato(models.TextChoices):
        VINIL = "vinil", _("Vinil")
        CD = "cd", _("CD")
        CASSETE = "cassete", _("Fita cassete")
        DIGITAL = "digital", _("Digital")
        DVD = "dvd", _("DVD / Blu-ray")
        OUTRO = "outro", _("Outro")

    titulo = models.CharField(_("título"), max_length=255)
    tipo = models.CharField(_("tipo"), max_length=20, choices=Formato.choices)
    data_lancamento = models.DateField(_("data de lançamento"))
    gravadora = models.ForeignKey(
        Gravadora,
        verbose_name=_("gravadora"),
        on_delete=models.PROTECT,
        related_name="lancamentos",
    )
    criado_em = models.DateTimeField(_("criado em"), auto_now_add=True)

    class Meta:
        verbose_name = _("lançamento")
        verbose_name_plural = _("lançamentos")
        db_table = "lancamentos"
        ordering = ("titulo", "data_lancamento")

    def __str__(self):
        return self.titulo


class Faixa(models.Model):
    titulo = models.CharField(_("título"), max_length=255)
    numero = models.PositiveSmallIntegerField(_("número"))
    duracao = models.DurationField(_("duração"), null=True, blank=True)
    lancamento = models.ForeignKey(
        Lancamento,
        verbose_name=_("lançamento"),
        on_delete=models.CASCADE,
        related_name="faixas",
    )

    class Meta:
        verbose_name = _("faixa")
        verbose_name_plural = _("faixas")
        db_table = "faixas"
        ordering = ("lancamento__titulo", "numero", "titulo")

    def __str__(self):
        return self.titulo


# TODO: adicionar campo de avatar
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        User, verbose_name=_("usuário"), on_delete=models.CASCADE
    )
    bio = models.TextField(_("biografia"), blank=True, null=True)
    pais = models.CharField(_("país"), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("perfil de usuário")
        verbose_name_plural = _("perfis de usuários")
        db_table = "perfis"
        ordering = ("usuario__username",)

    def __str__(self):
        return self.usuario.username
