from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO:
# - trocar null=True por só blank=True em bio (evita dois valores pra "vazio") (3)
# - validators em ano_formacao (ex.: mínimo 1900, máximo o ano atual) (4)
# - trocar pais por django-countries (5)
# - adicionar foto (5)
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
        ordering = ("nome",)

    def __str__(self):
        return self.nome


# TODO:
# - validators em ano_formacao (4)
# - trocar pais por django-countries (5)
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
        ordering = ("nome",)

    def __str__(self):
        return self.nome


# TODO:
# - nome com unique=True (hoje dá pra cadastrar dois "Pós-punk") (2)
class Genero(models.Model):
    nome = models.CharField(_("nome"), max_length=255)

    class Meta:
        verbose_name = _("gênero")
        verbose_name_plural = _("gêneros")
        ordering = ("nome",)

    def __str__(self):
        return self.nome


# TODO:
# - adicionar ManyToManyField para artistas (related_name="lancamentos") (1)
# - adicionar ManyToManyField para generos (blank=True) (1)
# - renomear tipo para formato (o campo guarda um Formato, não um tipo);
#   atualizar admin, filtros e script de popular junto (1)
# - decidir se o acervo é de cada usuário; se for, criar model ItemAcervo
#   (usuario, lancamento, adquirido_em, observacoes) com UniqueConstraint
#   em (usuario, lancamento) (2)
# - se quiser suportar coletâneas, mover artistas pra Faixa em vez do Lancamento (4)
# - adicionar atualizado_em (DateTimeField(auto_now=True)) (5)
# - data_lancamento obrigatória não serve pra disco só com ano conhecido;
#   considerar ano_lancamento (perde o date_hierarchy do admin) (5)
# - mesmo álbum em vinil e CD vira dois Lancamento com faixas duplicadas;
#   separar "obra" de "versão" (como o Discogs) é a solução (5)
# - adicionar imagem de capa (5)
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
        ordering = ("titulo", "data_lancamento")

    def __str__(self):
        return self.titulo


# TODO:
# - UniqueConstraint em (lancamento, numero) pra impedir duas faixas com o mesmo
#   número no mesmo lançamento (2)
# - validator em duracao pra não aceitar valor negativo (4)
# - simplificar ordering para ("lancamento", "numero") (evita JOIN por título) (4)
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
        ordering = ("lancamento__titulo", "numero", "titulo")

    def __str__(self):
        return self.titulo


# PerfilUsuario
# TODO:
# - criar o perfil automaticamente no cadastro do usuário (na view ou via
#   signal post_save), senão request.user.perfil levanta RelatedObjectDoesNotExist (3)
#   - https://docs.djangoproject.com/en/6.1/ref/signals/
# - trocar pais por django-countries (5)
# - adicionar avatar (5)
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("usuário"),
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    bio = models.TextField(_("biografia"), blank=True)
    pais = models.CharField(_("país"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("perfil de usuário")
        verbose_name_plural = _("perfis de usuários")
        ordering = ("id",)

    def __str__(self):
        return self.usuario.username
