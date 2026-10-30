from datetime import timedelta

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import caminho_avatar, caminho_capa, caminho_foto


# TODO:
# - trocar pais por django-countries (5)
class Artista(models.Model):
    nome = models.CharField(_("nome"), max_length=255)
    pais = models.CharField(_("país"), max_length=100)
    ano_formacao = models.PositiveSmallIntegerField(
        _("ano de formação"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1800)],
    )
    bio = models.TextField(_("biografia"), blank=True)
    foto = models.ImageField(_("foto"), upload_to=caminho_foto, blank=True)

    class Meta:
        verbose_name = _("artista")
        verbose_name_plural = _("artistas")
        ordering = ("nome",)

    def __str__(self):
        return self.nome


# TODO:
# - trocar pais por django-countries (5)
class Gravadora(models.Model):
    nome = models.CharField(_("nome"), max_length=255)
    pais = models.CharField(_("país"), max_length=100)
    ano_formacao = models.PositiveSmallIntegerField(
        _("ano de formação"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1800)],
    )

    class Meta:
        verbose_name = _("gravadora")
        verbose_name_plural = _("gravadoras")
        ordering = ("nome",)

    def __str__(self):
        return self.nome


class Genero(models.Model):
    nome = models.CharField(_("nome"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("gênero")
        verbose_name_plural = _("gêneros")
        ordering = ("nome",)

    def __str__(self):
        return self.nome


# TODO:
#   atualizar admin, filtros e script de popular junto (1)
# - decidir se o acervo é de cada usuário; se for, criar model ItemAcervo
#   (usuario, lancamento, adquirido_em, observacoes) com UniqueConstraint
#   em (usuario, lancamento) (2)
# - se quiser suportar coletâneas, mover artistas pra Faixa em vez do Lancamento (4)
# - mesmo álbum em vinil e CD vira dois Lancamento com faixas duplicadas;
#   separar "obra" de "versão" (como o Discogs) é a solução (5)
class Lancamento(models.Model):
    class Formato(models.TextChoices):
        VINIL = "vinil", _("Vinil")
        CD = "cd", _("CD")
        CASSETE = "cassete", _("Fita cassete")
        DIGITAL = "digital", _("Digital")
        DVD = "dvd", _("DVD / Blu-ray")
        OUTRO = "outro", _("Outro")

    titulo = models.CharField(_("título"), max_length=255)
    capa = models.ImageField(_("capa"), upload_to=caminho_capa, blank=True)
    formato = models.CharField(_("formato"), max_length=20, choices=Formato.choices)
    data_lancamento = models.DateField(_("data de lançamento"))
    gravadora = models.ForeignKey(
        Gravadora,
        verbose_name=_("gravadora"),
        on_delete=models.PROTECT,
        related_name="lancamentos",
    )
    criado_em = models.DateTimeField(_("criado em"), auto_now_add=True)
    editado_em = models.DateTimeField(_("editado em"), auto_now=True)
    artistas = models.ManyToManyField(
        Artista, verbose_name=_("artistas"), related_name="lancamentos"
    )
    generos = models.ManyToManyField(
        Genero,
        verbose_name=_("gêneros"),
        related_name="lancamentos",
        blank=True,
    )

    class Meta:
        verbose_name = _("lançamento")
        verbose_name_plural = _("lançamentos")
        ordering = ("titulo", "data_lancamento")

    def __str__(self):
        return self.titulo


class Faixa(models.Model):
    titulo = models.CharField(_("título"), max_length=255)
    numero = models.PositiveSmallIntegerField(_("número"))
    duracao = models.DurationField(
        _("duração"),
        null=True,
        blank=True,
        validators=[MinValueValidator(timedelta(seconds=1))],
    )
    lancamento = models.ForeignKey(
        Lancamento,
        verbose_name=_("lançamento"),
        on_delete=models.CASCADE,
        related_name="faixas",
    )

    class Meta:
        verbose_name = _("faixa")
        verbose_name_plural = _("faixas")
        ordering = ("lancamento_id", "numero", "titulo")
        constraints = [
            models.UniqueConstraint(
                fields=["lancamento", "numero"],
                name="unique_lancamento_numero",
            )
        ]

    def __str__(self):
        return self.titulo


# TODO:
# - trocar pais por django-countries (5)
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuário"),
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    bio = models.TextField(_("biografia"), blank=True)
    pais = models.CharField(_("país"), max_length=100, blank=True)
    avatar = models.ImageField(_("capa"), upload_to=caminho_avatar, blank=True)

    class Meta:
        verbose_name = _("perfil de usuário")
        verbose_name_plural = _("perfis de usuários")
        ordering = ("id",)

    def __str__(self):
        return self.usuario.username
