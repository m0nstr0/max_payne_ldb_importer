"""Texture conversion shared by embedded LDB images and external KF2 images."""
import hashlib
from pathlib import Path

from max_payne_sdk.images import encode_tga
from max_payne_sdk.images.pcx import decode_pcx
from max_payne_sdk.images.scx import decode_scx


def prepare_texture(data, extension):
    extension = extension.lower().lstrip('.')
    decoder = {'pcx': decode_pcx, 'scx': decode_scx}.get(extension)
    return (encode_tga(decoder(data)), 'tga') if decoder else (data, extension)


def convert_texture_file(source, output_directory):
    """Return a Maya image path; converted copies live in a caller-chosen folder."""
    source = Path(source)
    if source.suffix.lower() not in ('.pcx', '.scx'):
        return str(source)
    data = source.read_bytes()
    converted, extension = prepare_texture(data, source.suffix)
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    destination = output / (source.stem + '_' + hashlib.sha256(data).hexdigest() + '.' + extension)
    if not destination.exists() or destination.read_bytes() != converted:
        destination.write_bytes(converted)
    return str(destination)
