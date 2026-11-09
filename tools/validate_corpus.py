"""Read-only validation of user-supplied, hash-inventoried assets. No Maya needed.

Inventories may be lists or {"files": [...]}; each record needs path and sha256.
Original game assets are never bundled with the tests or this repository.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', action='append', required=True)
    parser.add_argument('--sdk-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--detailed', action='store_true', help='Include every accepted asset and failure')
    args = parser.parse_args()
    sys.path.insert(0, str(args.sdk_root.resolve()))
    from max_payne_sdk.max_kf2 import MaxKF2Reader
    from max_payne_sdk.max_ldb_factory import MaxLBDReaderFactory

    counts = Counter()
    failures = []
    inventory_hashes = []
    accepted = []
    seen = set()
    for inventory_path in args.inventory:
        data = Path(inventory_path).read_bytes()
        inventory_hashes.append({'name': Path(inventory_path).name,
                                  'sha256': hashlib.sha256(data).hexdigest()})
        inventory = json.loads(data)
        records = inventory if isinstance(inventory, list) else inventory['files']
        for record in records:
            path = Path(record['path'])
            extension = path.suffix.lower()
            if extension not in ('.kf2', '.kfs', '.skd', '.ldb') or path in seen:
                continue
            seen.add(path)
            if extension == '.ldb':
                print('Checking LDB: %s' % path.name, flush=True)
            try:
                before = hashlib.sha256(path.read_bytes()).hexdigest()
                if before != record['sha256']:
                    raise ValueError('Source hash differs from retained inventory')
                if extension == '.ldb':
                    MaxLBDReaderFactory.createReader(path).parse()
                else:
                    MaxKF2Reader().parse(path)
                after = hashlib.sha256(path.read_bytes()).hexdigest()
                if after != before:
                    raise ValueError('Source hash changed during validation')
                counts[extension + ':pass'] += 1
                accepted.append({'name': path.name, 'sha256': before})
            except Exception as error:
                counts[extension + ':fail'] += 1
                failures.append({'name': path.name, 'sha256': record['sha256'],
                                  'error': '%s: %s' % (type(error).__name__, error)})
            if len(seen) % 250 == 0:
                print('Checked %d assets' % len(seen), flush=True)

    report = {'scope': 'Headless parsing only; no Maya scene or game qualification',
              'python': sys.version, 'counts': dict(counts),
              'inventories': inventory_hashes}
    report.update(compact_results(accepted, failures))
    if args.detailed:
        report.update(failures=failures, accepted_assets=accepted)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'counts': dict(counts), 'failure_count': len(failures)}))
    return bool(failures)


def compact_results(accepted, failures):
    manifest = json.dumps(sorted(accepted, key=lambda row: (row['sha256'], row['name'])),
                          sort_keys=True, separators=(',', ':')).encode('utf-8')
    groups = {}
    for failure in failures:
        group = groups.setdefault(failure['error'], {'error': failure['error'], 'count': 0,
                                                      'example': failure})
        group['count'] += 1
    return {'accepted_count': len(accepted), 'accepted_manifest_sha256': hashlib.sha256(manifest).hexdigest(),
            'failure_count': len(failures), 'failure_groups': list(groups.values())}


if __name__ == '__main__':
    sys.exit(main())
