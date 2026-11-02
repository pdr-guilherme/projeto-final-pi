import uuid
from pathlib import Path


def extrair_extensao(filename):
    return Path(filename).suffix.lower()


def montar_nome(extensao):
    return f"{uuid.uuid4().hex}{extensao}"


def caminho_foto(instance, filename):
    extensao = extrair_extensao(filename)
    return f"fotos/{montar_nome(extensao)}"


def caminho_capa(instance, filename):
    extensao = extrair_extensao(filename)
    return f"capas/{montar_nome(extensao)}"


def caminho_avatar(instance, filename):
    extensao = extrair_extensao(filename)
    return f"avatares/{montar_nome(extensao)}"
