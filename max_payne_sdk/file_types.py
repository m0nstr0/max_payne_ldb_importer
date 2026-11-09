"""Translator selection without importing Maya."""
from pathlib import PurePath


def has_extension(path, extensions):
    return PurePath(path).suffix.lower().lstrip('.') in extensions
