# MP2 source comparison — 2026-11-14

The source projects are sibling workspace inputs, not dependencies of this
repository. [Input pins](mp2-source-pins-2026-11-14.json) record paths, byte sizes
and SHA-256 hashes for reproduction within the retained workspace. They are not
public download links. No target DLL was built, installed or executed for this
documentation update.

| Source | Result used in the specifications |
| --- | --- |
| MP2KF2 LoaderAuxiliaryChunks | Helper Node + className; Camera and Environment reconfirmed |
| MP2KF2 KeyframeAnimationChunk | Version guards, normalization field, retained scaling bool |
| MP2KF2 KeyframeAnimationLoading/Playback, KeyframeSampling, AnimationNumeric | Matrix vs compressed tracks, coefficient interpolation, normalization and scale restoration |
| MP2Level X_Level, X_LevelStringPool | Minimum revision 22, section gates, byte offsets and unsigned raw pool shorts |
| MP2Grph G_FColor | HSV-to-byte-scale RGB conversion used by volume lighting |
| MP2Level X_LevelVolumeLighting | Positive-dimension load gate, 12-byte samples, channel decode, trilinear and filtered sampling |
| MP2Level X_LevelDynamicMeshAnimation | Translation distance units, normalized graph time, quaternion rotation path |
| MP2Level X_LevelDynamicMesh, X_LevelMesh, X_LevelTrigger | Sequential prefab registration and selected revision branches |
| MP2LevelRuntime ObjectBase and Exit | State chunk layouts and their boundary with LDB/LV2 |

Retained evidence, not newly executed tests: KF2 final source R3 matrix reports
30 finite families with two dependency sets and no reported failures (exit 83
is expected in the secondary-exception controls); Level math comparison accepts a
2076-call/12-control-word Animation/Volume/Plane domain; LevelRuntime serialization
comparison accepts 1423 calls and matching saved bytes. Their coverage is bounded.
In particular the isolated serialization domain has no positive room lookup.
Source-only branches must not be described as new runtime test coverage.

The existing canonical C++ and Python LDB2 readers use set membership for prefab
registration. They can misclassify a skipped new ID; a focused validation follow-up
is recorded in TODO.md. No reader or writer was changed here. The runtime projects
do not supply MaxED2 editor serialization, so no missing LV2 entity payload was
inferred from similarly named runtime classes.

## Prefab validation follow-up — 2026-11-14

The validation gap described above is now fixed in both readers. New regression
fixtures distinguish skipped IDs from truncated input. The implementation and
new corpus checks are recorded in [PREFAB_VALIDATION.md](PREFAB_VALIDATION.md).
The original source-comparison observations remain as dated evidence.
