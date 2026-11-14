"""Read-only Helper census for hash-inventoried original KF2/KFS files."""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import sys


def helpers_in_bytes(data, base=0, depth=0):
    from max_payne_sdk.binary import FormatError, read_exact
    from max_payne_sdk.max_kf2_reader import KF2ReaderBase
    from max_payne_sdk.max_kf2_reader.node import NodeChunkReader
    from max_payne_sdk.max_type import parseType
    if not data and depth == 0:
        raise FormatError("Empty chunk stream")
    if depth > 64:
        raise FormatError("Chunk nesting limit exceeded")
    stream, found = io.BytesIO(data), []
    while stream.tell() < len(data):
        offset = base + stream.tell()
        header = KF2ReaderBase().readChunk(stream)
        payload = read_exact(stream, header.size - 13)
        if header.id == 0x10016:
            body = io.BytesIO(payload)
            child = KF2ReaderBase().readChunk(body)
            node = NodeChunkReader().create(body, 0x10000, child)
            if body.read(1) != b"\x0d":
                raise FormatError("Expected Helper className TString")
            body.seek(-1, io.SEEK_CUR)
            name = parseType(body)
            found.append(dict(offset=offset, depth=depth, helper_version=header.version,
                              node=vars(node), className=name,
                              className_hex=name.encode("latin-1").hex(),
                              trailing_hex=body.read().hex()))
        elif header.id == 0x10005 and header.version in (0, 1, 2):
            found.extend(helpers_in_bytes(payload, offset + 13, depth + 1))
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output must be a new file")
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    inventory_bytes = args.inventory.read_bytes()
    inventory = json.loads(inventory_bytes)
    rows = inventory if isinstance(inventory, list) else inventory["files"]
    counts, classes = Counter(), Counter()
    accepted, helpers, errors = [], [], []
    for row in rows:
        path = Path(row["path"])
        if path.suffix.lower() not in (".kf2", ".kfs"):
            continue
        try:
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise ValueError("Source hash differs from retained inventory")
            matches = helpers_in_bytes(data)
            if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError("Input changed during inspection")
            source = row.get("source", "unspecified")
            name = row.get("relative_path", path.name)
            accepted.append(dict(source=source, file=name, sha256=row["sha256"]))
            counts[source + ":" + path.suffix.lower()] += 1
            for match in matches:
                classes[match["className"]] += 1
                helpers.append(dict(match, source=source, file=name, sha256=row["sha256"]))
        except (ValueError, OSError) as error:
            errors.append(dict(file=str(path), error=str(error)))
    manifest = json.dumps(sorted(accepted, key=lambda x: (x["source"], x["file"])),
                          sort_keys=True, separators=(",", ":")).encode("utf-8")
    report = dict(scope="Top-level chunks and known Mesh child streams; opaque bytes are not tag-scanned",
                  inventory_sha256=hashlib.sha256(inventory_bytes).hexdigest(),
                  files_checked=len(accepted), counts=dict(sorted(counts.items())),
                  accepted_manifest_sha256=hashlib.sha256(manifest).hexdigest(),
                  helper_count=len(helpers), classes=dict(sorted(classes.items())),
                  helpers=helpers, errors=errors)
    with args.output.open("x", encoding="utf-8") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(json.dumps({k: v for k, v in report.items() if k != "helpers"}))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
